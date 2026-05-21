from flask import Flask, render_template, request, send_file
import struct, io

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    file = request.files['video']
    mode = request.form.get('mode')
    data = bytearray(file.read())

    if mode == 'bug':
        stts_idx = data.find(b'stts')
        if stts_idx != -1:
            # Inject 0xFFFF ke entry pertama durasi frame
            data[stts_idx + 16:stts_idx + 20] = struct.pack('>I', 0xFFFF)
    
    output = io.BytesIO(data)
    return send_file(output, mimetype='video/mp4', as_attachment=True, download_name=f"{mode}_{file.filename}")

if __name__ == '__main__':
    app.run()
