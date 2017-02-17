# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from flask import (render_template, redirect, app,
                   url_for, request, current_app,
                   make_response, session)
from flask_login import current_user
from flask_wtf import Form
from wtforms.fields import StringField, PasswordField
from wtforms.validators import DataRequired

from . import module_bp
from emcweb.emcweb.utils import get_block_status
from emcweb.utils import apply_db_settings


class LoginForm(Form):
    login = StringField('Login', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

@module_bp.route('/')
def index():
    if current_app.config.get('DB_FALL', None):
        try:
            apply_db_settings(current_app)
            current_app.config['DB_FALL'] = 0
        except:
            return render_template('err_conf.html',
                                   message='MySQL database is not configured'
                                   if current_app.config['DB_FALL'] == 1 else 'MySQL connection refused')

    status, _ = get_block_status()
    if status != 2:
        return render_template('blocks.html')

    serial = request.environ.get('SSL_CLIENT_M_SERIAL')
    if current_user.is_authenticated:
        redirect_to_index = redirect(url_for('emcweb.wallet'))
        resp = make_response(redirect_to_index)
        resp.set_cookie('strict_get_expires_nvs', value='1')

    return redirect_to_index \
        if current_user.is_authenticated else render_template('index.html',
                                                              form=LoginForm(),
                                                              enable_ssl=True if serial else False)
