from flask import Flask, render_template, request, send_file
import os
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    if 'video' not in request.files:
        return "No file", 400
    
    file = request.files['video']
    mode = request.form.get('mode')
    
    # Simpan file ke direktori sementara
    input_path = f"/tmp/{file.filename}"
    output_path = f"/tmp/out_{file.filename}"
    file.save(input_path)
    
    try:
        if mode == 'bug':
            # Gunakan subprocess dengan path absolut
            subprocess.run(['ffmpeg', '-i', input_path, '-filter:v', 'setpts=5.0*PTS', '-c:a', 'copy', '-y', output_path], check=True)
        else:
            subprocess.run(['ffmpeg', '-i', input_path, '-c', 'copy', '-movflags', '+faststart', '-y', output_path], check=True)
        
        return send_file(output_path, as_attachment=True)
    except Exception as e:
        return str(e), 500
    finally:
        # Opsional: hapus file setelah dikirim
        if os.path.exists(input_path): os.remove(input_path)

if __name__ == '__main__':
    app.run()
