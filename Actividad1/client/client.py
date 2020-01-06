from datetime import datetime
from google.protobuf.timestamp_pb2 import Timestamp
import logging
import grpc
import threading

import chat_pb2 as chat_pb2
import chat_pb2_grpc as chat_pb2_grpc

class Client:


    def __init__ (self):
        channel = grpc.insecure_channel('server:50051')
        self.user_stub = chat_pb2_grpc.UserStub(channel)
        req = chat_pb2.UserRequest()

        ## Agregar usuarios
        aux = False
        while aux == False:
            name = input("Ingrese su nombre: ")
            req.userId = name
            response = self.user_stub.addUser(req)

            if response.opt:
                print("Usuario agregado exitosamente")
                self.username = name ### self.name = name
                aux = True
            else:
                print("El usuario no existe")
        self.stub = chat_pb2_grpc.ContectionServerStub(channel)
        self.msge_stub = chat_pb2_grpc.ser_messageStub(channel)
        threading.Thread(target=self.getMsges, daemon=True).start()
    
    def sendMsg(self, msge):
        if msge != '':
            ts = Timestamp()
            ts.GetCurrentTime() #tiempo actual
            IDmsge = str(ts.seconds)+"-"+self.username
            mensaje = chat_pb2.MessageRequest()
            mensaje.id = IDmsge
            mensaje.timestamp.seconds = ts.seconds
            mensaje.message = msge

            self.stub.SendMsg(mensaje)
            self.msge_stub.savemsge(mensaje)     
    def getUsers(self):
        print("Usuarios en linea: ")
        users = self.user_stub.getListUser(chat_pb2.MessageResponse())
        for user in users.users:
            print(user.user_id)
    def getMsges(self):
        for MessageRequest in self.stub.CreateChannel(chat_pb2.MessageResponse()):
            msge = MessageRequest
            name = msge.id.split("-")[1]
            seconds = msge.timestamp.seconds
            data = datetime.fromtimestamp(seconds)
            date_time = data.strftime("%m/%d/%Y, %H:%M:%S")
            print("[{} - {} ] {}".format(date_time, name, msge.message))
    def getMsgForUsers(self):
        user = chat_pb2.UserRequest()
        user.userId = self.username
        Umsge = self.msge_stub.getMsges(user)
        print("Los mensajes enviados por "+str(self.username)+" son: ")
        for msges in Umsge.msges:
            username = msges.id.split("-")[1]
            seconds = msges.timestamp.seconds
            dt_object = datetime.fromtimestamp(seconds)
            date_time = dt_object.strftime("%m/%d/%Y, %H:%M:%S")
            print("[{} - {} ] {}".format(date_time, username, message.message))
    def closeConection(self):
        user = chat_pb2.UserRequest()
        user.userId = self.username
        self.user_stub.closeConection(user)

if __name__=='__main__':
    logging.basicConfig()
    client = Client()

    while True:
        userInput = input()
        if userInput == "send":
            mensaje = input
            client.sendMsg(mensaje)
        elif userInput == "userList":
            client.getUsers()
        elif userInput == "userMsges":
            client.getMsgForUsers()
        elif userInput == "exit":
            client.closeConection()
            break
        else:
            print("comando invalido")
    

        
