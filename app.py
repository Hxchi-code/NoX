from flask import Flask, render_template, request, send_file
import io
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    if 'video' not in request.files:
        return "Error: Tidak ada video yang diupload", 400
        
    file = request.files['video']
    mode = request.form.get('mode') # Menerima pilihan mode dari tombol HTML
    
    # Baca mentahan video ke memori HP/Server
    data = bytearray(file.read())

    if mode == 'bug':
        # --- MODE 1: KHUSUS BUG DURASI ---
        # Menjalankan skrip asli kamu yang terbukti work buat bikin player lag
        stts_pos = data.find(b'stts')
        if stts_pos != -1:
            try:
                data[stts_pos + 16:stts_pos + 20] = b'\x00\x00\x4e\x20'
            except:
                pass
        nama_file = f"Bug_{file.filename}"

    elif mode == 'bypass':
        # --- MODE 2: KHUSUS BYPASS ZERO COMPRESSION ---
        # Menambahkan 8 byte acak di ujung paling akhir file video.
        # Ukuran file TETAP UTUH (cuma nambah 8 byte), MD5 berubah total, 100% ANTI-CORRUPT!
        try:
            data.extend(os.urandom(8))
        except:
            pass
        nama_file = f"Bypass_{file.filename}"
        
    else:
        nama_file = file.filename

    # Bungkus kembali data biner ke dalam format stream
    output = io.BytesIO(data)
    output.seek(0)
    
    # Kirim file kembali ke browser
    response = send_file(
        output, 
        mimetype='video/mp4', 
        as_attachment=True, 
        download_name=nama_file
    )
    
    # Paksa server mengirimkan informasi ukuran asli agar browser tidak memotong unduhan
    response.headers['Content-Length'] = len(data)
    
    return response

if __name__ == '__main__':
    app.run()

