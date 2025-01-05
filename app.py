from flask import Flask, request, send_file, render_template
import browser_cookie3
import yt_dlp
import os

app = Flask(__name__)
DOWNLOAD_DIR = "tmp/downloads"

if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download_video():
    cookies = browser_cookie3.firefox()
    url = request.form['url']
    ydl_opts = {
        'outtmpl': f'{DOWNLOAD_DIR}/%(title)s.%(ext)s',
        'format': 'best',
        'cookies': cookies,  # Automatically get cookies from Chrome
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        video_filename = ydl.prepare_filename(info)

    return send_file(video_filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=False)
