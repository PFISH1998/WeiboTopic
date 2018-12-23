import pymysql
import configparser

config = configparser.ConfigParser()
config.read('weibo.ini')
host = config.get('DATABASE', 'HOST')
user = config.get('DATABASE', 'USERNAME')
pwd = config.get('DATABASE', 'PASSWORD')
database = config.get('DATABASE', 'DATABASE')


class PySQL:

    def __init__(self):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.db = database
        self._conn = self.get_connection()
        if self._conn:
            self._cur = self._conn.cursor()

    def get_connection(self):
        conn = False
        try:
            conn = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.pwd,
                database=self.db
            )
        except Exception as e:
            print("连接数据库失败：", e)
        else:
            return conn

    # 查询类语句
    def exec_query(self, sql):
        res = ''
        try:
            self._cur.execute(sql)
            res = self._cur.fetchall()
        except Exception as e:
            print("查询失败：", e)
        else:
            return res

    # 非查询类语句
    def exec_non_query(self, sql):
        flag = False
        try:
            self._cur.execute(sql)
            self._conn.commit()
            flag = True
        except Exception as e:
            flag = False
            self._conn.rollback()
            print("查询出错：", e)
        else:
            return flag

    def close(self):
        if self._conn:
            try:
                if type(self._cur) == 'object':
                    self._cur.close()
                if type(self._conn) == 'object':
                    self._conn.close()
            except Exception as e:
                raise ("close error:", e)