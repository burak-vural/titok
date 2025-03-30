from flask import Flask, request, jsonify, send_file, render_template, redirect, url_for, session, flash, make_response
import requests
import os
import re
import json
import urllib.parse
from io import BytesIO
import random
import string
import datetime
from werkzeug.utils import secure_filename
from functools import wraps
import admin_data as data

app = Flask(__name__)
app.secret_key = 'tiktok_video_downloader_secret_key'
app.config['UPLOAD_FOLDER'] = 'static/uploads/ads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
app.config['SECRET_KEY'] = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(32))

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Ensure the downloads directory exists
os.makedirs('downloads', exist_ok=True)

def generate_random_string(length=10):
    """Generate a random string for filenames"""
    letters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(letters) for i in range(length))

# Admin login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_logged_in' not in session:
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    # Get content from database
    settings = data.get_settings()
    main_contents = data.get_contents_by_section('main')
    sidebar_contents = data.get_contents_by_section('sidebar')
    steps_contents = data.get_contents_by_section('steps')
    faqs = data.get_faqs()
    footer_links = data.get_footer_links()
    seo_settings = data.get_seo_settings()
    
    # Sort footer links by order
    footer_links = sorted(footer_links, key=lambda x: x['order'])
    
    # Get active ads
    horizontal_top_ad = data.get_ad_by_position('horizontal-top')
    horizontal_middle_ad = data.get_ad_by_position('horizontal-middle')
    horizontal_bottom_ad = data.get_ad_by_position('horizontal-bottom')
    horizontal_footer_1_ad = data.get_ad_by_position('horizontal-footer-1')
    horizontal_footer_2_ad = data.get_ad_by_position('horizontal-footer-2')
    sidebar_top_ad = data.get_ad_by_position('sidebar-top')
    sidebar_bottom_ad = data.get_ad_by_position('sidebar-bottom')
    
    return render_template(
        'index.html',
        settings=settings,
        main_contents=main_contents,
        sidebar_contents=sidebar_contents,
        steps_contents=steps_contents,
        faqs=faqs,
        footer_links=footer_links,
        seo_settings=seo_settings,
        horizontal_top_ad=horizontal_top_ad,
        horizontal_middle_ad=horizontal_middle_ad,
        horizontal_bottom_ad=horizontal_bottom_ad,
        horizontal_footer_1_ad=horizontal_footer_1_ad,
        horizontal_footer_2_ad=horizontal_footer_2_ad,
        sidebar_top_ad=sidebar_top_ad,
        sidebar_bottom_ad=sidebar_bottom_ad
    )

