from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField,PasswordField,SubmitField,TextAreaField,FieldList,Form,FormField
from wtforms.validators import DataRequired,Length,Email,EqualTo,ValidationError,Optional
import random


class GroupForm(Form):
    emailId = StringField('Add Email Id',validators=[Optional()])

class EventForm(FlaskForm):
    
    title = StringField("Title",validators=[DataRequired(),Length(min=2,max=20)])
    daterange = StringField("Start & End DateTime")
    group = StringField('Group', description = "Add Email Id of group members")
    RRule = TextAreaField("Strict Recurrence Rule")
    submit=SubmitField('Create Event')
