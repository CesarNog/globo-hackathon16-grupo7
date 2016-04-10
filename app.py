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
import threading

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
    # Render template
    atleta_id = 38162;
    return render_template('pages/placeholder.home.html',
                           foto_atleta=get_atleta_foto(atleta_id),
                           nome_atleta=get_atleta_nome_upper(atleta_id),
                           n_cartao_amarelo=get_num_cartao_amarelo(atleta_id),
                           n_cartao_vermelho=get_num_cartao_vermelho(atleta_id),
                           n_chutes_ao_gol=get_num_chutes_ao_gol(atleta_id),
                           n_faltas_cometidas=get_num_chutes_ao_gol(atleta_id),
                           n_faltas_recebidas=get_num_chutes_ao_gol(atleta_id))


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/esportes', methods=['GET'])
def esportes():
    return do_get_request("https://api.sde.globo.com/esportes")


@app.route('/atleta/<int:atleta_id>/detalhes', methods=['GET'])
def atleta_detalhes(atleta_id, filter=None):
    return do_get_request("https://api.sde.globo.com/esportes/futebol/modalidades/"
                          "futebol_de_campo/categorias/profissional/campeonatos/campeonato-brasileiro/"
                          "edicoes/brasileirao-2015/estatisticas/atletas?atleta_ids=%d" % atleta_id, 'referencias')


@app.route('/atleta/<int:atleta_id>/resultados', methods=['GET'])
def atleta_resultados(atleta_id, filter=None):
    return do_get_request("https://api.sde.globo.com/esportes/futebol/modalidades/"
                          "futebol_de_campo/categorias/profissional/campeonatos/campeonato-brasileiro/"
                          "edicoes/brasileirao-2015/estatisticas/atletas?atleta_ids=%d" % atleta_id, 'resultados')


def get_atleta_foto(atleta_id):
    return do_get_request("https://api.sde.globo.com/esportes/futebol/modalidades/"
                          "futebol_de_campo/categorias/profissional/campeonatos/campeonato-brasileiro/"
                          "edicoes/brasileirao-2015/estatisticas/atletas?atleta_ids=%d" % atleta_id, 'referencias').get(
        'atletas').get(str(atleta_id)).get('fotos').get('300x300')


def get_atleta_nome_upper(atleta_id):
    return do_get_request("https://api.sde.globo.com/esportes/futebol/modalidades/"
                          "futebol_de_campo/categorias/profissional/campeonatos/campeonato-brasileiro/"
                          "edicoes/brasileirao-2015/estatisticas/atletas?atleta_ids=%d" % atleta_id, 'referencias').get(
        'atletas').get(str(atleta_id)).get('nome').upper()


def get_num_cartao_amarelo(atleta_id):
    return do_get_request("https://api.sde.globo.com/esportes/futebol/modalidades/"
                          "futebol_de_campo/categorias/profissional/campeonatos/campeonato-brasileiro/"
                          "edicoes/brasileirao-2015/estatisticas/atletas?atleta_ids=%d" % atleta_id, 'resultados').get('estatisticas_atletas')[0].get('estatisticas').get('CA').get('total')


def get_num_cartao_vermelho(atleta_id):
    return do_get_request("https://api.sde.globo.com/esportes/futebol/modalidades/"
                          "futebol_de_campo/categorias/profissional/campeonatos/campeonato-brasileiro/"
                          "edicoes/brasileirao-2015/estatisticas/atletas?atleta_ids=%d" % atleta_id, 'resultados').get('estatisticas_atletas')[0].get('estatisticas').get('CV').get('total')

def get_num_chutes_ao_gol(atleta_id):
    return do_get_request("https://api.sde.globo.com/esportes/futebol/modalidades/"
                          "futebol_de_campo/categorias/profissional/campeonatos/campeonato-brasileiro/"
                          "edicoes/brasileirao-2015/estatisticas/atletas?atleta_ids=%d" % atleta_id, 'resultados').get('estatisticas_atletas')[0].get('estatisticas').get('ZG').get('total')


def get_num_faltas_cometidas(atleta_id):
    return do_get_request("https://api.sde.globo.com/esportes/futebol/modalidades/"
                          "futebol_de_campo/categorias/profissional/campeonatos/campeonato-brasileiro/"
                          "edicoes/brasileirao-2015/estatisticas/atletas?atleta_ids=%d" % atleta_id, 'resultados').get('estatisticas_atletas')[0].get('estatisticas').get('PD').get('total')


def get_num_faltas_recebidas(atleta_id):
    return do_get_request("https://api.sde.globo.com/esportes/futebol/modalidades/"
                          "futebol_de_campo/categorias/profissional/campeonatos/campeonato-brasileiro/"
                          "edicoes/brasileirao-2015/estatisticas/atletas?atleta_ids=%d" % atleta_id, 'resultados').get('estatisticas_atletas')[0].get('estatisticas').get('TF').get('total')



def do_get_request(url, key=None):
    request = urllib2.Request(url)
    request.add_header('token', 'hack2016-grupo7')

    try:
        response = urllib2.urlopen(request)
        result = response.read()
        dict_result = json.loads(result)
        if key:
            return dict_result[key]
        else:
            return dict_result
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
