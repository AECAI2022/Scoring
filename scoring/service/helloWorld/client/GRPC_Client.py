from __future__ import print_function

import logging

import grpc
import helloworld_pb2
import helloworld_pb2_grpc


def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.

    # select which address the channel will use, right now is ('localhost:50051')
    with grpc.insecure_channel('localhost:50051') as channel:
        # select which stub to use for the service via the channel selected
        stub = helloworld_pb2_grpc.GreeterStub(channel)
        # giving the variable 'name' to the server via stub
        response = stub.SayHello(helloworld_pb2.HelloRequest(name='you'))
    # response in the print message
    print("Greeter client received: " + response.message)



if __name__ == '__main__':
    logging.basicConfig()
    run()