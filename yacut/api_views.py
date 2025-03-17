from flask import jsonify, request

from . import app
from .error_handlers import MissingDataError, NotFoundError
from .models import URLMap


@app.route('/api/id/', methods=['POST'])
def create_url_id():
    try:
        data = request.get_json()
    except Exception:
        raise MissingDataError("Отсутствует тело запроса")
    if 'url' not in data:
        raise MissingDataError('"url" является обязательным полем!')

    # Создаем объект URLMap из данных с помощью метода from_dict
    url = URLMap.from_dict(data)
    url.save()  # Сохраняем объект, валидируя его

    return jsonify(url.to_dict()), 201


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_original_url(short_id):
    url = URLMap.get(short_id)
    if url is None:
        raise NotFoundError('Указанный id не найден')
    return jsonify({'url': url.original}), 200
