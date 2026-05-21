    from flask import Flask, render_template, request, send_file
import subprocess, io, os

app = Flask(__name__)

@app.route('/process', methods=['POST'])
def process():
    file = request.files['video']
    mode = request.form.get('mode')
    
    
    in_mem = io.BytesIO(file.read())
    out_mem = io.BytesIO()
    

    with open("input.mp4", "wb") as f: f.write(in_mem.getvalue())
    
    if mode == 'bug':
        # Perintah ini dijamin tidak merusak header MP4
        cmd = ["ffmpeg", "-i", "input.mp4", "-filter:v", "setpts=2.0*PTS", "-c:a", "copy", "-f", "mp4", "-movflags", "frag_keyframe+empty_moov", "pipe:1"]
    else:
        cmd = ["ffmpeg", "-i", "input.mp4", "-c", "copy", "-movflags", "+faststart", "-f", "mp4", "pipe:1"]

    result = subprocess.run(cmd, capture_output=True)
    
    if result.returncode != 0:
        return f"FFmpeg Error: {result.stderr.decode()}", 500
    
    out_mem.write(result.stdout)
    out_mem.seek(0)
    return send_file(out_mem, mimetype='video/mp4', as_attachment=True, download_name=f"{mode}_{file.filename}")

if __name__ == '__main__':
    app.run()
