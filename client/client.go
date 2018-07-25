package main

import (
	"flag"

	"github.com/SKF/go-enlight-sdk/grpc"
	"github.com/SKF/go-enlight-sdk/services/iot"
	"github.com/SKF/go-utility/log"

	api "github.com/SKF/go-enlight-sdk/services/iot/iotgrpcapi"
)

func dialGRPC() iot.IoTClient {
	HOST := "grpc.sandbox.iot.enlight.skf.com"
	PORT := "50051"

	CLIENTCRT := "client/cert/client.crt"
	CLIENTKEY := "client/cert/client.key"
	CACRT := "client/cert/ca.crt"

	log.Info("CreateClient")
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

	log.Info("DeepPing")
	if err = client.DeepPing(); err != nil {
		log.WithError(err).Error("client.DeepPing")
		return nil
	}

	return client
}

func parseFlags() (int64, float64, string, string) {
	timePtr := flag.Int64("time", -1, "unix time in ms")
	dataPtr := flag.Float64("data", -1.0, "data of type float")
	unitPtr := flag.String("unit", "", "unit of data")
	idPtr := flag.String("id", "", "node id")

	flag.Parse()

	return *timePtr, *dataPtr, *unitPtr, *idPtr
}

func main() {

	time, data, unit, id := parseFlags()
	client := dialGRPC()

	if client == nil {
		return
	}

	defer client.Close()

	nodeData := api.NodeData{
		CreatedAt:   time,
		ContentType: api.NodeDataContentType_DATA_POINT,
		DataPoint: &api.DataPoint{
			Coordinate: &api.Coordinate{X: float64(time), Y: data},
			XUnit:      "ms",
			YUnit:      unit,
		},
	}

	log.WithField("nodeData", nodeData).Info("IngestNodeData")
	err := client.IngestNodeData(id, nodeData)
	if err != nil {
		log.
			WithError(err).
			WithField("nodeID", id).
			WithField("nodeData", nodeData).
			Error("client.IngestNodeData")
	}

}