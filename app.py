from flask import Flask, request, jsonify, send_from_directory
import os
import requests
import re
import json
from urllib.parse import urlparse
import random
import string

app = Flask(__name__, static_folder='static')

# Ensure the downloads directory exists
os.makedirs('downloads', exist_ok=True)

def generate_random_string(length=10):
    """Generate a random string for filenames"""
    letters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(letters) for i in range(length))

def get_tiktok_video_id(url):
    """Extract the TikTok video ID from the URL"""
    # Handle different URL formats
    if '/video/' in url:
        video_id = url.split('/video/')[1].split('?')[0]
    elif '/v/' in url:
        video_id = url.split('/v/')[1].split('?')[0]
    else:
        # Try to find a numeric ID in the URL
        match = re.search(r'(\d{19})', url)
        if match:
            video_id = match.group(1)
        else:
            raise ValueError("Could not extract video ID from URL")
    
    return video_id

def download_tiktok_video(url):
    """Download TikTok video without watermark"""
    try:
        # First, we need to get the TikTok video ID
        video_id = get_tiktok_video_id(url)
        
        # Use a different approach with a public API service
        api_url = f"https://www.tikwm.com/api/?url={url}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        
        response = requests.get(api_url, headers=headers)
        
        if response.status_code != 200:
            raise Exception("Failed to fetch video information")
        
        data = response.json()
        
        if data.get('code') != 0:
            raise Exception(data.get('msg', 'Failed to process video'))
        
        # Extract video URLs from the API response
        try:
            video_data = data.get('data', {})
            
            # URL with watermark (original video)
            watermark_url = video_data.get('origin_cover')
            
            # URL without watermark
            no_watermark_url = video_data.get('play')
            
            if not no_watermark_url:
                raise Exception("Could not find video download URL")
            
            # Download both versions
            random_id = generate_random_string()
            no_watermark_path = f"downloads/tiktok_no_watermark_{random_id}.mp4"
            
            # Download without watermark
            with open(no_watermark_path, 'wb') as f:
                f.write(requests.get(no_watermark_url, headers=headers).content)
            
            return {
                'success': True,
                'videoUrl': f'/downloads/tiktok_no_watermark_{random_id}.mp4',  # For preview
                'noWatermarkUrl': f'/downloads/tiktok_no_watermark_{random_id}.mp4',
                'noWatermarkPath': no_watermark_path
            }
            
        except (KeyError, IndexError) as e:
            raise Exception(f"Failed to extract video URLs: {str(e)}")
    
    except Exception as e:
        return {'success': False, 'message': str(e)}

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/downloads/<path:filename>')
def download_file(filename):
    return send_from_directory('downloads', filename, as_attachment=True)

@app.route('/api/download', methods=['POST'])
def api_download():
    data = request.json
    url = data.get('url')
    
    if not url:
        return jsonify({'success': False, 'message': 'URL is required'}), 400
    
    result = download_tiktok_video(url)
    
    if result['success']:
        return jsonify(result)
    else:
        return jsonify(result), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
