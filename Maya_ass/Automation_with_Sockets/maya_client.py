import socket
import sys

BUFER_SIZE  = 4096
 
port = 20181

if len(sys.argv) > 1:
    port = sys.argv[1]

maya_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
maya_socket.connect(("localhost", port))

# maya_socket.sendall("cmds.file(new=True, force=True)".encode())
# data = maya_socket.recv(BUFER_SIZE)

# maya_socket.sendall("cmds.polySphere()".encode())
# data = maya_socket.recv(BUFER_SIZE)
# result = eval(data.decode().replace('\x00', ''))
# print(result[0])


maya_socket.close()