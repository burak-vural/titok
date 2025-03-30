import json
import os
import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# Ensure data directory exists
os.makedirs('data', exist_ok=True)

# File paths
SETTINGS_FILE = 'data/settings.json'
CONTENT_FILE = 'data/content.json'
AD_FILE = 'data/ads.json'
FAQ_FILE = 'data/faqs.json'
ACTIVITY_FILE = 'data/activity.json'
FOOTER_LINKS_FILE = 'data/footer_links.json'
SEO_SETTINGS_FILE = 'data/seo_settings.json'

# Ad types
AD_TYPE_HTML = 'html'
AD_TYPE_IMAGE = 'image'

# Default data
DEFAULT_SETTINGS = {
    'site_title': 'TikTok Video İndirici - Filigransız Video İndir',
    'site_description': 'TikTok videolarını hızlı ve kolay bir şekilde filigransız indirin. Ücretsiz TikTok video indirme aracı.',
    'site_keywords': 'tiktok, video indirici, filigransız, ücretsiz, tiktok video indirme',
    'admin_username': 'admin',
    'admin_password_hash': generate_password_hash('admin123')
}

DEFAULT_CONTENT = [
    {
        'id': 1,
        'title': 'TikTok Video İndirici Hakkında',
        'content': 'TikTok Video İndirici, TikTok videolarını hızlı ve kolay bir şekilde indirmenizi sağlayan ücretsiz bir araçtır. Videolarınızı filigransız olarak indirin ve istediğiniz gibi kullanın.',
        'section': 'main',
        'order': 1,
        'created_at': datetime.datetime.now().isoformat(),
        'updated_at': datetime.datetime.now().isoformat()
    },
    {
        'id': 2,
        'title': 'Neden Bizi Tercih Etmelisiniz?',
        'content': 'Hızlı, güvenli ve kullanımı kolay aracımız ile TikTok videolarını saniyeler içinde indirebilirsiniz. Filigransız videolar, yüksek kalite ve tamamen ücretsiz!',
        'section': 'sidebar',
        'order': 1,
        'created_at': datetime.datetime.now().isoformat(),
        'updated_at': datetime.datetime.now().isoformat()
    }
]

DEFAULT_FAQS = [
    {
        'id': 1,
        'question': 'TikTok videolarını nasıl indirebilirim?',
        'answer': 'TikTok uygulamasından video URL\'sini kopyalayın, sitemize yapıştırın ve \'İndir\' düğmesine tıklayın. Video işlendikten sonra indirme bağlantısı görünecektir.',
        'order': 1,
        'created_at': datetime.datetime.now().isoformat(),
        'updated_at': datetime.datetime.now().isoformat()
    },
    {
        'id': 2,
        'question': 'İndirilen videolarda filigran (watermark) var mı?',
        'answer': 'Hayır, sitemizden indirilen tüm TikTok videoları filigransızdır.',
        'order': 2,
        'created_at': datetime.datetime.now().isoformat(),
        'updated_at': datetime.datetime.now().isoformat()
    },
    {
        'id': 3,
        'question': 'Servis tamamen ücretsiz mi?',
        'answer': 'Evet, TikTok video indirme servisimiz tamamen ücretsizdir ve herhangi bir kayıt gerektirmez.',
        'order': 3,
        'created_at': datetime.datetime.now().isoformat(),
        'updated_at': datetime.datetime.now().isoformat()
    }
]

DEFAULT_ADS = []

DEFAULT_ACTIVITY = [
    {
        'id': 1,
        'action': 'Sistem',
        'detail': 'Sistem ilk kez başlatıldı',
        'date': datetime.datetime.now().isoformat()
    }
]

DEFAULT_FOOTER_LINKS = [
    {
        'id': 1,
        'title': 'Hakkımızda',
        'url': '/hakkimizda',
        'follow_type': 'dofollow',
        'order': 1,
        'created_at': datetime.datetime.now().isoformat(),
        'updated_at': datetime.datetime.now().isoformat()
    },
    {
        'id': 2,
        'title': 'İletişim',
        'url': '/iletisim',
        'follow_type': 'dofollow',
        'order': 2,
        'created_at': datetime.datetime.now().isoformat(),
        'updated_at': datetime.datetime.now().isoformat()
    }
]

