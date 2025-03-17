import re
from datetime import datetime, timezone
from random import choices

from flask import current_app, flash
from yacut import db

from .constants import (DEFAULT_SHORT_ID_LENGTH, LETTERS_AND_DIGITS,
                        LETTERS_AND_DIGITS_PATTERN, MAX_USER_SHORT_ID_LENGTH)
from .error_handlers import TheFieldError


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String, unique=True, nullable=False)
    short = db.Column(db.String(MAX_USER_SHORT_ID_LENGTH), unique=True)
    timestamp = db.Column(db.DateTime,
                          index=True,
                          default=datetime.now(timezone.utc))

    def __init__(self, original, short=None):
        self.original = original
        self.short = short  # Устанавливаем short, если он передан, иначе None

    @classmethod
    def get_unique_short_id(cls):
        """
        Сгенерированные автоматически символы id для короткой ссылки.
        Формат для ссылки по умолчанию — шесть случайных символов,
        используя: заглавные/прописные латинские буквы, все цифры.
        """
        short_id = "".join(choices(LETTERS_AND_DIGITS,
                                   k=DEFAULT_SHORT_ID_LENGTH))
        # Проверяем, существует ли уже сгенерированный short_id в БД
        if cls.get(cls.short) is not None:
            raise TheFieldError('Возможные варианты короткого id исчерпаны.')
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

    def save(self):
        """Сохранить объект в базе данных с валидацией атрибутов."""
        # Если short не установлен, генерируем уникальный short_id
        if self.short is None:
            self.short = self.get_unique_short_id()
        # Если short уже был установлен, выполняем его валидацию...
        if self.short is not None and self.short != '':
            if not re.fullmatch(LETTERS_AND_DIGITS_PATTERN, self.short):
                raise TheFieldError(
                    'Указано недопустимое имя для короткой ссылки')
            if URLMap.get(self.short) is not None:
                flash('Предложенный вариант короткой ссылки уже существует.')
                raise TheFieldError(
                    'Предложенный вариант короткой ссылки уже существует.')

        db.session.add(self)
        db.session.commit()
