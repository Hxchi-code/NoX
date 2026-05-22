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

    # --- BUG DURASI (KHUSUS VIDEO MENTAH) ---
    # Kalau lu pake video hasil edit, fitur ini emang riskan corrupt
    if mode == 'bug':
        stts_pos = data.find(b'stts')
        if stts_pos != -1:
            data[stts_pos + 16:stts_pos + 20] = b'\x00\x00\x4e\x20'

    # --- BYPASS (AMANKAN DENGAN 'udta' BOX) ---
    # Ini trik paling stabil buat video hasil edit. 
    # Kita nyelipin 'udta' (User Data) box yang kosong.
    # Player bakal ngebaca ini sebagai tambahan info, bukan konten video.
    padding = b'\x00\x00\x00\x1fudta\x00\x00\x00\x17meta\x00\x00\x00\x00'
    data.extend(padding)

    output = io.BytesIO(data)
    return send_file(output, mimetype='video/mp4', as_attachment=True, download_name=f"Fixed_{file.filename}")

if __name__ == '__main__':
    app.run()
