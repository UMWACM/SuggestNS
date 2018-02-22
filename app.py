#!flask/bin/python
from flask import Flask, request
from flask import jsonify
import vocab

app = Flask(__name__)

# tasks = [
#     {
#         'id': 1,
#         'title': u'Buy groceries',
#         'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
#         'done': False
#     },
#     {
#         'id': 2,
#         'title': u'Learn Python',
#         'description': u'Need to find a good Python tutorial on the web',
#         'done': False
#     }
# ]
#
# @app.route('/todo/api/v1.0/tasks', methods=['GET'])
# def get_tasks():
#     return jsonify({'tasks': tasks})

@app.route('/suggestions', methods=['GET'])
def get_suggestions():
    url = request.args.get('url')
    print(url)
    return jsonify({'synonyms': vocab.get_synonyms(url)})

if __name__ == '__main__':
    app.run(debug=True)
