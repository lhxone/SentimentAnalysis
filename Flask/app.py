import os
import yaml
from flask import Flask, render_template, request

from utils.sql_util import MysqlFactory

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def hello_world():
    return Dashboard()


@app.route('/api/v1/getHotSearch', methods=['GET'])
def getHotSearch():
    cursor.execute("select * from HotSearch order by num DESC limit 50")
    data = cursor.fetchall()
    return data


@app.route('/api/v1/getHotSearchById/<id>', methods=['GET'])
def getHotSearchById(id):
    cursor.execute("select * from HotSearch where id ={}".format(id))
    data = cursor.fetchall()
    return data


@app.route('/api/v1/getHotSearchByTitle/<title>', methods=['GET'])
def getHotSearchByTitle(title):
    cursor.execute("select * from HotSearch where title like '%{}%'".format(title))
    data = cursor.fetchall()
    return data


@app.route('/dashboard', methods=['GET'])
def Dashboard():
    data = getHotSearch()
    data = data[:10]
    xAxis = []
    yAxis = []
    for i in data:
        xAxis.append(i['title'])
        yAxis.append(i['num'])

    return render_template('Dashboard.html', xdata=str(xAxis), ydata=str(yAxis))


@app.route('/hotsearch', methods=['GET'])
def HotSearch():
    return render_template('HotSearch.html', data=getHotSearch())


@app.route('/search', methods=['POST', 'GET'])
def Search():
    if request.method == 'POST':
        id = request.form.get('id')
        title = request.form.get('title')
        if (len(id)!=0 and len(title)!=0):
            result = getHotSearchById(id)
            result.append(getHotSearchByTitle(title))
        elif (len(id)==0 and len(title)!=0):
            result = getHotSearchByTitle(title)
        elif (len(id)!=0 and len(title)==0):
            result = getHotSearchById(id)
        else:
            result = []
        return render_template("Search.html", result=result)
    return render_template('Search.html')


if __name__ == '__main__':
    HOME_DIR = HOME = os.path.abspath(os.path.dirname(os.getcwd()))
    config_filepath = os.path.join(HOME_DIR, 'config/config.yaml')
    config = yaml.load(open(config_filepath, 'r').read(), Loader=yaml.FullLoader)
    mysql_config = config['mysql']
    conn, cursor = MysqlFactory(config).get()
    app.run(debug=True, port=8080)
