from flask import Flask, render_template, request, send_file
import os
import subprocess
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'video' not in request.files:
        return "No video uploaded", 400

    video = request.files['video']
    filename = secure_filename(video.filename)
    input_path = os.path.join(UPLOAD_FOLDER, filename)
    video.save(input_path)

    output_filename = filename.rsplit('.', 1)[0] + "_muted.mp4"
    output_path = os.path.join(PROCESSED_FOLDER, output_filename)

    # FFmpeg command to remove audio
    command = ['ffmpeg', '-i', input_path, '-c', 'copy', '-an', output_path]
    subprocess.run(command)

    return send_file(output_path, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
