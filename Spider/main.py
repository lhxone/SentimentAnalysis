import json
import requests
import pymysql

from utils.sql_util import MysqlFactory


def get_data():
    """
        获取微博热搜
        Args:
            params: (dict): {}
        Returns:
            json: {title: 标题, url: 地址, num: 热度数值, hot: 热搜等级}
    """

    data = []
    response = requests.get("https://weibo.com/ajax/side/hotSearch")
    data_json = response.json()['data']['realtime']
    jyzy = {
        '电影': '影',
        '剧集': '剧',
        '综艺': '综',
        '音乐': '音'
    }

    for data_item in data_json:
        hot = ''
        # 如果是广告，则不添加
        if 'is_ad' in data_item:
            continue
        if 'flag_desc' in data_item:
            hot = jyzy.get(data_item['flag_desc'])
        if 'is_boom' in data_item:
            hot = '爆'
        if 'is_hot' in data_item:
            hot = '热'
        if 'is_fei' in data_item:
            hot = '沸'
        if 'is_new' in data_item:
            hot = '新'

        dic = {
            'title': data_item['note'],
            'url': 'https://s.weibo.com/weibo?q=%23' + data_item['word'] + '%23',
            'num': data_item['num'],
            'hot': hot
        }
        data.append(dic)

    return data


def save_data(data, config):
    """
    Args:
        data: 要插入的数据
        config: 数据库连接设置
    Returns:
        affect_rows
    """

    conn, cursor = MysqlFactory().get()
    sql = "INSERT INTO HotSearch(title,url,num,hot) VALUES {} order by num"
    data_str = ""
    for each_data in data:
        data_str += "('{}','{}',{},'{}'),".format(each_data['title'], each_data['url'], each_data['num'],
                                                  each_data['hot'])
    sql = sql.format(data_str).strip(',')
    print(sql)
    affect_rows = cursor.execute(sql)
    conn.commit()
    return affect_rows


if __name__ == '__main__':
    data = get_data()
    print(data)
    save_data(data, "")
