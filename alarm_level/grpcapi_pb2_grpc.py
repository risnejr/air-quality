# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

import alarm_level.grpcapi_pb2 as grpcapi__pb2


class IoTStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.DeepPing = channel.unary_unary(
        '/iotgrpcapi.IoT/DeepPing',
        request_serializer=grpcapi__pb2.PrimitiveVoid.SerializeToString,
        response_deserializer=grpcapi__pb2.PrimitiveString.FromString,
        )
    self.CreateTask = channel.unary_unary(
        '/iotgrpcapi.IoT/CreateTask',
        request_serializer=grpcapi__pb2.InitialTaskDescription.SerializeToString,
        response_deserializer=grpcapi__pb2.PrimitiveString.FromString,
        )
    self.GetAllTasks = channel.unary_unary(
        '/iotgrpcapi.IoT/GetAllTasks',
        request_serializer=grpcapi__pb2.PrimitiveString.SerializeToString,
        response_deserializer=grpcapi__pb2.TaskDescriptions.FromString,
        )
    self.GetUncompletedTasks = channel.unary_unary(
        '/iotgrpcapi.IoT/GetUncompletedTasks',
        request_serializer=grpcapi__pb2.PrimitiveString.SerializeToString,
        response_deserializer=grpcapi__pb2.TaskDescriptions.FromString,
        )
    self.SetTaskCompleted = channel.unary_unary(
        '/iotgrpcapi.IoT/SetTaskCompleted',
        request_serializer=grpcapi__pb2.TaskUser.SerializeToString,
        response_deserializer=grpcapi__pb2.PrimitiveVoid.FromString,
        )
    self.DeleteTask = channel.unary_unary(
        '/iotgrpcapi.IoT/DeleteTask',
        request_serializer=grpcapi__pb2.TaskUser.SerializeToString,
        response_deserializer=grpcapi__pb2.PrimitiveVoid.FromString,
        )
    self.GetUncompletedTasksByHierarchy = channel.unary_unary(
        '/iotgrpcapi.IoT/GetUncompletedTasksByHierarchy',
        request_serializer=grpcapi__pb2.PrimitiveString.SerializeToString,
        response_deserializer=grpcapi__pb2.TaskDescriptions.FromString,
        )
    self.SetTaskStatus = channel.unary_unary(
        '/iotgrpcapi.IoT/SetTaskStatus',
        request_serializer=grpcapi__pb2.SetTaskStatusInput.SerializeToString,
        response_deserializer=grpcapi__pb2.PrimitiveVoid.FromString,
        )
    self.IngestNodeData = channel.unary_unary(
        '/iotgrpcapi.IoT/IngestNodeData',
        request_serializer=grpcapi__pb2.IngestNodeDataInput.SerializeToString,
        response_deserializer=grpcapi__pb2.IngestNodeDataOutput.FromString,
        )
    self.GetNodeData = channel.unary_unary(
        '/iotgrpcapi.IoT/GetNodeData',
        request_serializer=grpcapi__pb2.GetNodeDataInput.SerializeToString,
        response_deserializer=grpcapi__pb2.GetNodeDataOutput.FromString,
        )
    self.GetNodeDataStream = channel.unary_stream(
        '/iotgrpcapi.IoT/GetNodeDataStream',
        request_serializer=grpcapi__pb2.GetNodeDataStreamInput.SerializeToString,
        response_deserializer=grpcapi__pb2.GetNodeDataStreamOutput.FromString,
        )


class IoTServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def DeepPing(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def CreateTask(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GetAllTasks(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GetUncompletedTasks(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def SetTaskCompleted(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def DeleteTask(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GetUncompletedTasksByHierarchy(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def SetTaskStatus(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def IngestNodeData(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GetNodeData(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GetNodeDataStream(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_IoTServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'DeepPing': grpc.unary_unary_rpc_method_handler(
          servicer.DeepPing,
          request_deserializer=grpcapi__pb2.PrimitiveVoid.FromString,
          response_serializer=grpcapi__pb2.PrimitiveString.SerializeToString,
      ),
      'CreateTask': grpc.unary_unary_rpc_method_handler(
          servicer.CreateTask,
          request_deserializer=grpcapi__pb2.InitialTaskDescription.FromString,
          response_serializer=grpcapi__pb2.PrimitiveString.SerializeToString,
      ),
      'GetAllTasks': grpc.unary_unary_rpc_method_handler(
          servicer.GetAllTasks,
          request_deserializer=grpcapi__pb2.PrimitiveString.FromString,
          response_serializer=grpcapi__pb2.TaskDescriptions.SerializeToString,
      ),
      'GetUncompletedTasks': grpc.unary_unary_rpc_method_handler(
          servicer.GetUncompletedTasks,
          request_deserializer=grpcapi__pb2.PrimitiveString.FromString,
          response_serializer=grpcapi__pb2.TaskDescriptions.SerializeToString,
      ),
      'SetTaskCompleted': grpc.unary_unary_rpc_method_handler(
          servicer.SetTaskCompleted,
          request_deserializer=grpcapi__pb2.TaskUser.FromString,
          response_serializer=grpcapi__pb2.PrimitiveVoid.SerializeToString,
      ),
      'DeleteTask': grpc.unary_unary_rpc_method_handler(
          servicer.DeleteTask,
          request_deserializer=grpcapi__pb2.TaskUser.FromString,
          response_serializer=grpcapi__pb2.PrimitiveVoid.SerializeToString,
      ),
      'GetUncompletedTasksByHierarchy': grpc.unary_unary_rpc_method_handler(
          servicer.GetUncompletedTasksByHierarchy,
          request_deserializer=grpcapi__pb2.PrimitiveString.FromString,
          response_serializer=grpcapi__pb2.TaskDescriptions.SerializeToString,
      ),
      'SetTaskStatus': grpc.unary_unary_rpc_method_handler(
          servicer.SetTaskStatus,
          request_deserializer=grpcapi__pb2.SetTaskStatusInput.FromString,
          response_serializer=grpcapi__pb2.PrimitiveVoid.SerializeToString,
      ),
      'IngestNodeData': grpc.unary_unary_rpc_method_handler(
          servicer.IngestNodeData,
          request_deserializer=grpcapi__pb2.IngestNodeDataInput.FromString,
          response_serializer=grpcapi__pb2.IngestNodeDataOutput.SerializeToString,
      ),
      'GetNodeData': grpc.unary_unary_rpc_method_handler(
          servicer.GetNodeData,
          request_deserializer=grpcapi__pb2.GetNodeDataInput.FromString,
          response_serializer=grpcapi__pb2.GetNodeDataOutput.SerializeToString,
      ),
      'GetNodeDataStream': grpc.unary_stream_rpc_method_handler(
          servicer.GetNodeDataStream,
          request_deserializer=grpcapi__pb2.GetNodeDataStreamInput.FromString,
          response_serializer=grpcapi__pb2.GetNodeDataStreamOutput.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'iotgrpcapi.IoT', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
