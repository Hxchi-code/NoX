from flask import Flask, render_template, request, send_file
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    file = request.files['video']
    mode = request.form.get('mode')
    
    input_filename = f"input_{file.filename}"
    output_filename = f"out_{file.filename}"
    file.save(input_filename)
    
    # Menggunakan FFmpeg untuk manipulasi aman
    if mode == 'bug':
        # Efek lag/freeze dengan memperlambat frame
        os.system(f'ffmpeg -i {input_filename} -filter:v "setpts=5.0*PTS" -y {output_filename}')
    else:
        # Bypass standar (remux agar kompatibel)
        os.system(f'ffmpeg -i {input_filename} -c copy -movflags +faststart -y {output_filename}')
    
    return send_file(output_filename, as_attachment=True)

if __name__ == '__main__':
    app.run()

