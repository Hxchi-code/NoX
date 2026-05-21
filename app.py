import subprocess
from flask import Flask, request, send_file
import os

app = Flask(__name__)

@app.route('/process', methods=['POST'])
def process():
    file = request.files['video']
    mode = request.form.get('mode')
    
    input_path = f"temp_{file.filename}"
    output_path = f"out_{file.filename}"
    file.save(input_path)
    
    if mode == 'bug':
        # Menggunakan filter setpts untuk membuat video jadi sangat lambat (efek lag/freeze)
        # 10.0 adalah multiplier durasi. 
        subprocess.run(['ffmpeg', '-i', input_path, '-filter:v', 'setpts=10.0*PTS', output_path])
    else:
        # Bypass standar (hanya remux ke mp4 agar faststart)
        subprocess.run(['ffmpeg', '-i', input_path, '-c', 'copy', '-movflags', 'faststart', output_path])
        
    return send_file(output_path, as_attachment=True)
