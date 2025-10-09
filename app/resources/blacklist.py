from flask import request, current_app
from flask_restful import Resource
from .. import db
from ..models import Blacklist
from ..schemas import BlacklistSchema

blacklist_schema = BlacklistSchema()


def _auth_ok():
    """Return True if the request is authorized via static bearer token."""
    auth = request.headers.get('Authorization', '')
    if not auth.startswith('Bearer '):
        return False
    token = auth.split(' ', 1)[1]

    # Static token check
    expected = current_app.config.get('STATIC_BEARER_TOKEN') or 'secret-token'
    return token == expected


class BlacklistResource(Resource):
    def post(self):
        if not _auth_ok():
            return {'msg': 'Missing or invalid token'}, 401
        data = request.get_json() or {}
        email = data.get('email')
        if not email:
            return {'msg': 'email is required'}, 400
        app_uuid = data.get('app_uuid')
        blocked_reason = data.get('blocked_reason')
        bl = Blacklist(email=email, app_uuid=app_uuid, blocked_reason=blocked_reason)
        db.session.add(bl)
        db.session.commit()
        return {'msg': 'Email added to blacklist'}, 201


class BlacklistLookupResource(Resource):
    def get(self, email):
        if not _auth_ok():
            return {'msg': 'Missing or invalid token'}, 401
        bl = Blacklist.query.filter_by(email=email).order_by(Blacklist.created_at.desc()).first()
        if not bl:
            return {'blocked': False, 'reason': None}, 200
        return {'blocked': True, 'reason': bl.blocked_reason}, 200
