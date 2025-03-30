from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Settings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    site_title = db.Column(db.String(100), default="TikTok Video İndirici - Filigransız Video İndir")
    site_description = db.Column(db.Text, default="TikTok videolarını hızlı ve kolay bir şekilde filigransız indirin. Ücretsiz TikTok video indirme aracı.")
    site_keywords = db.Column(db.String(200), default="tiktok, video indirici, filigransız, ücretsiz, tiktok video indirme")
    admin_username = db.Column(db.String(50), default="admin")
    admin_password_hash = db.Column(db.String(200))
    
    def set_password(self, password):
        self.admin_password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.admin_password_hash, password)

class Content(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    section = db.Column(db.String(20), default="main")  # main, sidebar, steps
    order = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Ad(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(20), nullable=False)  # horizontal-top, horizontal-middle, horizontal-bottom, sidebar-top, sidebar-bottom
    code = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(10), default="active")  # active, inactive
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class FAQ(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(200), nullable=False)
    answer = db.Column(db.Text, nullable=False)
    order = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(50), nullable=False)
    detail = db.Column(db.String(200), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    
    @classmethod
    def log(cls, action, detail):
        activity = cls(action=action, detail=detail)
        db.session.add(activity)
        db.session.commit()
