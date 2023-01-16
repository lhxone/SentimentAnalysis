import json

import pymysql


class MysqlFactory:
    host: str = '127.0.0.1'
    port: int = 3306
    user: str = 'root'
    psw: str = '123456'
    db: str = 'weibo'
    charset: str = "utf8mb4"
    conn: pymysql.connections.Connection
    cursor: pymysql.connections.Connection

    def __init__(self):
        self.conn = pymysql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.psw,
            db=self.db,
            charset=self.charset
        )
        self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)

    def __int__(self, config: json):
        self.conn = pymysql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.psw,
            db=self.db,
            charset=self.charset
        )
        self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)

    def get(self):
        return self.conn,self.cursor
