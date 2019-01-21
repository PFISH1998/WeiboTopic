from sql import WeiboDataSearch
import time


class HotTopicChoose:
    def __init__(self):
        pass

    # 统计每日热搜榜
    def get_day(self):
        w = WeiboDataSearch()
        result = w.get_day_result(pass_time=1)
        hot_list = []
        for i in result:
            hot = dict()
            hot['title'] = i[0]
            hot['hot_sum'] = i[1]
            hot['update_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(i[2]))
            hot_list.append(hot)
        return hot_list
