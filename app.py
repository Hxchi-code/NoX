from flask import Flask, render_template, request, send_file
import io
import random

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
    
    # Baca file mentahan ke memori
    data = bytearray(file.read())

    # --- 1. FITUR BUG DURASI ---
    if mode == 'bug':
        stts_pos = data.find(b'stts')
        if stts_pos != -1:
            try:
                # Ubah frame duration agar nge-bug/lag
                data[stts_pos + 16:stts_pos + 20] = b'\x00\x00\x4e\x20'
            except:
                pass

    # --- 2. FITUR BYPASS ZERO COMPRESSION (UBAH MD5) ---
    # Aktif untuk semua mode. Kita acak metadata 'mvhd' (Movie Header).
    # Ini cuma ngubah info "Jam Pembuatan Video", BUKAN ngubah isi video.
    # Hasilnya: File tetap utuh, anti-corrupt, lolos kompresi platform.
    mvhd_pos = data.find(b'mvhd')
    if mvhd_pos != -1:
        try:
            # Mengacak 1 byte di area timestamp
            data[mvhd_pos + 16] = random.randint(0, 255)
        except:
            pass

    # Siapkan output
    output = io.BytesIO(data)
    
    # Penamaan file
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
