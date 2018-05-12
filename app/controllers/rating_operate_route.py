
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app.models import BxBookRating
from app.engines import db

rating_operate = Blueprint('rating_operate', __name__, url_prefix='')
param_location = ('json', )


@rating_operate.route('/admin/rating/list')
@login_required
def rating_list():
    ratings = db.session.query(BxBookRating).all()

    return render_template('rating_list.html', ratings=ratings)


@rating_operate.route('/admin/rating/delete/<int:rating_id>')
def rating_delete(rating_id):
    rating = db.session.query(BxBookRating).filter(BxBookRating.id == rating_id).first()
    db.session.delete(rating)
    db.session.commit()
    return redirect(url_for('rating_operate.rating_list'))


