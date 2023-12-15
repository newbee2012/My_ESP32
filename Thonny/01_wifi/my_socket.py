from socket import *

# 1. 创建udp套接字
udp_socket = socket(AF_INET, SOCK_DGRAM)

# 2. 准备接收方的地址
dest_addr = ('192.168.31.243', 8080)

# 3. 从键盘获取数据
send_data = "hello world"

# 4. 发送数据到指定的电脑上
udp_socket.sendto(send_data.encode('utf-8'), dest_addr)


# 5. 关闭套接字
udp_socket.close()