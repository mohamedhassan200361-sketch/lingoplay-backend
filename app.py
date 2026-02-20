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
        
        # إعدادات متقدمة لتخطي حماية يوتيوب
        ydl_opts = {
            'format': 'best',
            'quiet': True,
            'no_warnings': True,
            'source_address': '0.0.0.0', # إجبار استخدام IPv4
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
                'Accept': '*/*',
                'Accept-Language': 'en-US,en;q=0.5',
            }
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            return jsonify({'url': info['url']})

    except Exception as e:
        # طباعة الخطأ في سجلات السيرفر عشان نعرف المشكلة فين
        print(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
