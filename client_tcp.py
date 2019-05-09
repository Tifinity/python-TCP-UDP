import socket
import struct
import pickle
import os

server_ip = '172.18.61.253'
server_port = 5400
filepath = os.path.dirname(os.path.abspath(__file__))

def get(client):
    obj = client.recv(4)
    header_size = struct.unpack('i', obj)[0]
    if header_size == 0:
        print('我觉得你可能打错了文件名 |w ·)')
    else:
        header_types = client.recv(header_size)
        header = pickle.loads(header_types)
        print(header)
        file_size = header['file_size']
        file_name = header['file_name']
        with open('%s\\%s' % (filepath, file_name), 'wb') as f:
            recv_size = 0
            while recv_size < file_size:
                res = client.recv(1024)
                f.write(res)
                recv_size += len(res)
                print('一共有这么大：%s B 你已经下载了：%s B' % (file_size, recv_size))
            print('下完啦 (0 V 0)')

def run():
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client.connect((server_ip, server_port))
    while True:
        msg = input("你想下载的文件叫什么名字呢: ").strip()
        client.send(msg.encode('utf-8'))
        get(client)
    client.close()

if __name__ == '__main__':
    run()
