from flask import jsonify

from app import app
from app.models import Genre


@app.route('/api/genre/', methods=['GET'])
def get_all_genres():
    genres_list = [{'id': x.id, 'title': x.name} for x in Genre.query.all()]
    return jsonify({'genres-list': genres_list})
