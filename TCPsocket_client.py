from socket import *

serverHost = '127.0.0.1'
serverPort = 8015

def create_socket_and_send_message(request_message):
    # 클라이언트 소켓 만들기
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverHost, serverPort))
    clientSocket.send(request_message.encode('utf-8'))

    # 응답 확인
    receive_message = clientSocket.recv(65535)
    print(receive_message.decode())

    clientSocket.close()

while True:
    clients_request = input("request: ")
    if clients_request in ["GET", "HEAD"]: # user의 request가 'GET' 또는 'HEAD'일 경우
        posts_id = input("id number: ")
        request_message = clients_request + ' ' + posts_id + ' HTTP/1.1\r\n'

    elif clients_request == "POST": # user의 request가 'POST'일 경우
        posts_title = input("제목: ")
        posts_content = input("내용: ")
        request_message = clients_request + ' ' + posts_title + ' ' + posts_content + ' HTTP/1.1\r\n'

    elif clients_request == "PUT": # user의 request가 'PUT'일 경우
        posts_id = input("id number: ")
        posts_content = input("내용 변경: ")
        request_message = clients_request + ' ' + posts_id + ' ' + posts_content + ' HTTP/1.1\r\n'

    else: # user의 request가 잘못된 request일 경우
        request_message = clients_request + ' HTTP/1.1\r\n'

    request_message += 'Host: 127.0.0.1:12000\r\n'
    request_message += 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.35 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.35\r\n'
    request_message += 'Connection: Keep-Alive\n\n'
    create_socket_and_send_message(request_message)
