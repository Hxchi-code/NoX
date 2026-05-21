from flask import Flask, request, send_file
import io

app = Flask(__name__)

@app.route('/process', methods=['POST'])
def process():
    file = request.files['video']
    mode = request.form.get('mode')
    data = bytearray(file.read())

    # "Bypass" atau "Bug" dilakukan dengan modifikasi atom data
    # Cari atom 'mvhd' (Movie Header) untuk mengubah durasi
    mvhd = data.find(b'mvhd')
    if mvhd != -1 and mode == 'bug':
        # Ubah durasi secara manual di header (offset dari mvhd)
        # Ini tidak merusak file karena kita hanya mengubah durasi metadata
        data[mvhd+20:mvhd+24] = b'\xff\xff\xff\xff' 

    out = io.BytesIO(data)
    return send_file(out, mimetype='video/mp4', as_attachment=True, download_name=f"{mode}_{file.filename}")

if __name__ == '__main__':
    app.run()
