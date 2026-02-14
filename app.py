from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Asset, AvailabilityLog, SecurityNote, CapacityRecord, BackupLog
from forms import AssetForm, SecurityNoteForm, CapacityForm, BackupForm
from ping3 import ping
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///assets.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Create tables if they don't exist
with app.app_context():
    db.create_all()

# ------------------- Helper function for ping -------------------
def ping_asset(ip):
    """Returns (status, response_time)"""
    if not ip:
        return 'down', None
    try:
        response = ping(ip, timeout=2, unit='ms')
        if response is None:
            return 'down', None
        else:
            return 'up', round(response, 2)
    except Exception:
        return 'down', None

# ------------------- Routes -------------------

@app.route('/')
def index():
    assets = Asset.query.all()
    recent_logs = AvailabilityLog.query.order_by(AvailabilityLog.timestamp.desc()).limit(10).all()
    return render_template('index.html', assets=assets, recent_logs=recent_logs)

# Asset CRUD
@app.route('/assets')
def assets():
    assets = Asset.query.all()
    return render_template('assets.html', assets=assets)

@app.route('/assets/add', methods=['GET', 'POST'])
def add_asset():
    form = AssetForm()
    if form.validate_on_submit():
        asset = Asset(
            name=form.name.data,
            asset_type=form.asset_type.data,
            ip_address=form.ip_address.data,
            location=form.location.data,
            purchase_date=form.purchase_date.data,
            notes=form.notes.data
        )
        db.session.add(asset)
        db.session.commit()
        flash('Asset added successfully', 'success')
        return redirect(url_for('assets'))
    return render_template('asset_form.html', form=form, title='Add Asset')

@app.route('/assets/edit/<int:id>', methods=['GET', 'POST'])
def edit_asset(id):
    asset = Asset.query.get_or_404(id)
    form = AssetForm(obj=asset)
    if form.validate_on_submit():
        form.populate_obj(asset)
        db.session.commit()
        flash('Asset updated', 'success')
        return redirect(url_for('assets'))
    return render_template('asset_form.html', form=form, title='Edit Asset')

@app.route('/assets/delete/<int:id>')
def delete_asset(id):
    asset = Asset.query.get_or_404(id)
    db.session.delete(asset)
    db.session.commit()
    flash('Asset deleted', 'success')
    return redirect(url_for('assets'))

# Availability: check ping for a specific asset and log it
@app.route('/check_availability/<int:id>')
def check_availability(id):
    asset = Asset.query.get_or_404(id)
    if asset.ip_address:
        status, rtt = ping_asset(asset.ip_address)
        log = AvailabilityLog(asset_id=asset.id, status=status, response_time=rtt)
        db.session.add(log)
        db.session.commit()
        flash(f'Ping check: {status.upper()} (Response: {rtt} ms)' if rtt else f'Ping check: {status.upper()}', 'info')
    else:
        flash('Asset has no IP address', 'warning')
    return redirect(url_for('asset_detail', id=id))

# View asset details (with all related logs)
@app.route('/asset/<int:id>')
def asset_detail(id):
    asset = Asset.query.get_or_404(id)
    return render_template('asset_detail.html', asset=asset)

# Security notes
@app.route('/asset/<int:id>/security/add', methods=['GET', 'POST'])
def add_security_note(id):
    asset = Asset.query.get_or_404(id)
    form = SecurityNoteForm()
    if form.validate_on_submit():
        note = SecurityNote(
            asset_id=asset.id,
            note=form.note.data,
            severity=form.severity.data
        )
        db.session.add(note)
        db.session.commit()
        flash('Security note added', 'success')
        return redirect(url_for('asset_detail', id=id))
    return render_template('security_form.html', form=form, asset=asset)

# Capacity
@app.route('/asset/<int:id>/capacity/add', methods=['GET', 'POST'])
def add_capacity(id):
    asset = Asset.query.get_or_404(id)
    form = CapacityForm()
    if form.validate_on_submit():
        record = CapacityRecord(
            asset_id=asset.id,
            total_gb=form.total_gb.data,
            used_gb=form.used_gb.data
        )
        db.session.add(record)
        db.session.commit()
        flash('Capacity record added', 'success')
        return redirect(url_for('asset_detail', id=id))
    return render_template('capacity_form.html', form=form, asset=asset)

# Backups
@app.route('/asset/<int:id>/backup/add', methods=['GET', 'POST'])
def add_backup(id):
    asset = Asset.query.get_or_404(id)
    form = BackupForm()
    if form.validate_on_submit():
        backup = BackupLog(
            asset_id=asset.id,
            backup_date=form.backup_date.data,
            status=form.status.data,
            location=form.location.data,
            notes=form.notes.data
        )
        db.session.add(backup)
        db.session.commit()
        flash('Backup log added', 'success')
        return redirect(url_for('asset_detail', id=id))
    return render_template('backup_form.html', form=form, asset=asset)

if __name__ == '__main__':
    app.run(debug=True)