@app.route('/api/download', methods=['POST'])
def api_download():
    data_json = request.json
    url = data_json.get('url')
    
    if not url:
        return jsonify({'success': False, 'message': 'URL is required'}), 400
    
    try:
        # Use a different approach with a public API service
        api_url = f"https://www.tikwm.com/api/?url={url}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        
        response = requests.get(api_url, headers=headers)
        
        if response.status_code != 200:
            return jsonify({'success': False, 'message': 'Failed to fetch video information'}), 400
        
        data_response = response.json()
        
        if data_response.get('code') != 0:
            return jsonify({'success': False, 'message': data_response.get('msg', 'Failed to process video')}), 400
        
        # Extract video URLs from the API response
        video_data = data_response.get('data', {})
        
        # URL without watermark
        no_watermark_url = video_data.get('play')
        
        if not no_watermark_url:
            return jsonify({'success': False, 'message': 'Could not find video download URL'}), 400
        
        # Download the video to a temporary file
        random_id = generate_random_string()
        file_path = f"downloads/tiktok_video_{random_id}.mp4"
        
        # Download the video
        video_response = requests.get(no_watermark_url, headers=headers)
        
        if video_response.status_code != 200:
            return jsonify({'success': False, 'message': 'Failed to download video'}), 400
        
        # Save the video
        with open(file_path, 'wb') as f:
            f.write(video_response.content)
        
        # Log activity
        data.log_activity("Video İndirme", f"Yeni bir video indirildi: {url[:30]}...")
        
        return jsonify({
            'success': True,
            'videoUrl': f'/download/{random_id}',  # For preview
            'downloadUrl': f'/download/{random_id}?download=true'  # For download
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/download/<video_id>')
def download_video(video_id):
    file_path = f"downloads/tiktok_video_{video_id}.mp4"
    
    if not os.path.exists(file_path):
        return "Video not found", 404
    
    # Check if this is a download request
    download = request.args.get('download', 'false').lower() == 'true'
    
    if download:
        # Force the browser to download the file
        return send_file(
            file_path,
            as_attachment=True,
            download_name="tiktok_video.mp4",
            mimetype='video/mp4'
        )
    else:
        # Just stream the video for preview
        return send_file(file_path, mimetype='video/mp4')

# Admin Routes
@app.route('/admin')
@login_required
def admin_panel():
    if 'admin_logged_in' not in session:
        return redirect(url_for('admin_login'))
    
    settings = data.get_settings()
    contents = data.get_contents()
    ads = data.get_ads()
    faqs = data.get_faqs()
    footer_links = data.get_footer_links()
    activities = data.get_activities()
    seo_settings = data.get_seo_settings()
    
    # Sayaçları hesapla
    content_count = len(contents)
    ad_count = len(ads)
    faq_count = len(faqs)
    footer_link_count = len(footer_links)
    
    return render_template(
        'admin_panel.html',
        settings=settings,
        contents=contents,
        ads=ads,
        faqs=faqs,
        footer_links=footer_links,
        activities=activities,
        content_count=content_count,
        ad_count=ad_count,
        faq_count=faq_count,
        footer_link_count=footer_link_count,
        seo_settings=seo_settings
    )

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        settings = data.get_settings()
        
        if settings and settings['admin_username'] == username and data.check_password(password):
            session.clear()  # Önceki oturum verilerini temizle
            session['admin_logged_in'] = True
            app.logger.info(f"Admin giriş başarılı: {username}")
            data.log_activity("Giriş", f"Admin paneline giriş yapıldı: {username}")
            return redirect(url_for('admin_panel'))
        else:
            app.logger.warning(f"Başarısız admin giriş denemesi: {username}")
            return render_template('admin_login.html', error='invalid')
    
    return render_template('admin_login.html')

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('admin_login'))

# Content Management Routes
@app.route('/admin/content/add', methods=['POST'])
@login_required
def add_content():
    title = request.form.get('title')
    content_text = request.form.get('content')
    section = request.form.get('section')
    order = int(request.form.get('order', 1))
    
    data.add_content(title, content_text, section, order)
    data.log_activity("İçerik Ekleme", f"Yeni içerik eklendi: {title}")
    
    session['success_message'] = "İçerik başarıyla eklendi."
    return redirect(url_for('admin_panel'))

@app.route('/admin/content/edit/<int:content_id>', methods=['GET', 'POST'])
@login_required
def edit_content(content_id):
    content = data.get_content(content_id)
    
    if not content:
        session['error_message'] = "İçerik bulunamadı."
        return redirect(url_for('admin_panel'))
    
    if request.method == 'POST':
        title = request.form.get('title')
        content_text = request.form.get('content')
        section = request.form.get('section')
        order = int(request.form.get('order', 1))
        
        data.update_content(content_id, title, content_text, section, order)
        data.log_activity("İçerik Düzenleme", f"İçerik düzenlendi: {title}")
        
        session['success_message'] = "İçerik başarıyla güncellendi."
        return redirect(url_for('admin_panel'))
    
    return render_template(
        'admin_edit_content.html',
        content=content
    )

@app.route('/admin/content/delete/<int:content_id>')
@login_required
def delete_content(content_id):
    content = data.get_content(content_id)
    
    if not content:
        session['error_message'] = "İçerik bulunamadı."
        return redirect(url_for('admin_panel'))
    
    data.delete_content(content_id)
    data.log_activity("İçerik Silme", f"İçerik silindi: {content['title']}")
    
    session['success_message'] = "İçerik başarıyla silindi."
    return redirect(url_for('admin_panel'))

# Ad Management Routes
@app.route('/admin/ad/add', methods=['POST'])
@login_required
def add_ad():
    name = request.form.get('name')
    position = request.form.get('position')
    ad_type = request.form.get('ad_type')
    status = request.form.get('status')
    link = request.form.get('link', '')
    
    if ad_type == 'image':
        file = request.files.get('image')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Resim için HTML kodu oluştur
            if link:
                code = f'<a href="{link}" target="_blank"><img src="/static/uploads/ads/{filename}" style="max-width:100%;" alt="{name}"></a>'
            else:
                code = f'<img src="/static/uploads/ads/{filename}" style="max-width:100%;" alt="{name}">'
        else:
            session['error_message'] = "Geçersiz dosya formatı. Lütfen PNG, JPG veya GIF yükleyin."
            return redirect(url_for('admin_panel'))
    else:  # HTML kodu
        code = request.form.get('code', '')
    
    data.add_ad(name, position, code, status, ad_type)
    data.log_activity("Reklam Ekleme", f"Reklam eklendi: {name}")
    
    session['success_message'] = "Reklam başarıyla eklendi."
    return redirect(url_for('admin_panel'))

@app.route('/admin/ad/edit/<int:ad_id>', methods=['GET', 'POST'])
@login_required
def edit_ad(ad_id):
    ad = data.get_ad(ad_id)
    
    if not ad:
        session['error_message'] = "Reklam bulunamadı."
        return redirect(url_for('admin_panel'))
    
    if request.method == 'POST':
        name = request.form.get('name')
        position = request.form.get('position')
        ad_type = request.form.get('ad_type')
        status = request.form.get('status')
        link = request.form.get('link', '')
        
        if ad_type == 'image':
            file = request.files.get('image')
            if file and file.filename and allowed_file(file.filename):
                # Yeni resim yüklendi
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                
                # Resim için HTML kodu oluştur
                if link:
                    code = f'<a href="{link}" target="_blank"><img src="/static/uploads/ads/{filename}" style="max-width:100%;" alt="{name}"></a>'
                else:
                    code = f'<img src="/static/uploads/ads/{filename}" style="max-width:100%;" alt="{name}">'
            else:
                # Resim değiştirilmedi, mevcut kodu kullan
                code = ad['code']
        else:  # HTML kodu
            code = request.form.get('code', '')
        
        data.update_ad(ad_id, name, position, code, status, ad_type)
        data.log_activity("Reklam Düzenleme", f"Reklam düzenlendi: {name}")
        
        session['success_message'] = "Reklam başarıyla güncellendi."
        return redirect(url_for('admin_panel'))
    
    return render_template(
        'admin_edit_ad.html',
        ad=ad
    )

@app.route('/admin/ad/delete/<int:ad_id>')
@login_required
def delete_ad(ad_id):
    ad = data.get_ad(ad_id)
    
    if not ad:
        session['error_message'] = "Reklam bulunamadı."
        return redirect(url_for('admin_panel'))
    
    data.delete_ad(ad_id)
    data.log_activity("Reklam Silme", f"Reklam silindi: {ad['name']}")
    
    session['success_message'] = "Reklam başarıyla silindi."
    return redirect(url_for('admin_panel'))

# FAQ Management Routes
@app.route('/admin/faq/add', methods=['POST'])
@login_required
def add_faq():
    question = request.form.get('question')
    answer = request.form.get('answer')
    order = int(request.form.get('order', 1))
    
    data.add_faq(question, answer, order)
    data.log_activity("SSS Ekleme", f"Yeni SSS eklendi: {question[:30]}...")
    
    session['success_message'] = "SSS başarıyla eklendi."
    return redirect(url_for('admin_panel'))

@app.route('/admin/faq/edit/<int:faq_id>', methods=['GET', 'POST'])
@login_required
def edit_faq(faq_id):
    faq = data.get_faq(faq_id)
    
    if not faq:
        session['error_message'] = "SSS bulunamadı."
        return redirect(url_for('admin_panel'))
    
    if request.method == 'POST':
        question = request.form.get('question')
        answer = request.form.get('answer')
        order = int(request.form.get('order', 1))
        
        data.update_faq(faq_id, question, answer, order)
        data.log_activity("SSS Düzenleme", f"SSS düzenlendi: {question[:30]}...")
        
        session['success_message'] = "SSS başarıyla güncellendi."
        return redirect(url_for('admin_panel'))
    
    return render_template(
        'admin_edit_faq.html',
        faq=faq
    )

@app.route('/admin/faq/delete/<int:faq_id>')
@login_required
def delete_faq(faq_id):
    faq = data.get_faq(faq_id)
    
    if not faq:
        session['error_message'] = "SSS bulunamadı."
        return redirect(url_for('admin_panel'))
    
    data.delete_faq(faq_id)
    data.log_activity("SSS Silme", f"SSS silindi: {faq['question'][:30]}...")
    
    session['success_message'] = "SSS başarıyla silindi."
    return redirect(url_for('admin_panel'))

# Footer Link Management Routes
@app.route('/admin/footer-link/add', methods=['POST'])
@login_required
def add_footer_link():
    title = request.form.get('title')
    url = request.form.get('url')
    follow_type = request.form.get('follow_type', 'dofollow')
    order = int(request.form.get('order', 1))
    
    data.add_footer_link(title, url, follow_type, order)
    data.log_activity("Footer Link Ekleme", f"Yeni footer link eklendi: {title}")
    
    return redirect(url_for('admin_panel'))

@app.route('/admin/footer-link/edit/<int:link_id>', methods=['GET', 'POST'])
@login_required
def edit_footer_link(link_id):
    footer_link = data.get_footer_link(link_id)
    
    if not footer_link:
        return redirect(url_for('admin_panel'))
    
    if request.method == 'POST':
        title = request.form.get('title')
        url = request.form.get('url')
        follow_type = request.form.get('follow_type', 'dofollow')
        order = int(request.form.get('order', 1))
        
        data.update_footer_link(link_id, title, url, follow_type, order)
        data.log_activity("Footer Link Düzenleme", f"Footer link güncellendi: {title}")
        
        return redirect(url_for('admin_panel'))
    
    return render_template('admin_edit_footer_link.html', footer_link=footer_link)

@app.route('/admin/footer-link/delete/<int:link_id>')
@login_required
def delete_footer_link(link_id):
    footer_link = data.get_footer_link(link_id)
    
    if footer_link:
        data.delete_footer_link(link_id)
        data.log_activity("Footer Link Silme", f"Footer link silindi: {footer_link['title']}")
    
    return redirect(url_for('admin_panel'))

# Settings Management Route
@app.route('/admin/settings/update', methods=['POST'])
@login_required
def update_settings():
    settings = data.get_settings()
    
    settings['site_title'] = request.form.get('site_title')
    settings['site_description'] = request.form.get('site_description')
    settings['site_keywords'] = request.form.get('site_keywords')
    settings['admin_username'] = request.form.get('admin_username')
    
    # Update password only if provided
    new_password = request.form.get('admin_password')
    if new_password:
        data.set_password(new_password)
    
    data.update_settings(settings)
    data.log_activity("Ayarlar", "Site ayarları güncellendi")
    
    session['success_message'] = "Ayarlar başarıyla güncellendi."
    return redirect(url_for('admin_panel'))

@app.route('/sitemap.xml')
def sitemap():
    seo_settings = data.get_seo_settings()
    
    # XML başlığı ve kök eleman
    xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml_content += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n'
    xml_content += '        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n'
    
    # Ana sayfa URL'si
    xml_content += '    <url>\n'
    xml_content += f'        <loc>{request.url_root}</loc>\n'
    xml_content += f'        <lastmod>{seo_settings["sitemap_last_modified"]}</lastmod>\n'
    xml_content += f'        <changefreq>{seo_settings["sitemap_frequency"]}</changefreq>\n'
    xml_content += f'        <priority>{seo_settings["sitemap_priority"]}</priority>\n'
    xml_content += '    </url>\n'
    
    # XML kapanış etiketi
    xml_content += '</urlset>'
    
    # XML içeriğini döndür
    response = make_response(xml_content)
    response.headers['Content-Type'] = 'application/xml'
    return response

@app.route('/robots.txt')
def robots():
    seo_settings = data.get_seo_settings()
    
    # Robots.txt içeriğini döndür
    response = make_response(seo_settings['robots_txt_content'])
    response.headers['Content-Type'] = 'text/plain'
    return response

# SEO Ayarları Yönetimi
@app.route('/admin/seo-settings/update', methods=['POST'])
@login_required
def update_seo_settings():
    # Mevcut SEO ayarlarını al
    seo_settings = data.get_seo_settings()
    
    # Form verilerini al
    for key in seo_settings.keys():
        if key in request.form:
            # Boolean değerler için özel işlem
            if key in ['sitemap_auto_generate', 'sitemap_include_images']:
                seo_settings[key] = request.form.get(key) == 'on'
            else:
                seo_settings[key] = request.form.get(key)
    
    # Sitemap son güncelleme tarihini güncelle
    seo_settings['sitemap_last_modified'] = datetime.datetime.now().isoformat()
    
    # SEO ayarlarını kaydet
    data.update_seo_settings(seo_settings)
    
    # Aktivite kaydı ekle
    data.log_activity("SEO Ayarları", "SEO ayarları güncellendi")
    
    return redirect(url_for('admin_panel'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
