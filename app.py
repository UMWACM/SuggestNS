#!flask/bin/python
from flask import Flask, request
from flask import jsonify
import suggestions

app = Flask(__name__)

@app.route('/suggestions', methods=['GET'])
def get_suggestions():
    customizer = request.args.get('customizer')
    tlds = requests.args.get('tlds')
    if (requests.args.get('lat') or requests.args.get('long')) is None:
        return jsonify(suggestions.get(customizer, tlds))
    else:
        latlong = requests.args.get('lat') + requests.args.get('long')
        print(latlong)
        return jsonify(suggestions.get(customizer, tlds, latlong))
if __name__ == '__main__':
    app.run(debug=True)
