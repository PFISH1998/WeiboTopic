from PySQL import PySQL
import time

def get_topic_time():
    p = PySQL()
    sql = 'SELECT * FROM weibo_search_history'
    r = p.exec_query(sql)
    for i in r:
        print(i[3] - i[2])
        time_on = i[3] - i[2]
        t = time.ctime(i[3])
        print(t)

get_topic_time()