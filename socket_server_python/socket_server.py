import os
import socket
from datetime import datetime

class SocketServer:
    def __init__(self):
        self.bufsize = 1024
        with open('./response.bin', 'rb') as file:
            self.RESPONSE = file.read()
        
        self.DIR_PATH='./request'
        self.createDir(self.DIR_PATH)
    
    def createDir(self, path):
        try:
            if not os.path.exists(path):
                os.makedirs(path)
        except OSError:
            print("Error. Failed to create the directory.")

    def run(self, ip, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((ip, port))
        self.sock.listen(10)
        print("Start the socket server...")
        print("\"Ctrl+C\" for stopping the server!\r\n")

        try:
            while True:
                clnt_sock, req_addr = self.sock.accept()
                clnt_sock.settimeout(3)
                print("Request message...\r\n")        

                now_time = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
                with open(f"{self.DIR_PATH}/{now_time}.bin", 'wb') as file:
                    boundary_str = b""
                    while True:
                        try:
                            req_data = clnt_sock.recv(self.bufsize)
                            file.write(req_data)

                            if b"Content-Type: " in req_data:
                                content_type = req_data.split(b"Content-Type: ")[1].split(b';')[0]
                                if content_type == b"multipart/form-data":
                                    boundary_str = b"--" + req_data.split(b"boundary=")[1].split(b"\r\n")[0]

                        except socket.timeout:
                            break
                
                with open(f"{self.DIR_PATH}/{now_time}.bin", 'rb') as file:
                    full_data = file.read()

                if boundary_str != b"":
                    full_data = full_data.split(boundary_str)
                    # print(full_data)

                    for ele in full_data:
                        if b"Content-Disposition: form-data; name=\"image\"" in ele:
                            filename = ele.split(b"filename=")[1].split(b"\"")[1]
                            
                            with open(f"./{filename.decode('utf-8')}", 'wb') as file:
                                file.write(ele.split(b"\r\n\r\n")[1])
                    

                clnt_sock.sendall(self.RESPONSE)
                print("\r\nSent response message...\r\n")
                clnt_sock.close()
        except KeyboardInterrupt:
            print("\r\nStop the server...")
        
        self.sock.close()

if __name__ == "__main__":
    server = SocketServer()
    server.run("127.0.0.1", 8000)