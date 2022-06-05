import grpc

import helloworld_pb2 as helloworld__pb2

# Define the stub for the service
class GreeterStub(object):
  """The greeting service definition.
  """

  def __init__(self, channel):
    """Constructor.
    Args:
      channel: A grpc.Channel.
    """
    # Using unary RPC:
    # Once the client calls a stub method, server notified the RPC
    # Either the server send back its initial metadata or waite for the request message
    # Then server will create response once receiving the request message
    self.SayHello = channel.unary_unary(
        '/helloworld.Greeter/SayHello',
        request_serializer=helloworld__pb2.HelloRequest.SerializeToString,
        response_deserializer=helloworld__pb2.HelloReply.FromString,
        )

# Define the Servicer class
class GreeterServicer(object):
  """The greeting service definition.
  """

  # Define the function in the Servicer
  def SayHello(self, request, context):
    """Sends a greeting
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

# Adding this Servicer into the server
def add_GreeterServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'SayHello': grpc.unary_unary_rpc_method_handler(
          servicer.SayHello,
          request_deserializer=helloworld__pb2.HelloRequest.FromString,
          response_serializer=helloworld__pb2.HelloReply.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'helloworld.Greeter', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))