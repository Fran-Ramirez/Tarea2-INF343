import pika
import sys
import json
import threading
import time
from datetime import datetime


def mensaje(timestamp, fromID, toID, text):
        message = {
            'timestamp' : timestamp,
            'fromID' : fromID,
            'toID' : toID,
            'text' : text
        }
        return json.dumps(message)

class Client():
    
    def __init__(self,client_id):
        self.client_id = client_id
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host = 'localhost'))
        self.channel = self.connection.channel()
        #Seteo del nombre de la queue que recibe los mensajes
        self.channel.queue_declare(queue='rpc_queue')
        self.channel.exchange_declare('message_passing', exchange_type='direct')
        #Se publica la creacion del un nuevo cliente en el servidor
        self.channel.basic_publish(exchange='',
                            routing_key='rpc_queue',
                            body = mensaje(datetime.now().strftime("%H:%M:%S"),-1,-1,self.client_id),
                            properties=pika.BasicProperties(delivery_mode = 2)
                            )

    def send_message(self,text,toID):
        now = datetime.now().strftime("%H:%M:%S")
        toSend = mensaje(now,self.client_id,toID,text)
        #Enviar mensaje a la queue rpc_queue
        self.channel.basic_publish(exchange='',
                            routing_key='rpc_queue',
                            body = toSend,
                            properties=pika.BasicProperties(delivery_mode = 2)
                            )
    
    def callback(self, body):
        print("Dentro del callback")
        received = json.loads(body)
        if isinstance(received,list):
            if not received:
                print(received)
            else:    
                for item in received:
                    print(item)
        else:
            print('{} Recibido mensaje del cliente {}: {}'.format(received['timestamp'], received['fromID'], received['text']))

    def get_messages(self):
        result = self.channel.queue_declare(queue='', exclusive = True)
        callback_queue = result.method.queue
        self.channel.queue_bind(exchange = 'message_passing', queue = callback_queue, routing_key = str(self.client_id))
        self.channel.basic_consume(queue = callback_queue, on_message_callback = self.callback, auto_ack = True)
        print("Recibiendo mensajes en la cola %s" %str(self.client_id))
        self.channel.start_consuming()
        return

    def close_conection(self):
        self.channel.basic_publish(exchange='',
                            routing_key='rpc_queue',
                            body = mensaje(datetime.now().strftime("%H:%M:%S"),-2,-2,self.client_id),
                            properties=pika.BasicProperties(delivery_mode = 2)
                            )
        self.connection.close()
        return

    def get_messages_thread(self):
        print("Entrando al thread")
        self.get_messages_thread = threading.Thread(target=self.get_messages)
        self.get_messages_thread.start()
        return

def client_start():
    new_client_id = sys.argv[1]
    print("\n\nHas iniciado sesion en el servidor. Tu Id seleccionado es: {}".format(new_client_id))
    new_client = Client(new_client_id)
    new_client.get_messages_thread
    try:
        while True:
            #Usuario a enviarle el mensaje
            print("\n\n#############\n#############")
            print("Escriba el numero del usuario a enviarle el mensaje:")
            to_id = int(raw_input())
            if(to_id == int(new_client_id)):
                print("Te estas enviando un mensaje a ti, no es posible realizar esta operacion, intentalo nuevamente.")
                continue
            #Mensaje a enviar
            print("Escriba el mensaje que quiere enviar.\n** Para ver clientes conectados, escriba 'ver clientes conectados'\n** Para ver tus mensajes, escriba 'ver mensajes'\n** Para cerrar la conexion, escriba 'close'")
            text = raw_input()
            #Detectar tipo de mensaje
            if(text == "close"):
                new_client.close_conection()
                break
            if (text == "ver mensajes" or text == "ver clientes conectados"):
                new_client.send_message(text, -3)
                new_client.get_messages()
                continue
            new_client.send_message(text, to_id)
            print("Mensaje enviado de forma exitosa al usuario: %s" %to_id)
    except KeyboardInterrupt:
        new_client.close_conection()
        print("EXIT")
client_start()