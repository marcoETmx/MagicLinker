from wtforms import Form, StringField, validators


class ShortenRequestForm(Form):
    url = StringField("URL", [validators.DataRequired(), validators.URL()])
