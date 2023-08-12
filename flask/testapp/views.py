from flask import render_template
from testapp import app


@app.route('/')
def index():
    # htmlへデータを直接渡す
    my_dict = {
        'insert_something1': 'views.pyのinsert_something1部分です。',
        'insert_something2': 'views.pyのinsert_something2部分です。',
    }
    return render_template('testapp/index.html', my_dict=my_dict)

