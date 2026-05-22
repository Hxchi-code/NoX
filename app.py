from flask import Flask, render_template, request, send_file
import io
import os

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

    # --- 1. FITUR BUG DURASI ---
    # Pakai kodingan asli kamu yang sudah terbukti work 100%
    if mode == 'bug':
        stts_pos = data.find(b'stts')
        if stts_pos != -1:
            try:
                # Ubah metadata durasi frame agar player nge-lag (bug)
                data[stts_pos + 16:stts_pos + 20] = b'\x00\x00\x4e\x20'
            except:
                pass # Abaikan jika gagal agar file tidak corrupt

    # --- 2. FITUR BYPASS SENZEYN (ZERO COMPRESSION) ---
    # Otomatis aktif di kedua fitur (Bypass murni ATAU Bug + Bypass sekalian)
    # Kita suntikkan 'free' box valid di akhir file agar merubah MD5 secara unik
    # Cara ini dijamin tidak akan merusak struktur efek bug durasi di atas
    try:
        bypass_signature = b'SenzeynBypassZeroCompression1080p60FPS' + os.urandom(16)
        # Hitung ukuran box (panjang data + 8 byte header)
        box_size = (len(bypass_signature) + 8).to_bytes(4, byteorder='big')
        # Satukan menjadi struktur atom MP4 yang sah ([size][type][data])
        free_box = box_size + b'free' + bypass_signature
        # Tempel di paling akhir file video
        data.extend(free_box)
    except:
        pass

    # Siapkan data untuk didownload
    output = io.BytesIO(data)
    
    # Penamaan file otomatis sesuai mode yang dipilih
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
