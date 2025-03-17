from flask import abort, flash, redirect, render_template, request

from . import app
from .forms import URLForm
from .models import URLMap


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLForm()
    created_link = None
    if form.validate_on_submit():
        url = URLMap(original=form.original_link.data,
                     short=form.custom_id.data)

        try:
            url.save()
            created_link = f"{request.host_url}{url.short}"
        except Exception as e:  # Если что-то не так и метод save не обработал
            flash(str(e))
            return render_template('index.html', form=form)

    return render_template('index.html', form=form, created_link=created_link)


@app.route('/<short>')
def redirect_to_url(short):
    # Предполагаем, что short является первичным ключом
    url_object = URLMap.get(short)  # Здесь short должен быть первичным ключом
    if url_object:
        return redirect(url_object.original, code=302)
    return abort(404)
