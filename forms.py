from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, SelectMultipleField, FormField, Form
from wtforms.validators import DataRequired, Length, Email, EqualTo, Optional, InputRequired, NumberRange
from wtforms.widgets import HiddenInput
import email_validator
from consts import CATEGORIES, WHEN_TODO


class RequiredIf(InputRequired):
    """
    Validator which makes a field required if another field has a
    certain value set.

    Sources:
        - http://wtforms.simplecodes.com/docs/1.0.1/validators.html
        - http://stackoverflow.com/questions/8463209/
        how-to-make-a-field-conditionally-optional-in-wtforms

    """
    field_flags = ('requiredif',)

    def __init__(self, other_field_name, value, message=None, *args, **kwargs):
        self.other_field_name = other_field_name
        self.message = message
        self.value = value

    def __call__(self, form, field):
        other_field = form[self.other_field_name]
        if other_field is None:
            raise Exception('no field named "%s" in form' % self.other_field_name)
        if other_field.data == self.value:
            super(RequiredIf, self).__call__(form, field)
        else:
            Optional().__call__(form, field)


class VenueForm(Form):
    name = StringField('Venue name',
                       validators=[RequiredIf('location', 2, 'This field is required when the location is set to "Out & About"'), Length(min=4, max=60)])
    postcode = StringField('Postcode',
                           validators=[RequiredIf('location', 2, 'This field is required when the location is set to "Out & About"'),Length(min=6, max=10)])
    address = TextAreaField('Address',
                            validators=[RequiredIf('location', 2, 'This field is required when the location is set to "Out & About"'), Length(min=4, max=120)])
    email = StringField('Email',
                          validators=[Length(min=0, max=80)])
    website = StringField('Website',
                            validators=[Length(min=0, max=120)])
    location = IntegerField(widget=HiddenInput(),
                            validators=[DataRequired(), NumberRange(1, 2)])


# class ActivityForm(FlaskForm):
class ActivityForm():
    title = StringField('Title',
                        validators=[DataRequired(), Length(min=4, max=60)])
    shortDescr = StringField('Short Description',
                             validators=[DataRequired(),
                                         Length(min=4, max=120)])
    longDescr = TextAreaField(u'Long Description',
                              validators=[DataRequired(),
                                          Length(min=4, max=240)])
    location = SelectField(u'Location',
                           choices=[(1, 'Home'), (2, 'Out & About')])
    ageRange = StringField('Age Range',
                           validators=[DataRequired(),
                                       Length(min=1, max=6)])
    online = SelectField(u'Online only',
                         choices=[('', 'No'), ('true', 'Yes')])
    freeTodo = SelectField(u'Free todo',
                           choices=[('true', 'Yes'), ('', 'No')])
    category = SelectMultipleField(u'Category',
                                   validators=[DataRequired()],
                                   choices=[(cat, cat) for cat in CATEGORIES])
    whenTodo = SelectMultipleField(u'When todo',
                                   validators=[DataRequired()],
                                   choices=[(when, when) for when in WHEN_TODO])
    additionalURL = StringField('Additional URL',
                                validators=[Length(min=0, max=120)])
    keywords = StringField('Keywords',
                           validators=[Length(min=0, max=60)])
    venue = FormField(VenueForm)


class EditActivityForm(FlaskForm, ActivityForm):
    submit = SubmitField('Update Activity')


class AddActivityForm(FlaskForm, ActivityForm):
    submit = SubmitField('Submit Activity')