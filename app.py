from pymongo import MongoClient
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

client = MongoClient('mongodb+srv://test:sparta@cluster0.g4kgzxf.mongodb.net/Cluster0?retryWrites=true&w=majority')

db = client.study


@app.route('/')
def main_page():
    return render_template('/main.html')


@app.route('/post')
def post_page():
    return render_template('/index.html')


@app.route('/save_post', methods=["POST"])
def save_post():
    picture_receive = request.form.get('picture_give')
    db.pic.insert_one({'picture': picture_receive})
    return jsonify({'result': 'success'})


@app.route("/show_post", methods=["GET"])
def show_post():
    pic_list = list(db.pic.find({}, {'_id': False}))
    return jsonify({'pic': pic_list})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
