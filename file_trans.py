import socket

def recv_file_server(host, port):
    # 创建socket对象
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 绑定端口号
    server_socket.bind((host, port))

    # 开始监听
    server_socket.listen()

    # 等待客户端连接
    client_socket, addr = server_socket.accept()

    # 接收文件长度
    file_size = int(client_socket.recv(1024).decode())

    # 接收文件内容
    content = b""
    while len(content) < file_size:
        data = client_socket.recv(1024)
        content += data

    # 保存文件
    with open("RECEIVE", "wb") as f:
        f.write(content)
    print("file saved to current location as RECEIVE")
    # 关闭socket连接
    client_socket.close()
    server_socket.close()

def send_file_client(filename, host, port):
    # 创建socket对象
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 连接服务器
    client_socket.connect((host, port))

    # 打开文件并发送
    with open(filename, "rb") as f:
        # 读取文件内容
        content = f.read()

        # 发送文件长度
        file_size = len(content)
        client_socket.send(str(file_size).encode())

        # 发送文件内容
        client_socket.sendall(content)

    # 关闭socket连接
    client_socket.close()

# 测试
'''
if __name__ == "__main__":
    send_file_client("c:\\test.txt", "localhost", 8000)
'''

# 测试
'''
if __name__ == "__main__":
    recv_file_server("localhost", 8000)
'''