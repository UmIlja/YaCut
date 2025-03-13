from flask import jsonify, request

from . import app, db
from .constants import LETTERS_AND_DIGITS, MAX_USER_SHORT_ID_LENGTH
from .error_handlers import TheAPIError
from .models import URLMap


@app.route('/api/id/', methods=['POST'])
def create_url_id():
    try:
        data = request.get_json()
    except Exception:
        raise TheAPIError("Отсутствует тело запроса")
    if 'url' not in data:
        raise TheAPIError('"url" является обязательным полем!')
    if 'custom_id' in data:
        custom_id = data['custom_id']
        if len(custom_id) > MAX_USER_SHORT_ID_LENGTH:
            raise TheAPIError(
                'Указано недопустимое имя для короткой ссылки')
        for symbol in custom_id:
            if symbol not in LETTERS_AND_DIGITS:
                raise TheAPIError(
                    'Указано недопустимое имя для короткой ссылки')
        if URLMap.query.filter_by(short=custom_id).first() is not None:
            raise TheAPIError(
                'Предложенный вариант короткой ссылки уже существует.')

    url = URLMap()  # Создаем объект без параметров
    url.from_dict(data)  # Заполняем поля из запроса
    db.session.add(url)  # Добавляем объект в сессию
    db.session.commit()
    return jsonify(url.to_dict()), 201


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_original_url(short_id):
    url = URLMap.query.filter_by(short=short_id).first()
    if url is None:
        raise TheAPIError('Указанный id не найден', 404)
    return jsonify({'url': url.original}), 200
