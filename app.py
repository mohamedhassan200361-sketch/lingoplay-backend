from flask import Flask, request, jsonify
import yt_dlp
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "LingoPlay Server is Live!"

@app.route('/get_stream', methods=['POST'])
def get_stream():
    try:
        data = request.get_json()
        video_url = data.get('url')
        
        ydl_opts = {
            'format': 'best',
            'quiet': True,
            'no_warnings': True,
            'nocheckcertificate': True,
            # محاولة تخطي الحظر الجغرافي
            'geo_bypass': True,
            'geo_bypass_country': 'US', # جرب تخليه US أو SA (السعودية) لو الفيديو عربي
            'add_header': [
                'Accept-Language: en-US,en;q=0.5',
            ],
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            stream_url = info.get('url') or info.get('formats', [{}])[0].get('url')
            
            if stream_url:
                return jsonify({'url': stream_url})
            return jsonify({'error': 'No URL found'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
