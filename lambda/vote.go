package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"time"

	"github.com/tidwall/gjson"

	"github.com/SKF/go-enlight-sdk/grpc"
	"github.com/SKF/go-enlight-sdk/services/iot"
	"github.com/SKF/go-utility/log"
	"github.com/aws/aws-lambda-go/events"
	"github.com/aws/aws-lambda-go/lambda"

	api "github.com/SKF/go-enlight-sdk/services/iot/iotgrpcapi"
)

func dialGRPC() iot.IoTClient {
	HOST := "grpc.sandbox.iot.enlight.skf.com"
	PORT := "50051"

	CLIENTCRT := "cert/client.crt"
	CLIENTKEY := "cert/client.key"
	CACRT := "cert/ca.crt"

	var err error

	log.Info("Setup Client")
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

	log.Info("Deep Ping")
	if err = client.DeepPing(); err != nil {
		log.WithError(err).Error("client.DeepPing")
		return nil
	}

	return client
}

func handleRequest(request events.APIGatewayProxyRequest) (events.APIGatewayProxyResponse, error) {
	type Vote struct {
		FuncLoc string   `json:"func_loc"`
		Asset   string   `json:"asset"`
		Answer  []string `json:"answer"`
	}

	var body Vote
	var client = dialGRPC()
	defer client.Close()

	jsonFile, _ := ioutil.ReadFile("config.json")
	jsonString := string(jsonFile)

	err := json.Unmarshal([]byte(request.Body), &body)
	if err != nil {
		fmt.Println("error:", err)
	}

	nodeID := gjson.Get(jsonString, body.FuncLoc+"."+body.Asset+".vote").String()
	nodeData := api.NodeData{
		CreatedAt:       time.Now().Unix() * 1000,
		ContentType:     api.NodeDataContentType_QUESTION_ANSWERS,
		QuestionAnswers: body.Answer,
	}

	log.Info("Ingest Data")
	err = client.IngestNodeData(nodeID, nodeData)
	if err != nil {
		log.
			WithError(err).
			WithField("nodeID", nodeID).
			WithField("nodeData", nodeData).
			Error("client.IngestNodeData")
	}

	return events.APIGatewayProxyResponse{Body: request.Body, Headers: map[string]string{"Access-Control-Allow-Origin": "*"}, StatusCode: 200}, nil
}

func main() {
	lambda.Start(handleRequest)
}
