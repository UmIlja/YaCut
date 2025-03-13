from datetime import datetime, timezone
from random import choices

from flask import current_app

from yacut import db

from .constants import (
    DEFAULT_SHORT_ID_LENGTH, LETTERS_AND_DIGITS, MAX_USER_SHORT_ID_LENGTH
)


def get_unique_short_id():
    """
    Сгенерированные автоматически символы идентификатора для короткой ссылки.
    Формат для ссылки по умолчанию — шесть случайных символов,
    используя: заглавные/прописные латинские буквы, все цифры.
    """
    short_id = "".join(choices(LETTERS_AND_DIGITS, k=DEFAULT_SHORT_ID_LENGTH))
    return short_id


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String, unique=True, nullable=False)
    short = db.Column(db.String(MAX_USER_SHORT_ID_LENGTH),
                      unique=True,
                      default=get_unique_short_id)
    timestamp = db.Column(db.DateTime,
                          index=True,
                          default=datetime.now(timezone.utc))

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=self.get_full_link_with_short_id(),
        )

    def from_dict(self, data):
        for field in ['url', 'custom_id']:
            if field in data:
                setattr(self,
                        'original' if field == 'url' else 'short',
                        data[field])

    def get_full_link_with_short_id(self):
        base_url = current_app.config.get('BASE_URL', 'http://localhost')
        return f'{base_url}/{self.short}'
