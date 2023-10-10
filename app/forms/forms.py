from wtforms import Form, StringField, validators


class ShortenRequestForm(Form):
    url = StringField("URL", [validators.DataRequired(), validators.URL()])
    short_code = StringField(
        "Short Code", [validators.Optional(), validators.Length(min=3, max=12)]
    )
