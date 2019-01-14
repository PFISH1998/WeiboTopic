from datetime import datetime

from PySQL import PySQL
import time
import matplotlib.pyplot as plt


def get_weibo_data(search_id=None):
    mysql = PySQL()
    sql = 'SELECT search_time, hot FROM weibo_hot_history WHERE search_id = {} ORDER BY search_time ASC'.format(search_id)
    result = mysql.exec_query(sql)
    t_sql = 'SELECT TITLE FROM weibo_hot WHERE id={}'.format(search_id)
    title = mysql.exec_query(t_sql)[0][0]
    x_time = []
    y_hot = []
    for i in result:
        st = time.strftime('%H:%M', time.localtime(i[0]))
        x_time.append(st)
        print(x_time)
        y_hot.append(i[1])
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.plot(x_time, y_hot)
    plt.gcf().autofmt_xdate()
    plt.title('"{}" 热搜热度变化图'.format(str(title)))
    plt.show()



get_weibo_data(search_id=61543)
