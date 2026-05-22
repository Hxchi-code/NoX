from flask import Flask, render_template, request, send_file
import io

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    file = request.files['video']
    mode = request.form.get('mode')
    data = bytearray(file.read())

    # Modifikasi Header MP4 untuk efek "Bug"
    # Kita cari atom 'stts' (Time-to-Sample) yang mengatur durasi frame
    stts_pos = data.find(b'stts')
    if stts_pos != -1 and mode == 'bug':
        # Ubah entry durasi frame agar player bingung (efek lag)
        # Kita pakai offset aman agar tidak merusak struktur file
        data[stts_pos + 16:stts_pos + 20] = b'\x00\x00\x4e\x20'

    output = io.BytesIO(data)
    return send_file(output, mimetype='video/mp4', as_attachment=True, download_name=f"processed_{file.filename}")

if __name__ == '__main__':
    app.run()
