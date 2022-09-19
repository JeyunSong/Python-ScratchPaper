from pymongo import MongoClient
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

client = MongoClient('mongodb+srv://JEYUN:JEYUN@cluster0.g4kgzxf.mongodb.net/Cluster0?retryWrites=true&w=majority')

db = client.study


@app.route('/')
def main_page():
    return render_template('/main.html')


@app.route('/post')
def post_page():
    return render_template('/index.html')


@app.route('/save_post', methods=["POST"])
def save_post():
    title_receive = request.form['title_give']
    content_receive = request.form['content_give']
    likecount_receive = request.form['likecount_give']
    picture_receive = request.form.get('picture_give')

    user_posting_list = list(db.pic.find({}, {'_id': False}))
    count = len(user_posting_list) + 1

    # likeid = []

    doc = {
        'postnum': count,
        'title': title_receive,
        'content': content_receive,
        'likecount': likecount_receive,
        'picture': picture_receive
        # 'likeid' : (title_receive,content_receive)
    }

    db.pic.insert_one(doc)
    return jsonify({'result': 'success', 'msg': '저장 완료!'})


@app.route("/show_post", methods=["GET"])
def show_post():
    pic_list = list(db.pic.find({}, {'_id': False}))
    return jsonify({'pic': pic_list})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
