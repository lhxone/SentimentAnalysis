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
    print(cursor.fetchall())
    return data


@app.route('/api/v1/getHotSearch/<id>', methods=['GET'])
def getHotSearchById(id):
    cursor.execute("select * from HotSearch where id ={}".format(id))
    data = cursor.fetchall()
    print(data)
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
        result = getHotSearchById(id)
        print(result)
        return render_template("Search.html", result=result)
    return render_template('Search.html')


if __name__ == '__main__':
    conn, cursor = MysqlFactory().get()
    app.run(debug=True, port=8080)
