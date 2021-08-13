import socket
import threading
import random
import redis

r = redis.StrictRedis(host='127.0.0.1',port=6379,db=0)

timeout = 300
nodatatime = 5

def getPX(a):
    px = str(r.get(a))
    px = px.strip('b\'')
    ip = px.split(":")[0]
    port = px.split(":")[1]
    port = int(port)
    return ip,port

def targetToClient(conn,toPX):
    global timeout
    global nodatatime
    i = 0
    j = 0
    while i < timeout:
        try:
            data = toPX.recv(1024)
            if not data:
                if j > nodatatime:
                    conn.close()
                    toPX.close()
                    return
                j += 1
        except:
            if j > nodatatime:
                conn.close()
                toPX.close()
                return
            j += 1
            #print("TC【get data from px error】")
        try:
            conn.sendall(data)
        except:
            #print("TC【send data to client error】")
            pass

def clientToTarget(conn,toPX):
    global timeout
    global nodatatime
    j = 0
    i = 0
    while i < timeout:
        try:
            data = conn.recv(1024)
            if not data:
                if j > nodatatime:
                    conn.close()
                    toPX.close()
                    return
                j += 1
        except:
            if j > nodatatime:
                conn.close()
                toPX.close()
                print("close")
                return
            j += 1
            #print("CT【get data from client error】")
        try:
            toPX.sendall(data)
        except:
            print("CT【send data to px error】")
        i += 1


def AConnectFromClient(conn,ip,port):
    print("熊桥建立")
    pxip = ip
    pxport = port
    try:
        toPX = socket.socket()
        toPX.connect((pxip,pxport))
    except:
        print("connect px error")
    threading.Thread(target=clientToTarget,args=(conn,toPX)).start()
    threading.Thread(target=targetToClient,args=(conn,toPX)).start()



if __name__ == "__main__":
    sever = socket.socket()
    host = "127.0.0.1"
    port = 3080
    sever.bind((host,port))
    sever.listen(20)
    print("欢迎使用熊儿子代理！")
    while True:
        try:
            conn,addr = sever.accept()
            a = random.randint(0, 49)
            ip, port = getPX(a)
            threading.Thread(target=AConnectFromClient,args=(conn,ip,port)).start()
        except:
            print("垃圾熊某，代理失败！")
