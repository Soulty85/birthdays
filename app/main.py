from flask import Blueprint, jsonify
from app import db 
import redis

main_bp = Blueprint('main', __name__)
cache = redis.Redis(host='redis', port=6379, decode_responses=True)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        return {'id': self.id, 'name': self.name}

@main_bp.route('/')
def index():
    return jsonify({'message': 'Flask + Docker + SQLAlchemy OK'})

@main_bp.route('/users')
def users():
    users = User.query.all()
    return jsonify([u.to_dict() for u in users])

@main_bp.route('/cache')
def cache_test():
    cache.set('message', 'Bonjour depuis Redis !')
    return cache.get('message')

if __name__ == '__main__':
    from app import create_app
    app = create_app()
    app.run(host='0.0.0.0', port=5000)
