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
    
    # Baca video langsung ke memori (Sesuai kodingan kamu yang terbukti work)
    data = bytearray(file.read())

    # --- 1. FITUR BUG DURASI ---
    # Pakai kodingan asli kamu yang sudah terbukti mantap
    if mode == 'bug':
        stts_pos = data.find(b'stts')
        if stts_pos != -1:
            try:
                # Ubah metadata durasi frame agar player nge-lag (bug)
                data[stts_pos + 16:stts_pos + 20] = b'\x00\x00\x4e\x20'
            except:
                pass 

    # --- 2. FITUR BYPASS ZERO COMPRESSION (UBAH MD5) ---
    # Aktif otomatis di kedua mode (Bypass murni maupun Bug+Bypass)
    # Kita tempel 16 byte data acak di paling akhir file video.
    # Pemutar video & TikTok akan mengabaikan ekor file ini saat memutar video (Anti-Corrupt),
    # tapi MD5 filenya berubah total jadi file baru (Bypass Sukses & Ukuran Tetap Utuh).
    try:
        data.extend(os.urandom(16))
    except:
        pass

    # Bungkus kembali pakai BytesIO agar transfer data ke HP stabil dan tidak kepotong
    output = io.BytesIO(data)
    
    # Penamaan file otomatis sesuai tombol
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
