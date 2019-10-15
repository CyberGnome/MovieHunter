import math

from flask import jsonify

from app import app, db
from app.models import Movie
from app.raw_sql.raw_sql import count_all
from settings import APP_CONFIG


@app.route('/api/movies/', methods=['GET'])
@app.route('/api/movies/<page_id>/', methods=['GET'])
def get_all_movies(page_id=1):
    try:
        page_id = int(page_id)
    except:
        return jsonify(
            {'message': "Bad Request"}), 400

    res = []
    pagination = APP_CONFIG['movie_pagination']
    pages_count = math.ceil(count_all(Movie) / pagination)

    if page_id > pages_count:
        return jsonify({'result': res,
                        'pages': pages_count})

    res = [{'id': x.id, 'title': x.title, 'year': x.year,
            'rating': x.rating.rating_value} for x in Movie.query.paginate(page_id, pagination, False).items]

    return jsonify({'result': res,
                    'pages': pages_count})


