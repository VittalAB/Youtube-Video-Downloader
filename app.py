''''
Created by Vittal Badami
Desc : - This is free youtube video downloader using pytube library.

'''

from flask import *
from pytube import YouTube as yt
import os
from datetime import datetime
from flask import current_app
import shutil

app = Flask(__name__)

audio_no = 0
video_no = 0

i = 0

if not os.path.exists('audios'):
    os.mkdir('audios')
if not os.path.exists('videos'):
    os.mkdir('videos')


def download_audio(link):
    global i
    if len(os.listdir('audios')) > 5 or f'{i}_.mp4' in os.listdir('audios'):
        shutil.rmtree('audios')
        os.mkdir('audios')
    url = yt(str(link))
    video = url.streams.filter(only_audio=True).first()
    out_file = video.download(output_path="./audios", filename=str(i)+'_.mp3')
    os.system(
        f'ffmpeg -loop 1 -r 1 -i static/images/flyer.jpg -i audios/{i}_.mp3 -c:a copy -shortest -c:v libx264 audios/{i}_.mp4')
    os.remove(out_file)
    ret_file = f'audios/{i}_.mp4'
    i = (i+1) % 5
    with open("history.txt", "a") as myfile:
        myfile.write(
            "\n" + f"{datetime.now().strftime('%d/%m/%y__%H:%M:%S')} --> {link}" + "\n")
    return ret_file


def download_video(link):

    global i

    if len(os.listdir('videos')) > 2:
        shutil.rmtree('videos')
        os.mkdir('videos')

    url = yt(str(link))
    video = url.streams.get_lowest_resolution()
    
    out_file = video.download(output_path='./videos', filename=str(i)+'_.mp4')

    if os.name=='posix':
        ret_file = f'videos/{i}_.mp4'
    else:
        ret_file = f'videos//{i}_.mp4'

    i = (i+1) % 2
    with open("history.txt", "a") as myfile:
        myfile.write(
            "\n" + f"{datetime.now().strftime('%d/%m/%y__%H:%M:%S')} --> {link}" + "\n")
    return ret_file

# home page


@app.route('/')
def hello_world():
    return render_template('index.html')

# for audio downloading


@app.route('/submit_audio', methods=['POST'])
def submit_audio():
    data = request.form.get('link')
    print(data)
    write_path = download_audio(data)
    print(write_path)
    return send_file(write_path, as_attachment=True)


# for video downloading
@app.route('/submit', methods=['POST', 'GET'])
def submit():
    data = request.form.get('link')
    print(data)
    write_path = download_video(data)
    print(write_path)
    return send_file(write_path, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=False, port=5000, host="0.0.0.0")
