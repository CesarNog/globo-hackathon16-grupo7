#!/usr/bin/python
# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#

from flask import Flask, flash, redirect, render_template, request, \
    jsonify, abort, url_for, Response

# from flask.ext.sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler

from camera import VideoCamera
from forms import *
import urllib2
import json

# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_object('config')
# db = SQLAlchemy(app)

# Automatically tear down SQLAlchemy.
'''
@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()
'''

# Login required decorator.
'''
def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap
'''


# ----------------------------------------------------------------------------#
# Controllers.
# ----------------------------------------------------------------------------#


@app.route('/')
def home():
    obj = [[1, 2, 3], 123, 123.123, 'abc', {'key1': (1, 2, 3), 'key2': (4, 5, 6)}]

    try:
        json_atleta = atleta_detalhes_json(38162)
    except Exception:
        pass

    # Convert python object to json
    json_string = json.dumps(obj)
    print 'Json: %s' % json_string

    # Convert json to python object
    new_obj = json.loads(json_string)
    print 'Python obj: ', new_obj

    # Render template
    return render_template('pages/placeholder.home.html', info_atleta=json_string, info_atleta2=obj)


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/about')
def about():
    return render_template('pages/placeholder.about.html')


@app.route('/login')
def login():
    form = LoginForm(request.form)
    return render_template('forms/login.html', form=form)


@app.route('/register')
def register():
    form = RegisterForm(request.form)
    return render_template('forms/register.html', form=form)


@app.route('/forgot')
def forgot():
    form = ForgotForm(request.form)
    return render_template('forms/forgot.html', form=form)


@app.route('/esportes', methods=['GET'])
def esportes():
    return do_get_request("https://api.sde.globo.com/esportes")


@app.route('/atleta/<int:atleta_id>/detalhes/', methods=['GET'])
def atleta_detalhes(atleta_id, filter=None):
    return do_get_request("https://api.sde.globo.com/esportes/futebol/modalidades/"
                          "futebol_de_campo/categorias/profissional/campeonatos/campeonato-brasileiro/"
                          "edicoes/brasileirao-2015/estatisticas/atletas?atleta_ids=%d" % atleta_id, 'referencias')


def atleta_detalhes_json(atleta_id, filter=None):
    return do_get_request("https://api.sde.globo.com/esportes/futebol/modalidades/"
                          "futebol_de_campo/categorias/profissional/campeonatos/campeonato-brasileiro/"
                          "edicoes/brasileirao-2015/estatisticas/atletas?atleta_ids=%d" % atleta_id, 'referencias')


def do_get_request(url, key=None):
    request = urllib2.Request(url)
    request.add_header('token', 'hack2016-grupo7')

    try:
        response = urllib2.urlopen(request)
        result = response.read()
        dict_result = json.loads(result)
        if key:
            return jsonify(dict_result[key])
        else:
            return jsonify(dict_result)
    except urllib2.HTTPError, e:
        print str(e)
        abort(500)


@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % username


@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id


# Error handlers below


@app.errorhandler(500)
def internal_error(error):
    # db_session.rollback()
    return render_template('errors/500.html'), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

# ----------------------------------------------------------------------------#
# Launch.
# ----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
