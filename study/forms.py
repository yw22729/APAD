from flask_wtf import FlaskForm
from wtforms import StringField, validators, DateTimeField, FloatField, SelectField
from wtforms.widgets import TextArea
from flask_wtf.file import FileField, FileAllowed

class BasicStudyForm(FlaskForm):
    name = StringField('Study Name', validators=[validators.DataRequired(), validators.Length(min=2, max=80)])
    theme = StringField('Theme', validators=[validators.DataRequired(), validators.Length(min=2, max=80)])
    place = StringField('Place', validators=[validators.DataRequired()], widget=TextArea())
    start_datetime = DateTimeField('Start Time',
                                  validators=[validators.DataRequired()],
                                  format='%Y-%m-%d %H:%M')
    end_datetime = DateTimeField('End Time',
                                validators=[validators.DataRequired()],
                                format='%Y-%m-%d %H:%M')
    description = StringField('Description', widget=TextArea(), validators=[validators.Length(min=50)])
    tag = SelectField('Tag', validators=[validators.DataRequired()])

class EditStudyForm(BasicStudyForm):
    photo = FileField('Study photo',
                     validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif'],
                                             'Only allow .jpg .png and .gif files')])

class CancelStudyForm(FlaskForm):
    confirm = StringField('Are you sure you want to cancel this study? (say yes)',
                         validators=[validators.DataRequired()])

class TagsForm(FlaskForm):
    name = StringField('Tag', validators=[validators.DataRequired(), validators.Length(min=2, max=20)])
