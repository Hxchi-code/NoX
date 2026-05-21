from flask import Flask, render_template, request, send_file
from moviepy.editor import VideoFileClip
import os

app = Flask(__name__)

@app.route('/process', methods=['POST'])
def process():
    file = request.files['video']
    mode = request.form.get('mode')
    
    input_path = "temp_in.mp4"
    output_path = "temp_out.mp4"
    file.save(input_path)
    
    try:
        # Load video
        clip = VideoFileClip(input_path)
        
        if mode == 'bug':
            # Efek freeze/lag dengan memperlambat 5x
            final = clip.fx(lambda c: c.speedx(0.2))
        else:
            final = clip
            
        final.write_videofile(output_path, codec="libx264", audio_codec="aac")
        return send_file(output_path, as_attachment=True)
    
    except Exception as e:
        return str(e), 500
    finally:
        if os.path.exists(input_path): os.remove(input_path)

if __name__ == '__main__':
    app.run()
