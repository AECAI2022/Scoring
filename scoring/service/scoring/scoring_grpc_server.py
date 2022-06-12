import logging
import pymysql
from networkx.readwrite import json_graph
from concurrent import futures

import class_floorplan_copy
import scoring2

import grpc
import scoring_service_pb2
import scoring_service_pb2_grpc
from google.protobuf.json_format import MessageToDict, ParseDict


# # retrieve data from database
# def DataRetrieval():
#     '''#configuration values
#     endpoint = 'building-info.clvzv6ux6jdz.us-west-1.rds.amazonaws.com'
#     username = 'JZNYC'
#     password = '58290273'
#     database_name = 'buildingInfo' '''
#
#
#     # configuration values
#     endpoint = 'building-info.clvzv6ux6jdz.us-west-1.rds.amazonaws.com'
#     database_name = 'buildingInfo'
#     username = str(input('PLEASE INPUT USERNAME: '))
#     password = str(input('PLEASE INPUT PASSWORD: '))
#
#     # connection
#     connection = pymysql.connect(host=endpoint, user=username, passwd=password, db=database_name)
#     update_list = []
#
#     with connection:
#         with connection.cursor() as cursor:
#             sql = "SELECT 'houseID', 'update_status' FROM 'HouseInfo' WHERE 'update_status'=TRUE"
#             cursor.execute(sql)
#             rows = cursor.fetchall()
#             for row in rows:
#                 update_list.append(row[0])
#     return update_list



class ScoringServer(scoring_service_pb2_grpc.ScoringServicer):
    def GetNewGraph(self, request, context):
        '''#configuration values
        endpoint = 'building-info.clvzv6ux6jdz.us-west-1.rds.amazonaws.com'
        username = 'JZNYC'
        password = '58290273'
        database_name = 'buildingInfo' '''

        #trigger
        hour = request.t[0:2]
        min = request.t[3:5]
        sec = request.t[6:8]



        # configuration values
        endpoint = 'building-info.clvzv6ux6jdz.us-west-1.rds.amazonaws.com'
        database_name = 'buildingInfo'
        username = str(input('PLEASE INPUT USERNAME: '))
        password = str(input('PLEASE INPUT PASSWORD: '))

        # connection
        if hour == '00' and min == '00' and sec == '00':
            connection = pymysql.connect(host=endpoint, user=username, passwd=password, db=database_name)


            with connection:
                with connection.cursor() as cursor:
                    sql = "SELECT 'houseID', 'update_status' FROM 'HouseInfo' WHERE 'update_status'=TRUE"
                    cursor.execute(sql)
                    rows = cursor.fetchall()
                    for row in rows:
                        yield(row[0])

    # request is a Floorplan message
    def GenerateGraph(self, request, context):
        floorplan_id = request.id
        figure_path = request.floorplan_path
        floorplan = class_floorplan_copy.Floorplan(figure_path)
        graph = floorplan.generate_connectivity_graph()
        graph = json_graph.node_link_data(graph)
        graph_message = ParseDict(graph, scoring_service_pb2.Graph())
        return graph_message

    # request is a dict_like message
    def GenerateScore(self, request, context):
        request_dict = MessageToDict(request)
        rooms = scoring2.Rooms.create_from_json(request_dict)
        score_common_area = rooms.get_score_commonarea()
        score_functional = rooms.get_score_function()
        score_corridor = rooms.get_score_corridor()
        score_connectivity_private = rooms.get_score_connectivity_private()
        score_connectivity_public = rooms.get_score_connectivity_public()


        return  scoring_service_pb2.Scores(score_commonarea = score_common_area,
                                           score_functional=score_functional,
                                           score_corridor=score_corridor,
                                           score_connectivity_private=score_connectivity_private,
                                           score_connectivity_public=score_connectivity_public)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    scoring_service_pb2_grpc.add_ScoringServicer_to_server(ScoringServer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    logging.basicConfig()
    serve()








