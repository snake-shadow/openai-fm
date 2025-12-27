from flask import Flask, request, send_file
import requests
import os
from io import BytesIO

app = Flask(__name__)

TTS_URL = "https://api.ttsopenai.com/uapi/v1/text-to-speech"
API_KEY = os.getenv("TTSOPENAI_KEY")  # must match your Render env var name

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        text = request.form["text"]
        voice_id = request.form.get("voice_id", "OA001")

        headers = {
            "Content-Type": "application/json",
            "x-api-key": API_KEY
        }
        data = {
            "model": "tts-1",
            "voice_id": voice_id,
            "speed": 1.0,
            "input": text
        }

        response = requests.post(TTS_URL, headers=headers, json=data)

        # NEW: show real error instead of silently failing
        if response.status_code != 200:
            return f"TTS API error {response.status_code}: {response.text}", 500

        return send_file(
            BytesIO(response.content),
            mimetype="audio/mpeg",
            as_attachment=True,
            download_name="speech.mp3"
        )

    # simple HTML form
    return '''
    <h1>TTSOpenAI Web Service</h1>
    <form method="post">
        <textarea name="text" rows="5" cols="50" placeholder="Enter text...">
Hello! Walk 20 steps to the coffee shop.
        </textarea><br>
        <input type="text" name="voice_id" value="OA001" placeholder="Voice ID"><br>
        <button type="submit">Generate MP3</button>
    </form>
    '''

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
