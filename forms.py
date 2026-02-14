from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, FloatField, DateField
from wtforms.validators import DataRequired, IPAddress, Optional

class AssetForm(FlaskForm):
    name = StringField('Asset Name', validators=[DataRequired()])
    asset_type = SelectField('Type', choices=[('Server','Server'), ('Laptop','Laptop'), ('Router','Router'), ('Other','Other')])
    ip_address = StringField('IP Address', validators=[Optional(), IPAddress()])
    location = StringField('Location')
    purchase_date = DateField('Purchase Date', format='%Y-%m-%d', validators=[Optional()])
    notes = TextAreaField('Notes')

class SecurityNoteForm(FlaskForm):
    note = TextAreaField('Note', validators=[DataRequired()])
    severity = SelectField('Severity', choices=[('Low','Low'), ('Medium','Medium'), ('High','High')])

class CapacityForm(FlaskForm):
    total_gb = FloatField('Total (GB)', validators=[DataRequired()])
    used_gb = FloatField('Used (GB)', validators=[DataRequired()])

class BackupForm(FlaskForm):
    backup_date = DateField('Backup Date', format='%Y-%m-%d', validators=[DataRequired()])
    status = SelectField('Status', choices=[('Success','Success'), ('Failed','Failed')])
    location = StringField('Location')
    notes = TextAreaField('Notes')