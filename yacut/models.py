import re
from datetime import datetime, timezone
from random import choices

from flask import current_app

from yacut import db

from .constants import (DEFAULT_SHORT_ID_LENGTH, LETTERS_AND_DIGITS,
                        LETTERS_AND_DIGITS_PATTERN, MAX_USER_SHORT_ID_LENGTH)
from .error_handlers import TheAPIError


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String, unique=True, nullable=False)
    short = db.Column(db.String(MAX_USER_SHORT_ID_LENGTH), unique=True)
    timestamp = db.Column(db.DateTime,
                          index=True,
                          default=datetime.now(timezone.utc))

    def __init__(self, original, short=None):
        self.original = original
        if short:
            self.short = short  # Используем переданный short
        else:
            self.short = self.get_unique_short_id()

    @classmethod
    def get_unique_short_id(cls):
        """
        Сгенерированные автоматически символы id для короткой ссылки.
        Формат для ссылки по умолчанию — шесть случайных символов,
        используя: заглавные/прописные латинские буквы, все цифры.
        """
        while True:
            short_id = "".join(choices(LETTERS_AND_DIGITS,
                                       k=DEFAULT_SHORT_ID_LENGTH))
            # Проверяем, существует ли уже сгенерированный short_id в БД
            if not cls.query.filter_by(short=short_id).first():
                return short_id

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=self.get_full_link_with_short_id(),
        )

    @staticmethod
    def from_dict(data):
        """Создает экземпляр URLMap из словаря."""
        original = data.get('url')
        custom_id = data.get('custom_id')
        url_map = URLMap(original=original, short=custom_id)
        return url_map

    def get_full_link_with_short_id(self):
        base_url = current_app.config.get('BASE_URL', 'http://localhost')
        return f'{base_url}/{self.short}'

    @classmethod
    def get(cls, short_id):
        """Получить оригинальный URL по короткому идентификатору."""
        return cls.query.filter_by(short=short_id).first()

    def save(self, custom_id=None, url=None):
        """Сохранить объект в базе данных с валидацией атрибутов."""
        if url is None:
            raise TheAPIError('"url" является обязательным полем!')
        # Если custom_id передан и не пустой, выполняем его валидацию
        if custom_id is not None and custom_id != '':
            if not re.fullmatch(LETTERS_AND_DIGITS_PATTERN, custom_id):
                raise TheAPIError(
                    'Указано недопустимое имя для короткой ссылки')
            if URLMap.query.filter_by(short=custom_id).first() is not None:
                raise TheAPIError(
                    'Предложенный вариант короткой ссылки уже существует.')
            self.short = custom_id
            self.original = url

        db.session.add(self)
        db.session.commit()
