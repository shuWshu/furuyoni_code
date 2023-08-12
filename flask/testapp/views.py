from testapp import app

@app.route('/') # url
def index():
    return 'Hellow World!'

@app.route('/test')
def other1():
    return "テストページです！"
