# server.py
from flask import Flask, request, jsonify
from ArdChip import set

app = Flask(__name__)

@app.route('/update_status', methods=['POST'])
def update_status():
    try:
        status = request.args.get('status', type=bool)
        set(status)
        return jsonify({'success': True, 'status': status})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
