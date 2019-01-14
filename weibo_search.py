import json
import time
import requests
from PySQL import PySQL

topic_url = 'https://s.weibo.com/weibo?q={}'


class WeiboSearch:
    def __init__(self):
        self.api_url = 'https://m.weibo.cn/api/container/getIndex' \
                       '?containerid=106003type%3D25%26t%3D3%26disable_hot%3D1%26filter_type%3Drealtimehot'

    def get_search_page(self):
        # api_url = 'https://s.weibo.com/top/summary'
        r = requests.get(self.api_url)
        json_str = json.loads(r.text)
        try:
            content = json_str['data']['cards'][0]['card_group']
        except KeyError as e:
            if e == 'card_group':
                content = json_str['data']['cards'][1]['card_group']
            else:
                print(e)
                time.sleep(3)
                self.get_search_page()
        except Exception as e:
            print(e)
            # time.sleep(3)
            # self.get_search_page()
        else:
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
            return info_list

    def save_data(self, search_list):
        mysql = PySQL()
        search_time = int(time.time())
        print('---------{}----------'.format(time.asctime(time.localtime(time.time()))))
        for i in search_list:
            title_id = ''
            title = i['title']
            hot = i['hot']
            select_sql = "SELECT ID FROM weibo_hot WHERE title='{}'".format(title)
            is_result = mysql.exec_query(select_sql)
            # 查询有结果
            if is_result:
                title_id = is_result[0][0]
            else:
                insert_sql = "INSERT INTO weibo_hot (title, add_time, update_time) " \
                             "VALUES ('{}', {}, {})".format(title, search_time, search_time)
                mysql.exec_non_query(insert_sql)

                select_sql = "SELECT ID FROM weibo_hot WHERE title='{}'".format(title)
                result = mysql.exec_query(select_sql)
                title_id = result[0][0]

            sql = "INSERT INTO weibo_hot_history (search_time, search_id, hot) " \
                  "VALUES ({},'{}',{})".format(search_time, title_id, hot)
            mysql.exec_non_query(sql)
        mysql.close()

    def get_api_topic(self):
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


if __name__ == '__main__':
    weibo = WeiboSearch()
    while True:
        try:
            data = weibo.get_search_page()
            weibo.save_data(data)
        except Exception as e:
            print("e", e)
            pass
        time.sleep(120)