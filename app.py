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
    
    # Baca video langsung ke memori (Sesuai kodingan asli kamu yang terbukti stabil)
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
                pass 

    # --- 2. FITUR BYPASS ZERO COMPRESSION (TRIK SENZEYN) ---
    # Otomatis aktif di semua mode (Bypass murni atau Bug + Bypass)
    # Kita kunci headernya di byte ke-15 (Minor Version MP4) di bagian paling depan file.
    # Ukuran file TETAP ASLI, tidak bergeser 1 byte pun, tapi MD5 berubah total!
    try:
        if len(data) > 15 and data[4:8] == b'ftyp':
            data[15] = (data[15] + 1) % 256
    except:
        pass

    # Kembalikan pakai kombinasi BytesIO + send_file milikmu agar ukuran utuh dan tidak terpotong
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
