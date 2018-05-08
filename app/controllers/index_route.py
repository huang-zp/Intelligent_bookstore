from flask import Blueprint, render_template

from datetime import datetime, timedelta

now_time = datetime.now()
begin_time = now_time + timedelta(days=-7)

ib = Blueprint('ib', __name__, url_prefix='')
param_location = ('json', )


@ib.route('/admin')
def index():

    return render_template('index.html')