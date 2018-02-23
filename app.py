#!flask/bin/python
from flask import Flask, request
from flask import jsonify
import suggestions

app = Flask(__name__)

@app.route('/suggestions', methods=['GET'])
def get_suggestions():
    customizer = request.args.get('customizer')
    tlds = request.args.get('tlds')
    if (request.args.get('lat') or request.args.get('long')) is None:
        return jsonify(suggestions.get(customizer, tlds))
    else:
        latlong = request.args.get('lat') + request.args.get('long')
        print(latlong)
        return jsonify(suggestions.get(customizer, tlds, latlong))
if __name__ == '__main__':
    app.run(debug=True)
