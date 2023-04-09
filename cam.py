import cv2
import pickle
import socket

def send_cam_image(host, port):
    # 打开默认摄像头
    cap = cv2.VideoCapture(0)
    # 读取视频流中的一帧
    ret, frame = cap.read()
    # 显示当前帧
    # cv2.imshow('frame', frame)
    #cv2.imwrite('D:/img.jpg', frame)
    img_data = pickle.dumps(frame)

    # 创建socket对象
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 连接服务器
    client_socket.connect((host, port))

    # 发送文件长度
    file_size = len(img_data)
    client_socket.send(str(file_size).encode())

    # 发送文件内容
    client_socket.sendall(img_data)

    # 关闭socket连接
    client_socket.close()

    # 释放摄像头资源
    cap.release()
    # 关闭所有窗口
    cv2.destroyAllWindows()
    
def get_cam_image(host, port):

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

    frame = pickle.loads(content)

    # 保存文件
    cv2.imwrite('img.jpg', frame)
    # 关闭socket连接
    client_socket.close()
    server_socket.close()


if __name__ == '__main__':
    get_cam_image()
