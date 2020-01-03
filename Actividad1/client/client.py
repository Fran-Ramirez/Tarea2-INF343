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
        self.stub = chat_pb2_grpc.ContectionServerStub(channel)
        self.msge_stub = chat_pb2_grpc.ser_messageStub(channel)
        req = chat_pb2.User()

        ## Agregar usuarios
        aux = False
        while aux == False:
            name = input("Ingrese su nombre: ")
            req.user_id = name
            response = self.user_stub.addUser(req)

            if response.opt:
                print("Usuario agregado exitosamente")
                self.username = name ### self.name = name
                aux = True
            else:
                print("El usuario no existe")
        threading.Thread(target=self.get_msgs, daemon=True)).start()
    
    def sendMsg(self, msge):
        if msge != '':
            ts = Timestamp()
            ts.GetCurrentTime() #tiempo actual
            IDmsge = str(ts.seconds)+"-"+self.name
            mensaje = chat_pb2.MessageRequest()
            mensaje.id = IDmsge
            mensaje.time.seconds = ts.seconds
            mensaje.message = msge

            self.stub.SendMsg(mensaje)
            self.msge_stub.savemsge(mensaje)     
    def getUsers(self):
        print("Usuarios en linea: ")
        users = self.users_stub.getListUser(chat_pb2.MessageResponse())
        for user in users.users:
            print(user.user_id)
    def getMsges(self):
        for MessageRequest in self.stub.CreateChannel(chat_pb2.MessageResponse()):
            msge = MessageRequest
            name = msge.id.split("-")[1]
            seconds = msge.timestamp(seconds)
            data = datatime.fromtimestamp(seconds)
            date_time = data.strftime("%m/%d/%Y, %H:%M:%S")
            print("[{} - {} ] {}".format(date_time, name, msge.message))
    def getMsgForUsers(self):
        user = chat_pb2.UserRequest()
        user.userId = self.name
        Umsge = self.msge_stub.getMsges(UserRequest)
        print("Los mensajes enviados pro"+str(self.name)+" son: ")
        for msges in Umsge.msges:
            username = msges.id.split("-")[1]
            seconds = message.timestamp.seconds
            dt_object = datetime.fromtimestamp(seconds)
            date_time = dt_object.strftime("%m/%d/%Y, %H:%M:%S")
            print("[{} - {} ] {}".format(date_time, username, message.message))
    def closeConection(self):
        user = chat_pb2.User()
        user.userId = self.name
        self.users_stub.Disconnect(user)

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
    

        
