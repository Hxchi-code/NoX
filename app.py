from flask import Flask, render_template, request, send_file
import io

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    # Cek apakah ada file yang diupload
    if 'video' not in request.files:
        return "Error: Tidak ada video yang diupload", 400
        
    file = request.files['video']
    mode = request.form.get('mode')
    
    # Baca video langsung ke memori (TIDAK butuh akses folder/disk)
    data = bytearray(file.read())

    # Mode BUG: Manipulasi struktur data biner video secara langsung
    if mode == 'bug':
        stts_pos = data.find(b'stts')
        if stts_pos != -1:
            try:
                # Ubah metadata durasi frame agar player nge-lag (bug)
                data[stts_pos + 16:stts_pos + 20] = b'\x00\x00\x4e\x20'
            except:
                pass # Abaikan jika gagal agar file tidak corrupt

    # Siapkan data untuk didownload
    output = io.BytesIO(data)
    nama_file = f"{mode}_{file.filename}"
    
    return send_file(
        output, 
        mimetype='video/mp4', 
        as_attachment=True, 
        download_name=nama_file
    )

if __name__ == '__main__':
    app.run()
