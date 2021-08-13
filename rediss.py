import redis
import requests
import json
import time

r = redis.StrictRedis(host='127.0.0.1',port=6379,db=0)


def WriteProxy():#从代理池中获取代理IP
    try:
        p = requests.get("http://http.tiqu.letecs.com/getip3?num=100&type=2&pro=&city=0&yys=0&port=2&time=1&ts=0&ys=0&cs=0&lb=1&sb=0&pb=4&mr=1&regions=&gm=4")
    except:
        print('代理获取失败！')

    p = p.text
    p = json.loads(p)
    for i in range(0,49):
        ip = p['data'][i]['ip']
        port = p['data'][i]['port']
        vl = ip+":"+str(port)
        r.set(i,vl)
    print("写入完毕")
    time.sleep(3)


if __name__ == "__main__":
    while True:
        try:
            WriteProxy()
        except:
            print('代理获取失败！')
            pass

