from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Asset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    asset_type = db.Column(db.String(50))        # e.g., Server, Laptop, Router
    ip_address = db.Column(db.String(15), unique=True)
    location = db.Column(db.String(100))
    purchase_date = db.Column(db.Date)
    notes = db.Column(db.Text)

    # Relationships
    availability_logs = db.relationship('AvailabilityLog', backref='asset', lazy=True, cascade="all, delete-orphan")
    security_notes = db.relationship('SecurityNote', backref='asset', lazy=True, cascade="all, delete-orphan")
    capacity_records = db.relationship('CapacityRecord', backref='asset', lazy=True, cascade="all, delete-orphan")
    backup_logs = db.relationship('BackupLog', backref='asset', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Asset {self.name}>'

class AvailabilityLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    asset_id = db.Column(db.Integer, db.ForeignKey('asset.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20))            # 'up' or 'down'
    response_time = db.Column(db.Float)          # in ms, optional

class SecurityNote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    asset_id = db.Column(db.Integer, db.ForeignKey('asset.id'), nullable=False)
    date = db.Column(db.Date, default=datetime.utcnow)
    note = db.Column(db.Text, nullable=False)
    severity = db.Column(db.String(20))          # e.g., Low, Medium, High

class CapacityRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    asset_id = db.Column(db.Integer, db.ForeignKey('asset.id'), nullable=False)
    date = db.Column(db.Date, default=datetime.utcnow)
    total_gb = db.Column(db.Float)
    used_gb = db.Column(db.Float)

class BackupLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    asset_id = db.Column(db.Integer, db.ForeignKey('asset.id'), nullable=False)
    backup_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20))            # Success, Failed
    location = db.Column(db.String(200))          # Where backup is stored
    notes = db.Column(db.Text)