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
	"github.com/SKF/go-utility/log"

	"github.com/SKF/go-enlight-sdk/grpc"
	"github.com/SKF/go-enlight-sdk/services/iot"
	iotapi "github.com/SKF/go-enlight-sdk/services/iot/iotgrpcapi"
	"github.com/SKF/go-enlight-sdk/services/pas/pasapi"
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
	nodeIDs := config[funcLoc][asset]

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

	id := 0

	var pointData float64
	// GetLatestNodeData from every nodeID and send them over SSE
	for pointName, pointID := range nodeIDs {
		// Make sure to ignore IDs which begin and ends with "__"
		if string(pointName[:2]) != "__" && string(pointName[len(pointName)-2:]) != "__" {
			latestInput := iotapi.GetLatestNodeDataInput{NodeId: pointID, ContentType: 1}
			latestOutput, err := iotClient.GetLatestNodeData(latestInput)
			if err != nil {
				log.Error(err)
			}
			pointData = latestOutput.DataPoint.Coordinate.Y

			latestAlarmInput := pasapi.GetPointAlarmStatusInput{NodeId: pointID}
			latestAlarm, err := pasClient.GetPointAlarmStatus(latestAlarmInput)
			if err != nil {
				log.Error(err)
			}
			pointAlarmStatus := latestAlarm

			jsonData := map[string]interface{}{"node_data": pointData, "point_name": pointName, "alarm_status": pointAlarmStatus}
			sseData, _ := json.Marshal(jsonData)
			fmt.Fprintf(w, "id: %v\ndata: %s\n\n", id, string(sseData))
			flusher.Flush()
			id++
		}
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
				// s, _ := status.FromError(err)
				iotClient = DialIoT()
			}
		}
	}()

	// Listen to stream and filter on correct IDs and send data over SSE
	for data := range stream {
		for pointName, pointID := range nodeIDs {
			if data.NodeId == pointID {
				pointData = data.NodeData.DataPoint.Coordinate.Y
				latestAlarmInput := pasapi.GetPointAlarmStatusInput{NodeId: pointID}
				latestAlarm, err := pasClient.GetPointAlarmStatus(latestAlarmInput)
				if err != nil {
					log.Error(err)
					// TODO Add reconnection here
					// s, _ := status.FromError(err)
					pasClient = DialPAS()
				}
				pointAlarmStatus := latestAlarm

				jsonData := map[string]interface{}{"node_data": pointData, "point_name": pointName, "alarm_status": pointAlarmStatus}
				sseData, _ := json.Marshal(jsonData)
				fmt.Fprintf(w, "id: %v\ndata: %s\n\n", id, string(sseData))
				flusher.Flush()
				id++
			}
		}
	}
}

func main() {
	fmt.Println("Server is now running on port 5000...")
	http.HandleFunc("/", Stream)
	if err := http.ListenAndServe(":5000", nil); err != nil {
		log.Error(err)
	}

	return
}
