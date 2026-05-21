from flask import Flask, render_template, request, send_file
import subprocess, io, os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    file = request.files['video']
    mode = request.form.get('mode')
    input_path = "input.mp4"
    output_path = "output.mp4"
    file.save(input_path)
    
    if mode == 'bug':
        subprocess.run(['ffmpeg', '-i', input_path, '-filter:v', 'setpts=5.0*PTS', '-c:a', 'copy', '-y', output_path], check=True)
    else:
        subprocess.run(['ffmpeg', '-i', input_path, '-c', 'copy', '-movflags', '+faststart', '-y', output_path], check=True)
    
    return send_file(output_path, as_attachment=True)

if __name__ == '__main__':
    app.run()

