from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Optional, Regexp

from .constants import (LETTERS_AND_DIGITS_PATTERN, MAX_USER_SHORT_ID_LENGTH,
                        MIN_USER_SHORT_ID_LENGTH)


class URLForm(FlaskForm):
    original_link = StringField(
        'Введите свою длинную ссылку',
        validators=[DataRequired(message='Обязательное поле')]
    )
    custom_id = StringField(
        'Введите свой вариант короткой ссылки',
        validators=[Length(MIN_USER_SHORT_ID_LENGTH, MAX_USER_SHORT_ID_LENGTH),
                    Regexp(LETTERS_AND_DIGITS_PATTERN,
                           message="Только латинские буквы и цифры."),
                    Optional()]
    )
    submit = SubmitField('Добавить')
