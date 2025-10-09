"""
Unit tests for Blacklist schema serialization.
"""
import pytest
from app.models import Blacklist
from app.schemas import BlacklistSchema


class TestBlacklistSchema:
    """Test cases for the BlacklistSchema."""
    
    def test_serialize_blacklist_entry(self, app):
        """Test serializing a blacklist entry."""
        with app.app_context():
            entry = Blacklist(
                email='schema@example.com',
                app_uuid='app-schema',
                blocked_reason='schema test'
            )
            schema = BlacklistSchema()
            result = schema.dump(entry)
            
            assert result['email'] == 'schema@example.com'
            assert result['app_uuid'] == 'app-schema'
            assert result['blocked_reason'] == 'schema test'
            assert 'created_at' in result
    
    def test_serialize_blacklist_with_none_values(self, app):
        """Test serializing a blacklist entry with None values."""
        with app.app_context():
            entry = Blacklist(email='minimal@example.com')
            schema = BlacklistSchema()
            result = schema.dump(entry)
            
            assert result['email'] == 'minimal@example.com'
            assert result['app_uuid'] is None
            assert result['blocked_reason'] is None
    
    def test_deserialize_blacklist_data(self, app):
        """Test deserializing blacklist data."""
        from app import db
        with app.app_context():
            schema = BlacklistSchema()
            data = {
                'email': 'deserialize@example.com',
                'app_uuid': 'app-deser',
                'blocked_reason': 'deserialize test'
            }
            # Validate with session (required by marshmallow-sqlalchemy)
            errors = schema.validate(data, session=db.session)
            assert errors == {}
