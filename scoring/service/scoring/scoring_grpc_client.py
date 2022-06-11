import grpc
import scoring_service_pb2
import scoring_service_pb2_grpc

from datetime import datetime


def cilent_get_gew_graph(stub, time):
    graph_list = stub.GetNewGraph(time)
    print(graph_list)

def client_generate_new_graph(stub, floorplan):
    graph = stub.GenerateGraph(floorplan)
    print(graph)

def client_generate_score(stub, graph):
    scores = stub.GenerateScore(graph)
    print("score_commonarea: ", scores.score_commonarea)
    print("score_function: ", scores.score_functional)
    print("score_corridor: ", scores.corridor)
    print("connectivity score public: ", scores.score_connectivity_private)
    print("connectivity score private: ", scores.score_connectivity_public)

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = scoring_service_pb2_grpc.ScoringStub(channel)
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        floorplan_list = cilent_get_gew_graph(stub, current_time)
        for floorplan in floorplan_list:
            graph = client_generate_new_graph(stub,floorplan)
            client_generate_score(stub, graph)