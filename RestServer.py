from flask import Flask, jsonify
from flask import abort
from flask import make_response
from flask import request
from flask import abort
from flask import make_response
import json
import document_analyzer

app = Flask(__name__)

# example request:
# curl -i -H "Content-Type: application/json" -X POST -d '{"URLs": ["https://www.araba.com", "https://www.arabam.com", "http://www.oyunskor.com/araba-oyunlari", "https://www.sahibinden.com/kategori/otomobil", "http://www.oyunkolu.com/araba-oyunlari/"]}' http://localhost:5000/document-analyzer/api/get_tfidf_scores
@app.route('/document-analyzer/api/get_tfidf_scores', methods=['POST'])
def search_wordenp():
    if not request.json or not 'URLs' in request.json:
        abort(400)
    result = document_analyzer.get_tfidf_scores(request.json['URLs'])
    return jsonify(result), 200

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
	app.run(debug=True)