import json
from socket import *
import datetime

serverHost = '127.0.0.1'
serverPort = 8015

# TCP server socket 생성
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind((serverHost, serverPort))

# 서버 요청 받기 시작
serverSocket.listen()
print('The server is running')

while True:
    # 요청오면 connection 만들어주기
    connectionSocket, addr = serverSocket.accept()

    try:
        # 수신
        message = connectionSocket.recv(65535).decode()
        request_headers = message.split()

        # user의 request가 'GET'일 경우
        if request_headers[2] == 'HTTP/1.1' and request_headers[0] == 'GET':
            f = open('post.json', 'rt', encoding='utf-8')
            dataArray = json.load(f)
            posts_id = [] # 게시글의 id를 저장하는 배열
            for data in dataArray:
                posts_id.append(data.get("id"))

            if int(request_headers[1]) in posts_id: # 데이터 접근에 성공한 경우
                body_content = json.dumps(dataArray[int(request_headers[1])-1])
                f.close()
                request_time = datetime.datetime.now().strftime("%c")
                sendingData = request_headers[2] + ' 200 OK\n' + 'Content-Type: application/json\n' + 'Context-length: '+ str(len(body_content)) + '\n' + 'Date: ' + request_time + '\n\n' + body_content
                connectionSocket.send(sendingData.encode('utf-8'))

            else: # 없는 데이터 id에 접근한 경우
                f.close()
                request_time = datetime.datetime.now().strftime("%c")
                sendingData = request_headers[2] + ' 404 Not found\n' + 'Content-Type: application/json\n' + 'Date: ' + request_time
                connectionSocket.send(sendingData.encode('utf-8'))

        # user의 request가 'HEAD'일 경우
        elif request_headers[2] == 'HTTP/1.1' and request_headers[0] == 'HEAD':
            f = open('post.json', 'rt', encoding='utf-8')
            dataArray = json.load(f)
            posts_id = [] # 게시글의 id를 저장하는 배열
            for data in dataArray:
                posts_id.append(data.get("id"))

            if int(request_headers[1]) in posts_id: # 데이터 접근에 성공한 경우
                body_content = json.dumps(dataArray[int(request_headers[1]) - 1])
                f.close()
                request_time = datetime.datetime.now().strftime("%c")
                sendingData = request_headers[2] + ' 200 OK\n' + 'Content-Type: application/json\n' + 'Context-length: ' + str(len(body_content)) + '\n' + 'Date: ' + request_time
                connectionSocket.send(sendingData.encode('utf-8'))

            else: # 없는 데이터 id에 접근한 경우
                f.close()
                request_time = datetime.datetime.now().strftime("%c")
                sendingData = request_headers[2] + ' 404 Not found\n' + 'Content-Type: application/json\n' + 'Date: ' + request_time
                connectionSocket.send(sendingData.encode('utf-8'))

        # user의 request가 'POST'일 경우
        elif request_headers[3] == 'HTTP/1.1' and request_headers[0] == 'POST':
            f = open('post.json', 'rt', encoding='utf-8')
            dataArray = json.load(f)
            # client로부터 받은 데이터 추가
            dataArray.append({
                "id": len(dataArray) + 1,
                "title": request_headers[1],
                "content": request_headers[2]
            })
            f.close()

            # 'post.json' 파일 편집
            with open('post.json', 'wt', encoding='utf-8') as f:
                json.dump(dataArray, f, indent=4)

            request_time = datetime.datetime.now().strftime("%c")
            sendingData = request_headers[3] + ' 200 OK\n' + 'Content-Type: application/json\n' + 'Date: ' + request_time
            connectionSocket.send(sendingData.encode('utf-8'))

        # user의 request가 'PUT'일 경우
        elif request_headers[3] == 'HTTP/1.1' and request_headers[0] == 'PUT':
            f = open('post.json', 'rt', encoding='utf-8')
            dataArray = json.load(f)
            posts_id = []
            for data in dataArray:
                posts_id.append(data.get("id"))

            if int(request_headers[1]) in posts_id: # 데이터 접근에 성공한 경우
                for data in dataArray:
                    if data['id'] == int(request_headers[1]): # client로부터 받은 데이터로 기존 데이터 수정
                        data['content'] = request_headers[2]
                f.close()

                # 'post.json' 파일 편집
                with open('post.json', 'wt', encoding='utf-8') as f:
                    json.dump(dataArray, f, indent=4)

                request_time = datetime.datetime.now().strftime("%c")
                sendingData = request_headers[3] + ' 200 OK\n' + 'Content-Type: application/json\n' + 'Date: ' + request_time
                connectionSocket.send(sendingData.encode('utf-8'))

            else: # 없는 데이터 id에 접근한 경우
                f.close()
                request_time = datetime.datetime.now().strftime("%c")
                sendingData = request_headers[3] + ' 404 Not found\n' + 'Content-Type: application/json\n' + 'Date: ' + request_time
                connectionSocket.send(sendingData.encode('utf-8'))

        # user의 request가 잘못된 request일 경우
        else:
            request_time = datetime.datetime.now().strftime("%c")
            sendingData = request_headers[1] + ' 400 Bad Request\n' + 'Content-Type: application/json\n' + 'Date: ' + request_time
            connectionSocket.send(sendingData.encode('utf-8'))

    except ConnectionResetError as e:
        print('Disconnected by' + addr)
        break

connectionSocket.close()
serverSocket.close()