from flask import Flask, request, jsonify, render_template
from youtube_transcript_api import YouTubeTranscriptApi

app = Flask(__name__)

def get_transcript(video_url):
    try:
        video_id = video_url.split("v=")[-1]
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return transcript
    except Exception as e:
        return str(e)

@app.route('/')
def index():
    return render_template('index.html')  # HTML form for input

@app.route('/transcript', methods=['POST'])
def transcript():
    video_url = request.form.get('video_url')
    if not video_url:
        return jsonify({"error": "No YouTube URL provided"}), 400

    transcript_data = get_transcript(video_url)
    if isinstance(transcript_data, str):  # Handle error as string
        return jsonify({"error": transcript_data}), 400
    return jsonify(transcript_data)

if __name__ == '__main__':
    app.run(debug=True)
