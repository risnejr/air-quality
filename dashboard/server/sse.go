package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
	"os"
	"os/signal"
	"syscall"

	"github.com/SKF/go-enlight-sdk/services/pas"

	"github.com/SKF/go-enlight-sdk/grpc"
	"github.com/SKF/go-enlight-sdk/services/iot"
	iotapi "github.com/SKF/go-enlight-sdk/services/iot/iotgrpcapi"
	"github.com/SKF/go-enlight-sdk/services/pas/pasapi"
	"github.com/SKF/go-utility/log"
)

// Config map[functional_location_name]map[asset_name]map[point_name]point_id
type Config map[string]map[string]map[string]string

// DialIoT returns an IoTClient client
func DialIoT() iot.IoTClient {
	HOST := "grpc.sandbox.iot.enlight.skf.com"
	PORT := "50051"

	CLIENTCRT := "../../certs/iot/client.crt"
	CLIENTKEY := "../../certs/iot/client.key"
	CACRT := "../../certs/iot/ca.crt"

	client := iot.CreateClient()
	transportOption, err := grpc.WithTransportCredentials(
		HOST, CLIENTCRT, CLIENTKEY, CACRT,
	)
	if err != nil {
		log.
			WithError(err).
			WithField("serverName", HOST).
			WithField("clientCrt", CLIENTCRT).
			WithField("clientKey", CLIENTKEY).
			WithField("caCert", CACRT).
			Error("grpc.WithTransportCredentials")
		return nil
	}

	err = client.Dial(
		HOST, PORT,
		transportOption,
		grpc.WithBlock(),
		grpc.FailOnNonTempDialError(true),
	)
	if err != nil {
		log.
			WithError(err).
			WithField("host", HOST).
			WithField("port", PORT).
			Error("client.Dial")
		return nil
	}

	if err = client.DeepPing(); err != nil {
		log.WithError(err).Error("client.DeepPing")
		return nil
	}

	return client
}

// DialPAS returns a PASClient
func DialPAS() pas.PointAlarmStatusClient {
	HOST := "grpc.point-alarm-status.sandbox.hierarchy.enlight.skf.com"
	PORT := "50051"

	CLIENTCRT := "../../certs/pas/client.crt"
	CLIENTKEY := "../../certs/pas/client.key"
	CACRT := "../../certs/pas/ca.crt"

	client := pas.CreateClient()
	transportOption, err := grpc.WithTransportCredentials(
		HOST, CLIENTCRT, CLIENTKEY, CACRT,
	)
	if err != nil {
		log.
			WithError(err).
			WithField("serverName", HOST).
			WithField("clientCrt", CLIENTCRT).
			WithField("clientKey", CLIENTKEY).
			WithField("caCert", CACRT).
			Error("grpc.WithTransportCredentials")
		return nil
	}

	err = client.Dial(
		HOST, PORT,
		transportOption,
		grpc.WithBlock(),
		grpc.FailOnNonTempDialError(true),
	)
	if err != nil {
		log.
			WithError(err).
			WithField("host", HOST).
			WithField("port", PORT).
			Error("client.Dial")
		return nil
	}

	if err = client.DeepPing(); err != nil {
		log.WithError(err).Error("client.DeepPing")
		return nil
	}

	return client
}

