package main

import (
	"flag"

	"github.com/SKF/go-enlight-sdk/grpc"
	"github.com/SKF/go-enlight-sdk/services/iot"
	"github.com/SKF/go-utility/log"

	api "github.com/SKF/go-enlight-sdk/services/iot/iotgrpcapi"
)

func main() {
	HOST := "grpc.sandbox.iot.enlight.skf.com"
	PORT := "50051"

	clientCrt := "cert/client.crt"
	clientKey := "cert/client.key"
	caCert := "cert/ca.crt"

	var err error

	// log.Info("Setup Client")
	client := iot.CreateClient()
	transportOption, err := grpc.WithTransportCredentials(
		HOST, clientCrt, clientKey, caCert,
	)
	if err != nil {
		log.
			WithError(err).
			WithField("serverName", HOST).
			WithField("clientCrt", clientCrt).
			WithField("clientKey", clientKey).
			WithField("caCert", caCert).
			Error("grpc.WithTransportCredentials")
		return
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
		return
	}

	defer client.Close()

	// log.Info("DeepPing")
	if err = client.DeepPing(); err != nil {
		log.WithError(err).Error("client.DeepPing")
		return
	}

	datePtr := flag.Int64("datetime", -1, "unix time in ms")
	dataPtr := flag.Float64("data", -1.0, "temperature in celsius")
	unitPtr := flag.String("unit", "", "unit of data")
	idPtr := flag.String("id", "", "node id")
	flag.Parse()

	nodeData := api.NodeData{
		CreatedAt:   *datePtr,
		ContentType: api.NodeDataContentType_DATA_POINT,
		DataPoint: &api.DataPoint{
			Coordinate: &api.Coordinate{X: float64(*datePtr), Y: *dataPtr},
			XUnit:      "ms",
			YUnit:      *unitPtr,
		},
	}

	// log.WithField("nodeData", nodeData).Info("IngestNodeData")
	err = client.IngestNodeData(*idPtr, nodeData)
	if err != nil {
		log.
			WithError(err).
			WithField("nodeID", *idPtr).
			WithField("nodeData", nodeData).
			Error("client.IngestNodeData")
	}

}
