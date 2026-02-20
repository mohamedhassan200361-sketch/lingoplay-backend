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
        
        # إعدادات متقدمة جداً للتمويه وتخطي الحظر
        ydl_opts = {
            'format': 'best[ext=mp4]/best', # ضمان صيغة مدعومة
            'quiet': True,
            'no_warnings': True,
            'nocheckcertificate': True,
            'ignoreerrors': False,
            'logtostderr': False,
            'add_header': [
                'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                'Accept-Language: en-US,en;q=0.5',
            ],
            # التمويه كأنه متصفح حقيقي
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # محاولة جلب البيانات مع تخطي القيود
            info = ydl.extract_info(video_url, download=False)
            if 'url' in info:
                return jsonify({'url': info['url']})
            else:
                # لو الرابط مطلعش مباشرة، نجربه من الـ formats
                formats = info.get('formats', [])
                for f in formats:
                    if f.get('acodec') != 'none' and f.get('vcodec') != 'none':
                        return jsonify({'url': f['url']})
                
        return jsonify({'error': 'Could not find a valid stream'}), 404

    except Exception as e:
        print(f"Internal Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