// Stream is a handler that sends SSE packages
func Stream(w http.ResponseWriter, r *http.Request) {
	// Make sure that streaming is supported
	flusher, ok := w.(http.Flusher)
	if !ok {
		http.Error(w, "Streaming unsupported!", http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "text/event-stream")
	w.Header().Set("Cache-Control", "no-cache")
	w.Header().Set("Connection", "keep-alive")
	w.Header().Set("Access-Control-Allow-Origin", "*")

	// Get functional location and asset from url parameters
	query := r.URL.Query()
	funcLoc := query["func_loc"][0]
	asset := query["asset"][0]

	// Read config file and extract corresponding node ids
	jsonConfig, err := ioutil.ReadFile("../../config.json")
	if err != nil {
		log.Error(err)
	}
	var config Config
	json.Unmarshal(jsonConfig, &config)
	nodeIds := config[funcLoc][asset]

	// Dial and defer connection with gRPC server
	iotClient := DialIoT()
	pasClient := DialPAS()
	defer iotClient.Close()
	defer pasClient.Close()

	// Make sure to close client if ctrl+c is invoked
	c := make(chan os.Signal)
	signal.Notify(c, os.Interrupt, syscall.SIGTERM)
	go func() {
		<-c
		iotClient.Close()
		pasClient.Close()
		os.Exit(1)
	}()

	var pointData interface{}
	// GetLatestNodeData from every nodeID and send them over SSE
	for pointName, pointId := range nodeIds {
		if pointName != "vote" && pointName != "air_quality" {
			latestInput := iotapi.GetLatestNodeDataInput{NodeId: pointId, ContentType: 1}
			latestOutput, err := iotClient.GetLatestNodeData(latestInput)
			if err != nil {
				log.Error(err)
				// s, ok := status.FromError(err)
				// fmt.Println(s, ok)
			}
			pointData = latestOutput.DataPoint.Coordinate.Y
		} else {
			latestInput := iotapi.GetLatestNodeDataInput{NodeId: pointId, ContentType: 6}
			latestOutput, err := iotClient.GetLatestNodeData(latestInput)
			if err != nil {
				log.Error(err)
			}
			pointData = latestOutput.QuestionAnswers
		}
		latestAlarmInput := pasapi.GetPointAlarmStatusInput{NodeId: pointId}
		latestAlarm, err := pasClient.GetPointAlarmStatus(latestAlarmInput)
		if err != nil {

		}
		pointAlarmStatus := latestAlarm

		// fmt.Println(pointData, pointName, pointAlarmStatus)
		jsonData := map[string]interface{}{"node_data": pointData, "point_name": pointName, "alarm_status": pointAlarmStatus}
		sseData, _ := json.Marshal(jsonData)
		fmt.Fprintf(w, "data: %s\n\n", string(sseData))
		flusher.Flush()
	}

	// Setup in and outputs of GetNodeDataStream
	input := iotapi.GetNodeDataStreamInput{}
	stream := make(chan iotapi.GetNodeDataStreamOutput)

	go func() {
		for {
			err = iotClient.GetNodeDataStream(input, stream)
			if err != nil {
				log.Error(err)
				// TODO Add reconnection here
				iotClient = DialIoT()
			}
			fmt.Println("test")
		}
	}()

	// Listen to stream and filter on correct IDs and send data over SSE
	for data := range stream {
		for pointName, pointId := range nodeIds {
			if data.NodeId == pointId {
				if pointName != "vote" && pointName != "air_quality" {
					pointData = data.NodeData.DataPoint.Coordinate.Y
				} else {
					pointData = data.NodeData.QuestionAnswers
				}
				latestAlarmInput := pasapi.GetPointAlarmStatusInput{NodeId: pointId}
				latestAlarm, err := pasClient.GetPointAlarmStatus(latestAlarmInput)
				if err != nil {
					log.Error(err)
					// TODO Add reconnection here
					pasClient = DialPAS()
				}
				pointAlarmStatus := latestAlarm

				// fmt.Println(pointData, pointName, pointAlarmStatus)
				jsonData := map[string]interface{}{"node_data": pointData, "point_name": pointName, "alarm_status": pointAlarmStatus}
				sseData, _ := json.Marshal(jsonData)
				fmt.Fprintf(w, "data: %s\n\n", string(sseData))
				flusher.Flush()
			}
		}
	}
}

func main() {
	http.HandleFunc("/", Stream)
	if err := http.ListenAndServe(":5000", nil); err != nil {
		log.Error(err)
	}

	return
}
