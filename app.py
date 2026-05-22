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
    mode = request.form.get('mode')
    
    # Membaca mentahan file video langsung ke memori
    data = bytearray(file.read())

    # --- 1. FITUR BUG DURASI ---
    # Hanya dijalankan jika user memilih tombol Bug
    if mode == 'bug':
        stts_pos = data.find(b'stts')
        if stts_pos != -1:
            try:
                # Modifikasi metadata durasi frame agar video nge-lag (bug)
                data[stts_pos + 16:stts_pos + 20] = b'\x00\x00\x4e\x20'
            except:
                pass # Abaikan jika gagal agar file tetap aman

    # --- 2. FITUR BYPASS (ZERO COMPRESSION) ---
    # Diterapkan ke SEMUA mode secara otomatis (Bypass Murni ATAU Bug+Bypass)
    # Cara kerja: Menyuntikkan Atom MP4 valid berisi data acak di akhir file.
    # File akan lolos pemeriksaan duplikasi server dan terhindar dari kompresi burik.
    bypass_size = 2048  # Menyuntikkan 2KB padding data Bypass
    bypass_atom = bypass_size.to_bytes(4, byteorder='big') + b'free' + os.urandom(bypass_size - 8)
    data.extend(bypass_atom)

    # Siapkan file output untuk didownload
    output = io.BytesIO(data)
    
    # Penamaan file otomatis agar kamu tahu hasilnya
    if mode == 'bug':
        nama_file = f"Bug_Bypass_{file.filename}"
    else:
        nama_file = f"Bypass_{file.filename}"
        
    return send_file(
        output, 
        mimetype='video/mp4', 
        as_attachment=True, 
        download_name=nama_file
    )

if __name__ == '__main__':
    app.run()

