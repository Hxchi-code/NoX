from flask import Flask, render_template, request, send_file
import io

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
    
    # Baca file mentah
    data = bytearray(file.read())

    # --- JALUR 1: KODINGAN BUG ASLI LU ---
    if mode == 'bug':
        stts_pos = data.find(b'stts')
        if stts_pos != -1:
            try:
                # Ini kodingan ori lu yang aman dan work
                data[stts_pos + 16:stts_pos + 20] = b'\x00\x00\x4e\x20'
            except:
                pass
        nama_file = f"Bug_{file.filename}"

    # --- JALUR 2: BYPASS AMAN (FREE BOX) ---
    elif mode == 'bypass':
        # Nambahin kotak kosong resmi MP4 di akhir file.
        # Dijamin 100% GAK CORRUPT karena ini struktur MP4 yang sah.
        data.extend(b'\x00\x00\x00\x08free')
        nama_file = f"Bypass_{file.filename}"
    
    else:
        # Jaga-jaga kalau mode gak kepilih
        nama_file = f"Ori_{file.filename}"

    # Kirim hasil
    output = io.BytesIO(data)
    return send_file(
        output, 
        mimetype='video/mp4', 
        as_attachment=True, 
        download_name=nama_file
    )

if __name__ == '__main__':
    app.run()
    
