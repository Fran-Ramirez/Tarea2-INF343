# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

import chat_pb2 as chat__pb2


class ContectionStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.SendMsg = channel.unary_unary(
        '/grpc.Contection/SendMsg',
        request_serializer=chat__pb2.Request.SerializeToString,
        response_deserializer=chat__pb2.Msje.FromString,
        )


class ContectionServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def SendMsg(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_ContectionServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'SendMsg': grpc.unary_unary_rpc_method_handler(
          servicer.SendMsg,
          request_deserializer=chat__pb2.Request.FromString,
          response_serializer=chat__pb2.Msje.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'grpc.Contection', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
