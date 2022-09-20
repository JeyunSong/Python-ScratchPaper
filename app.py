from pymongo import MongoClient
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

client = MongoClient('mongodb+srv://JEYUN:LAKE@cluster0.g4kgzxf.mongodb.net/Cluster0?retryWrites=true&w=majority')

db = client.study

# 완료!
@app.route('/')
def main_page():
    return render_template('/main.html')


@app.route('/post')
def post_page():
    return render_template('/index.html')

# 상세페이지
@app.route("/user/<keyword>")
def show_userpostings(keyword):
    keywords = int(float(keyword))
    user_postings_list = db.pic.find_one({'post_num': keywords})
    return render_template('/index2.html', row = user_postings_list)


@app.route('/save_post', methods=["POST"])
def save_post():
    title_receive = request.form['title']
    content_receive = request.form['text']
    likecount_receive = request.form['like_count']
    picture_receive = request.form.get('picture')

    user_posting_list = list(db.pic.find({}, {'_id': False}))
    count = len(user_posting_list) + 1

    # likeid = []

    doc = {
        'post_num': count,
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
