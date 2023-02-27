from ast import Try
import socket
import sys
import traceback



class MayaClient(object):

    BUFFER_SIZE = 4096
    PORT = 20181

    def __init__(self) -> None:
        self.port = MayaClient.PORT
        self.maya_socket = None

    def connect(self, port=-1):
        if port >= 0:
            self.port = port
        try:
            self.maya_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.maya_socket.connect(("localhost", self.port))

        except:
            traceback.print_exc()
            return False
        return True


    def disconnect(self):
        try:
            self.maya_socket.close()
        except:
            traceback.print_exc()
            return False
        return True


    def send(self, cmd):
        try:
            self.maya_socket.sendall(cmd.encode())
        except:
            traceback.print_exc()
            return None
        return self.recv()

    def recv(self):
        try:
            data = self.maya_socket.recv(MayaClient.BUFFER_SIZE)
        except:
            traceback.print_exc()
            return None
        return data.decode().replace('\x00', '')
    
    def echo(self, text):
        cmd = "eval(\"'{0}'\")".format(text)
        return self.send(cmd)

if __name__ == "__main__":
    maya_client = MayaClient()

    if maya_client.connect():
        print("Connect successfully")

        a = maya_client.echo("hello world")
        print(a)
        
        # print("Echo:{0}".format(maya_client.echo("Hello World")))

        if maya_client.disconnect():
            print("Disconnect successfully")
            
    
    else:
        print("Failed to connect")
