from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from finder import MasterEmailFinder

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/find_email', methods=['POST'])
def api_find_email():
    data = request.json
    if not data:
        return jsonify({"error": "No JSON data provided"}), 400
        
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    domain = data.get('domain')
    
    if not all([first_name, last_name, domain]):
        return jsonify({"error": "Missing 'first_name', 'last_name', or 'domain'"}), 400
        
    try:
        finder = MasterEmailFinder(first_name, last_name, domain)
        result = finder.find_email()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
