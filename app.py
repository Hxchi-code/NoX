from flask import Flask, render_template, request, send_file
import os

app = Flask(__name__)

@app.route('/process', methods=['POST'])
def process():
    file = request.files['video']
    mode = request.form.get('mode')
    
    input_f = f"in_{file.filename}"
    output_f = f"out_{file.filename}"
    file.save(input_f)
    
    if mode == 'bug':
        # Menggunakan setpts agar durasi melambat (freeze) tanpa merusak file
        os.system(f'ffmpeg -i {input_f} -filter:v "setpts=5.0*PTS" -c:a copy -y {output_f}')
    else:
        # Bypass standar (hanya copy stream)
        os.system(f'ffmpeg -i {input_f} -c copy -movflags +faststart -y {output_f}')
    
    return send_file(output_f, as_attachment=True)

# ... (tambahkan route lain seperti sebelumnya)
