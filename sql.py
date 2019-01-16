"""
This module implements the API of get weibo_hot_search data
"""
from PySQL import PySQL
import time


class WeiboDataSearch:
    def __init__(self):
        self._day_sum_sql = "SELECT title, SUM(hot), weibo_hot.update_time FROM weibo_hot " \
                            "INNER JOIN weibo_hot_history ON weibo_hot.id = weibo_hot_history.search_id " \
                            "GROUP BY title HAVING {now_time} - update_time < {pass_time} " \
                            "AND title LIKE '%{title}%' " \
                            "ORDER BY SUM(hot) DESC LIMIT {num}"

    def _get_result(self, **kwargs):
        value = dict(
            now_time=int(time.time()),
            pass_time=1,
            num=30,
            title=None
        )

        badargs = set(kwargs) - set(value)
        if badargs:
            err = 'search_result got unexpected keyword arguments: {}'
            raise TypeError(err.format(list(badargs)))

        value.update(kwargs)
        sql = self._day_sum_sql.format(**value)
        print(sql)
        return PySQL().exec_query(sql=sql)

    def get_day_result(self, **kwargs):
        one_day = 86400
        value = dict(pass_time=1)
        value.update(kwargs)
        value['pass_time'] = one_day * value['pass_time']
        return self._get_result(**value)

    def get_hour_result(self, **kwargs):
        one_hour = 3600
        value = dict(pass_time=1)
        value.update(kwargs)
        value['pass_time'] = one_hour * value['pass_time']
        return self._get_result(**value)


w = WeiboDataSearch()
r = w.get_day_result(title='中', pass_time=2)
print(r)