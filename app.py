from flask import Flask, render_template, request, send_file
import struct
import io

app = Flask(__name__)

def process_video_logic(data, mode):
    data = bytearray(data)
    if mode == 'bug':
        stts_idx = data.find(b'stts')
        if stts_idx != -1:
            entry_offset = stts_idx + 12 + 4
            if len(data) > entry_offset + 4:
                data[entry_offset:entry_offset+4] = struct.pack('>I', 0xFFFF)
    return data

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    file = request.files['video']
    mode = request.form.get('mode')
    data = process_video_logic(file.read(), mode)
    
    output = io.BytesIO(data)
    return send_file(output, mimetype='video/mp4', as_attachment=True, download_name=f"{mode}_{file.filename}")

if __name__ == '__main__':
    app.run(debug=True)
