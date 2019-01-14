

"""
# 查询总热度最高的20条热搜
SELECT weibo_hot.title, SUM(hot)
FROM weibo_hot
INNER JOIN weibo_hot_history ON weibo_hot.id = weibo_hot_history.search_id
GROUP BY title
HAVING SUM(hot) > 300000
ORDER BY SUM(hot)
DESC LIMIT 20
"""