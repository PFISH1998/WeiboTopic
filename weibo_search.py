import json
import time
import requests
import pymysql

topic_url = 'https://s.weibo.com/weibo?q={}'


def get_search_page():
    api_url = 'https://m.weibo.cn/api/container/getIndex?containerid=106003type%3D25%26t%3D3%26disable_hot%3D1%26filter_type%3Drealtimehot&title=%E5%BE%AE%E5%8D%9A%E7%83%AD%E6%90%9C&extparam=filter_type%3Drealtimehot%26mi_cid%3D100103%26pos%3D0_0%26c_type%3D30%26display_time%3D1545472196&luicode=10000011&lfid=231583'
    # api_url = 'https://s.weibo.com/top/summary'
    r = requests.get(api_url)
    json_str = json.loads(r.text)
    # print(json_str)
    try:
        content = json_str['data']['cards'][0]['card_group']
    except KeyError as e:
        if e == 'card_group':
            content = json_str['data']['cards'][1]['card_group']
        else:
            print(e)
            time.sleep(3)
            get_search_page()
    except Exception as e:
        print(e)
        # time.sleep(3)
        # get_search_page()

    finally:
        info_list = []
        for i in content:
            info = dict()
            try:
                info['title'] = i['desc']
                info['hot'] = int(i['desc_extr'])
                print(info)
                info_list.append(info)
            except KeyError:
                pass
        print('-----------------')
        return info_list


def save_data(data):
    db = pymysql.connect("172.17.4.62", "pi", "pengyu", "weibo")
    db.set_charset('utf8')
    cursor = db.cursor()
    search_time = int(time.time())
    print(time.asctime(time.localtime(time.time())))
    for i in data:
        title = i['title']
        hot = i['hot']
        select_sql = "INSERT INTO weibo_search_history(title, add_time, update_time)" \
                     "VALUES ('{}', {}, {}) ON DUPLICATE KEY UPDATE " \
                     "UPDATE_TIME = {}".format(title, search_time, search_time, search_time)
        cursor.execute(select_sql)
        db.commit()
        select_sql = "SELECT ID FROM weibo_search_history WHERE title='{}'".format(title)
        cursor.execute(select_sql)
        result = cursor.fetchall()
        title_id = result[0][0]
        sql = "INSERT INTO weibo_search (search_time, search_id, hot) " \
              "VALUES ({},'{}',{})".format(search_time, title_id, hot)
        cursor.execute(sql)
        db.commit()
    cursor.close()
    db.close()


def get_api_topic():
    api_url = 'https://m.weibo.cn/api/container/getIndex?containerid=231648_-_1_-_all_-_' \
              '%E8%AF%9D%E9%A2%98%E6%A6%9C_-_1&luicode=10000011&lfid=231583&page=1'
    r = requests.get(api_url)
    json_str = json.loads(r.text)
    content = json_str['data']['cards'][0]['card_group']
    search_time = time.asctime(time.localtime(time.time()))
    for i in content:
        topic = dict()
        try:
            topic['title'] = i['title_sub']
            topic['view'] = i['desc2']
            topic['desc'] = i['desc1']
            topic['pic'] = i['pic']
            print(topic)
        except KeyError:
            pass
    print(search_time)
    print('-----------------')
    return topic


def main():
    data = get_search_page()
    save_data(data)


if __name__ == '__main__':
    while True:
        main()
        time.sleep(120)