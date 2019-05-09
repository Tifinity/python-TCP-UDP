import socket
import os
import struct
import pickle

server_ip = '172.18.61.253'
server_port = 5400
filepath = os.path.dirname(os.path.abspath(__file__))

def get(file_name, client, server):
    file_path = os.path.join(filepath, file_name)
    if os.path.isfile(file_path):
        header = {
            'file_name': file_name,
            'file_size': os.path.getsize(file_path)
        }
        header_bytes = pickle.dumps(header)
        server.sendto(struct.pack('i', len(header_bytes)), client)
        server.sendto(header_bytes, client)
        with open(file_path, 'rb') as f:
            for line in f:
                server.sendto(line, client)
    else:
        server.sendto(struct.pack('i', 0), client)

def run():
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind((server_ip, server_port))
    print('Server start on')
    print('-> ip: %s port: %d' %(server_ip, server_port))
    while True:
        try:
            data, client = server.recvfrom(1024)
            data = data.decode('utf-8')
            print('Send %s to %s' % (data, client[0]))
            get(data, client, server)
        except ConnectionResetError:
            break
    server.close()

if __name__ == '__main__':
    run()