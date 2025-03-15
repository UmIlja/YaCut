from flask import jsonify, request

from . import app
from .error_handlers import TheAPIError
from .models import URLMap


@app.route('/api/id/', methods=['POST'])
def create_url_id():
    try:
        data = request.get_json()
    except Exception:
        raise TheAPIError("Отсутствует тело запроса")

    # Получаем оригинальный URL и custom_id из данных
    original = data.get('url')  # Получаем original_url, если он есть
    custom_id = data.get('custom_id')  # Получаем custom_id, если он есть

    # Создаем объект URLMap с оригинальным URL и, если есть, с custom_id
    url = URLMap(original=original, short=custom_id)

    # Сохраняем объект, валидируя его
    url.save(custom_id=custom_id, url=original)

    return jsonify(url.to_dict()), 201


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_original_url(short_id):
    url = URLMap.get(short_id)
    if url is None:
        raise TheAPIError('Указанный id не найден', 404)
    return jsonify({'url': url.original}), 200
