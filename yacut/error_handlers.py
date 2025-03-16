from flask import jsonify, render_template

from . import app


class TheFieldError(Exception):
    status_code = 400

    def __init__(self, message, status_code=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code

    def to_dict(self):
        return dict(message=self.message)


@app.errorhandler(TheFieldError)
def the_handler(error):
    return jsonify(error.to_dict()), error.status_code


class MissingDataError(TheFieldError):
    def __init__(self, message="Отсутствует тело запроса"):
        super().__init__(message, status_code=400)


@app.errorhandler(TheFieldError)
@app.errorhandler(MissingDataError)
def handle_field_error(error):
    return jsonify(error.to_dict()), error.status_code


class NotFoundError(TheFieldError):
    def __init__(self, message="Не найдено"):
        super().__init__(message, status_code=404)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404
