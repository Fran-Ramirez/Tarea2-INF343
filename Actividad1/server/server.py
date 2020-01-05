from concurrent import futures
from datetime import datetime
import logging
import grpc

import chat_pb2 as chat_pb2
import chat_pb2_grpc as chat_pb2_grpc

class Chat():
    def __init__(self):
        self.listChats =[]
    def sendmsge(self, request: chat_pb2.MessageRequest, context):
        f=open("log.txt", "a")
        name = request.id.split("-")[1]
        sec = request.timestamp.seconds
        dt = datetime.fromtimestamp(sec)
        datatime = dt.strftime("%m/%d/%Y, %H:%M:%S")
        f.write("[{} - {} ] {}\n".format(datatime, name, request.message))
        f.close()
        self.listChats.append(request)
        return chat_pb2.MessageResponse()
    def Channel(self, request, context):
        aux=0
        while True:
            while(len(self.listChats)>aux):
                n = self.listChats[aux]
                aux += 1
                yield n

class Users():
    def __init__(self):
        self.usersList = []
    def JoinChat(self, request, context):
        response = chat_pb2.response()
        if request.userId in self.usersList:
            response.opt = False    
            return response
        response.opt = True
        self.usersList.append(request.userId)

        return response
    def getUsers(self, request, context):
        user_list = chat_pb2.UserResponse()
        userMsge = []
        for user in self.usersList:
            uMsge = chat_pb2.UserRequest()
            uMsge.userId = user
            userMsge.append(uMsge)
        user_list.userlist.extend(userMsge)
        return user_list
    def Disconnect(self, request, context):
        username = request.userId
        self.usersList.remove(username)

        return chat_pb2.MessageResponse()
    
class msgeServer():
    def __init__(self):
        self.user_messages = {}
    def MsgeSave(self, request, context):
        name = request.id.split("-")[1]
        if name not in self.user_messages:
            self.user_messages[name] = [request]
        else: 
            self.user_messages[name].append(request)
        return chat_pb2.MessageResponse()
    def AllMsges(self, request, context):
        name = request.userId
        uMsge = chat_pb2.UserMsje()

        if name not in self.user_messages:
            return uMsge
        uMsge.msges.extend(self.uMsge[name])
        return uMsge
        

def servidor():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    chat_pb2_grpc.add_ContectionServerServicer_to_server(Chat(), server)
    chat_pb2_grpc.add_UserServicer_to_server(Users(),server)
    chat_pb2_grpc.add_ser_messageServicer_to_server(msgeServer(),server)
    server.add_insecure_port('[::]50051')
    server.start()
    server.wait_for_termination

if __name__ == '__main__':
    logging.basicConfig()
    servidor()