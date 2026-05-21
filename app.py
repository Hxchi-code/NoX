from flask import Flask, render_template, request, send_file
import subprocess, os

app = Flask(__name__)

@app.route('/process', methods=['POST'])
def process():
    file = request.files['video']
    mode = request.form.get('mode')
    
    input_path = "input.mp4"
    output_path = "output.mp4"
    file.save(input_path)
    
    # Hapus output lama jika ada
    if os.path.exists(output_path):
        os.remove(output_path)
    
    # Jalankan FFmpeg
    if mode == 'bug':
        cmd = ['ffmpeg', '-i', input_path, '-filter:v', 'setpts=5.0*PTS', '-c:v', 'libx264', '-crf', '28', '-c:a', 'copy', '-y', output_path]
    else:
        cmd = ['ffmpeg', '-i', input_path, '-c', 'copy', '-movflags', '+faststart', '-y', output_path]
        
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    # Jika FFmpeg berhasil dan file output ada
    if result.returncode == 0 and os.path.exists(output_path):
        # Cek apakah file output beneran ada isinya (lebih dari 1KB)
        if os.path.getsize(output_path) > 1024:
            return send_file(output_path, as_attachment=True)
        else:
            return "Error: File hasil terlalu kecil, proses gagal.", 500
    else:
        return f"FFmpeg Error: {result.stderr}", 500

if __name__ == '__main__':
    app.run()