DEFAULT_SEO_SETTINGS = {
    # Meta etiketleri
    'meta_title': 'TikTok Video İndirici',
    'meta_description': 'TikTok videolarını hızlı ve kolay bir şekilde filigransız indirin.',
    'meta_keywords': 'tiktok, video indirici, filigransız, ücretsiz, tiktok video indirme',
    
    # Open Graph etiketleri
    'og_title': 'TikTok Video İndirici',
    'og_description': 'TikTok videolarını hızlı ve kolay bir şekilde filigransız indirin.',
    'og_image': 'https://example.com/og-image.jpg',
    
    # Twitter Card etiketleri
    'twitter_card': 'summary',
    'twitter_site': '@example',
    'twitter_creator': '@example',
    
    # Google Search Console doğrulama
    'google_site_verification': '',
    
    # Google Analytics
    'google_analytics_id': '',
    
    # Robots.txt ayarları
    'robots_txt_content': 'User-agent: *\nAllow: /\nDisallow: /admin/\n\nSitemap: https://example.com/sitemap.xml',
    
    # Sitemap ayarları
    'sitemap_auto_generate': True,
    'sitemap_include_images': True,
    'sitemap_frequency': 'weekly',
    'sitemap_priority': '0.8',
    'sitemap_last_modified': datetime.datetime.now().isoformat()
}

def initialize_data():
    """Initialize data files with default values if they don't exist"""
    if not os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
            json.dump(DEFAULT_SETTINGS, f, ensure_ascii=False, indent=4)
    
    if not os.path.exists(CONTENT_FILE):
        with open(CONTENT_FILE, 'w', encoding='utf-8') as f:
            json.dump(DEFAULT_CONTENT, f, ensure_ascii=False, indent=4)
    
    if not os.path.exists(FAQ_FILE):
        with open(FAQ_FILE, 'w', encoding='utf-8') as f:
            json.dump(DEFAULT_FAQS, f, ensure_ascii=False, indent=4)
    
    if not os.path.exists(AD_FILE):
        with open(AD_FILE, 'w', encoding='utf-8') as f:
            json.dump(DEFAULT_ADS, f, ensure_ascii=False, indent=4)
    
    if not os.path.exists(ACTIVITY_FILE):
        with open(ACTIVITY_FILE, 'w', encoding='utf-8') as f:
            json.dump(DEFAULT_ACTIVITY, f, ensure_ascii=False, indent=4)
    
    if not os.path.exists(FOOTER_LINKS_FILE):
        with open(FOOTER_LINKS_FILE, 'w', encoding='utf-8') as f:
            json.dump(DEFAULT_FOOTER_LINKS, f, ensure_ascii=False, indent=4)
    
    if not os.path.exists(SEO_SETTINGS_FILE):
        with open(SEO_SETTINGS_FILE, 'w', encoding='utf-8') as f:
            json.dump(DEFAULT_SEO_SETTINGS, f, ensure_ascii=False, indent=4)

# Settings functions
def get_settings():
    """Get settings from file"""
    try:
        with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return DEFAULT_SETTINGS

def update_settings(settings):
    """Update settings in file"""
    with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
        json.dump(settings, f, ensure_ascii=False, indent=4)

def check_password(password):
    """Check if password matches the stored hash"""
    settings = get_settings()
    return check_password_hash(settings['admin_password_hash'], password)

def set_password(password):
    """Set a new password"""
    settings = get_settings()
    settings['admin_password_hash'] = generate_password_hash(password)
    update_settings(settings)

