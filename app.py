from flask import Flask, render_template, request, Response

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
    
    # Baca file mentahan secara utuh
    data = bytearray(file.read())

    # --- 1. FITUR BUG DURASI ---
    if mode == 'bug':
        stts_pos = data.find(b'stts')
        if stts_pos != -1:
            try:
                # Manipulasi durasi frame (Kodingan asli kamu yang aman)
                data[stts_pos + 16:stts_pos + 20] = b'\x00\x00\x4e\x20'
            except:
                pass

    # --- 2. FITUR BYPASS ZERO COMPRESSION (UBAH MD5) ---
    # Aktif di semua mode. 
    mvhd_pos = data.find(b'mvhd')
    if mvhd_pos != -1:
        try:
            # Offset +12 adalah "Modification Time".
            # Kita cuma nambahin angka 1 di jam modifikasinya. 
            # File dijamin tidak corrupt, ukuran TETAP ASLI, tapi MD5 berubah 100%.
            data[mvhd_pos + 12] = (data[mvhd_pos + 12] + 1) % 256
        except:
            pass

    # Penamaan file
    if mode == 'bug':
        nama_file = f"Bug_Bypass_{file.filename}"
    else:
        nama_file = f"Bypass_{file.filename}"
        
    # Lempar file mentah langsung ke browser (Tanpa BytesIO) agar ukuran tidak menyusut
    return Response(
        bytes(data),
        mimetype="video/mp4",
        headers={"Content-disposition": f"attachment; filename={nama_file}"}
    )

if __name__ == '__main__':
    app.run()
