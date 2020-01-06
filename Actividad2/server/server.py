import pika
import sys
import json
import time

class Server():

    def __init__(self):
        self.clientes = []
        self.mensajes_id = []
        self.msgID = 0
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host = 'localhost'))
        self.channel = self.connection.channel()
        self.channel.basic_qos(prefetch_count=1)
        self.channel.queue_declare(queue='rpc_queue')
        self.channel.exchange_declare(exchange='message_passing', exchange_type='direct')

    def get_messages(self, client_id):
        messages = []
        for not_json_msg in self.mensajes_id:
            if (not_json_msg['fromID'] == client_id):
                messages.append(not_json_msg)
        return json.dumps(messages)

    def handle_message(self,ch, method, properties, body):
        received = json.loads(body)
        print(received)
        ch.basic_ack(delivery_tag = method.delivery_tag)
        #Se recibe mensaje de creacion de nuevo usuario
        if(received['fromID'] == -1):
            try:
                print("Agregando cliente a la lista")
                print("El Cliente %s ha iniciado sesion." %(received['text']))
                self.clientes.append(received['text'])
                print("Clientes activos %s" %self.clientes)
                return
            except:
                return
        #Cliente cierra sesion
        if(received['fromID'] == -2):
            try:
                print("Eliminando cliente de la lista")
                print("El Cliente %s ha cerrado sesion." %(received['text']))
                #del(self.clientes(received['text']))
                self.clientes.remove(received['text'])
                print("Clientes activos {}".format(self.clientes))
                return
            except:
                return
        #Cliente pide ver mensajes
        if(received['text']) == 'ver mensajes':
            try:
                print("Viendo mensajes")
                print(json.dumps(self.clientes))
                ch.basic_publish(exchange='message_passing',
                                routing_key=str(received['fromID']),
                                body = json.dumps(self.clientes)
                                )
                print("mensaje enviado a: %s" %str(received['fromID']))
                return 
            except:
                return 
        #Cliente pide ver clientes conectados
        if(received['text']) == "ver clientes conectados":
            print("Viendo clientes conectados")
            print(json.dumps(self.clientes))
            ch.basic_publish(exchange='message_passing',
                            routing_key=str(received['fromID']),
                            body = json.dumps(self.clientes),
                            properties=pika.BasicProperties(delivery_mode = 2)
                            )
            return  
        log = "{} Cliente {} envia '{}' al cliente {}".format(received['timestamp'],received['fromID'],received['text'], received['toID'])
        print(log)        
        if(str(received['toID']) not in self.clientes):
            print("Cliente %s no ha iniciado sesion, no se envio el mensaje" %str(received['toID']))
            return
        to_send = received
        to_send['msgID'] = self.msgID
        self.msgID += 1
        self.mensajes_id.append(to_send)
        ch.basic_publish(exchange='message_passing',
                        routing_key=str(to_send['toID']),
                        body = json.dumps(to_send),
                        )
        with open('log.txt','a') as file:
            file.write(log + '\n')

    def start_server(self):
        print("Starting server")
        self.channel.basic_consume(queue = 'rpc_queue', on_message_callback = self.handle_message)
        self.channel.start_consuming()

servidor = Server()
servidor.start_server()