# Content functions
def get_contents():
    """Get all contents"""
    try:
        with open(CONTENT_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return DEFAULT_CONTENT

def get_content(content_id):
    """Get a specific content by ID"""
    contents = get_contents()
    for content in contents:
        if content['id'] == content_id:
            return content
    return None

def get_contents_by_section(section):
    """Get contents by section"""
    contents = get_contents()
    return [c for c in contents if c['section'] == section]

def add_content(title, content, section, order):
    """Add a new content"""
    contents = get_contents()
    new_id = max([c['id'] for c in contents], default=0) + 1
    
    new_content = {
        'id': new_id,
        'title': title,
        'content': content,
        'section': section,
        'order': order,
        'created_at': datetime.datetime.now().isoformat(),
        'updated_at': datetime.datetime.now().isoformat()
    }
    
    contents.append(new_content)
    
    with open(CONTENT_FILE, 'w', encoding='utf-8') as f:
        json.dump(contents, f, ensure_ascii=False, indent=4)
    
    return new_content

def update_content(content_id, title, content, section, order):
    """Update an existing content"""
    contents = get_contents()
    
    for i, c in enumerate(contents):
        if c['id'] == content_id:
            contents[i]['title'] = title
            contents[i]['content'] = content
            contents[i]['section'] = section
            contents[i]['order'] = order
            contents[i]['updated_at'] = datetime.datetime.now().isoformat()
            
            with open(CONTENT_FILE, 'w', encoding='utf-8') as f:
                json.dump(contents, f, ensure_ascii=False, indent=4)
            
            return contents[i]
    
    return None

def delete_content(content_id):
    """Delete a content by ID"""
    contents = get_contents()
    contents = [c for c in contents if c['id'] != content_id]
    
    with open(CONTENT_FILE, 'w', encoding='utf-8') as f:
        json.dump(contents, f, ensure_ascii=False, indent=4)

# FAQ functions
def get_faqs():
    """Get all FAQs"""
    try:
        with open(FAQ_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return DEFAULT_FAQS

def get_faq(faq_id):
    """Get a specific FAQ by ID"""
    faqs = get_faqs()
    for faq in faqs:
        if faq['id'] == faq_id:
            return faq
    return None

def add_faq(question, answer, order):
    """Add a new FAQ"""
    faqs = get_faqs()
    new_id = max([f['id'] for f in faqs], default=0) + 1
    
    new_faq = {
        'id': new_id,
        'question': question,
        'answer': answer,
        'order': order,
        'created_at': datetime.datetime.now().isoformat(),
        'updated_at': datetime.datetime.now().isoformat()
    }
    
    faqs.append(new_faq)
    
    with open(FAQ_FILE, 'w', encoding='utf-8') as f:
        json.dump(faqs, f, ensure_ascii=False, indent=4)
    
    return new_faq

def update_faq(faq_id, question, answer, order):
    """Update an existing FAQ"""
    faqs = get_faqs()
    
    for i, f in enumerate(faqs):
        if f['id'] == faq_id:
            faqs[i]['question'] = question
            faqs[i]['answer'] = answer
            faqs[i]['order'] = order
            faqs[i]['updated_at'] = datetime.datetime.now().isoformat()
            
            with open(FAQ_FILE, 'w', encoding='utf-8') as f:
                json.dump(faqs, f, ensure_ascii=False, indent=4)
            
            return faqs[i]
    
    return None

def delete_faq(faq_id):
    """Delete a FAQ by ID"""
    faqs = get_faqs()
    faqs = [f for f in faqs if f['id'] != faq_id]
    
    with open(FAQ_FILE, 'w', encoding='utf-8') as f:
        json.dump(faqs, f, ensure_ascii=False, indent=4)

# Ad functions
def get_ads():
    """Get all ads"""
    try:
        with open(AD_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return DEFAULT_ADS

def get_ad(ad_id):
    """Get a specific ad by ID"""
    ads = get_ads()
    for ad in ads:
        if ad['id'] == ad_id:
            return ad
    return None

def get_ad_by_position(position):
    """Get an active ad by position"""
    ads = get_ads()
    active_ads = [a for a in ads if a['status'] == 'active' and a['position'] == position]
    return active_ads[0] if active_ads else None

def add_ad(name, position, code, status, ad_type):
    """Add a new ad"""
    ads = get_ads()
    new_id = max([a['id'] for a in ads], default=0) + 1
    
    new_ad = {
        'id': new_id,
        'name': name,
        'position': position,
        'code': code,
        'status': status,
        'ad_type': ad_type,
        'created_at': datetime.datetime.now().isoformat(),
        'updated_at': datetime.datetime.now().isoformat()
    }
    
    ads.append(new_ad)
    
    with open(AD_FILE, 'w', encoding='utf-8') as f:
        json.dump(ads, f, ensure_ascii=False, indent=4)
    
    return new_ad

def update_ad(ad_id, name, position, code, status, ad_type):
    """Update an existing ad"""
    ads = get_ads()
    
    for i, a in enumerate(ads):
        if a['id'] == ad_id:
            ads[i]['name'] = name
            ads[i]['position'] = position
            ads[i]['code'] = code
            ads[i]['status'] = status
            ads[i]['ad_type'] = ad_type
            ads[i]['updated_at'] = datetime.datetime.now().isoformat()
            
            with open(AD_FILE, 'w', encoding='utf-8') as f:
                json.dump(ads, f, ensure_ascii=False, indent=4)
            
            return ads[i]
    
    return None

def delete_ad(ad_id):
    """Delete an ad by ID"""
    ads = get_ads()
    ads = [a for a in ads if a['id'] != ad_id]
    
    with open(AD_FILE, 'w', encoding='utf-8') as f:
        json.dump(ads, f, ensure_ascii=False, indent=4)

# Footer Links functions
def get_footer_links():
    """Get all footer links"""
    try:
        with open(FOOTER_LINKS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return DEFAULT_FOOTER_LINKS

def get_footer_link(link_id):
    """Get a specific footer link by ID"""
    links = get_footer_links()
    for link in links:
        if link['id'] == link_id:
            return link
    return None

def add_footer_link(title, url, follow_type, order):
    """Add a new footer link"""
    links = get_footer_links()
    new_id = max([l['id'] for l in links], default=0) + 1
    
    new_link = {
        'id': new_id,
        'title': title,
        'url': url,
        'follow_type': follow_type,
        'order': order,
        'created_at': datetime.datetime.now().isoformat(),
        'updated_at': datetime.datetime.now().isoformat()
    }
    
    links.append(new_link)
    
    with open(FOOTER_LINKS_FILE, 'w', encoding='utf-8') as f:
        json.dump(links, f, ensure_ascii=False, indent=4)
    
    return new_link

def update_footer_link(link_id, title, url, follow_type, order):
    """Update an existing footer link"""
    links = get_footer_links()
    
    for i, l in enumerate(links):
        if l['id'] == link_id:
            links[i]['title'] = title
            links[i]['url'] = url
            links[i]['follow_type'] = follow_type
            links[i]['order'] = order
            links[i]['updated_at'] = datetime.datetime.now().isoformat()
            
            with open(FOOTER_LINKS_FILE, 'w', encoding='utf-8') as f:
                json.dump(links, f, ensure_ascii=False, indent=4)
            
            return links[i]
    
    return None

def delete_footer_link(link_id):
    """Delete a footer link by ID"""
    links = get_footer_links()
    links = [l for l in links if l['id'] != link_id]
    
    with open(FOOTER_LINKS_FILE, 'w', encoding='utf-8') as f:
        json.dump(links, f, ensure_ascii=False, indent=4)

# Activity functions
def get_activities(limit=10):
    """Get recent activities with limit"""
    try:
        with open(ACTIVITY_FILE, 'r', encoding='utf-8') as f:
            activities = json.load(f)
            # Sort by date descending and limit
            activities.sort(key=lambda x: x['date'], reverse=True)
            return activities[:limit]
    except:
        return DEFAULT_ACTIVITY

def log_activity(action, detail):
    """Log a new activity"""
    activities = []
    try:
        with open(ACTIVITY_FILE, 'r', encoding='utf-8') as f:
            activities = json.load(f)
    except:
        activities = DEFAULT_ACTIVITY
    
    new_id = max([a['id'] for a in activities], default=0) + 1
    
    new_activity = {
        'id': new_id,
        'action': action,
        'detail': detail,
        'date': datetime.datetime.now().isoformat()
    }
    
    activities.append(new_activity)
    
    with open(ACTIVITY_FILE, 'w', encoding='utf-8') as f:
        json.dump(activities, f, ensure_ascii=False, indent=4)
    
    return new_activity

# SEO Settings functions
def get_seo_settings():
    """Get SEO settings from file"""
    try:
        with open(SEO_SETTINGS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return DEFAULT_SEO_SETTINGS

def update_seo_settings(settings):
    """Update SEO settings in file"""
    with open(SEO_SETTINGS_FILE, 'w', encoding='utf-8') as f:
        json.dump(settings, f, ensure_ascii=False, indent=4)

# Initialize data on import
initialize_data()
