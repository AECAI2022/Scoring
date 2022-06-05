from concurrent import futures
import logging

import grpc
import helloworld_pb2
import helloworld_pb2_grpc

# using the servicer in the serve
class Greeter(helloworld_pb2_grpc.GreeterServicer):

    # using the replay function in the servicer with the variables
    def SayHello(self, request, context):
        return helloworld_pb2.HelloReply(message='Hello, %s!' % request.name)

# Define the server
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    # Adding the servicer
    helloworld_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    # Adding the address for the stub and port
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()