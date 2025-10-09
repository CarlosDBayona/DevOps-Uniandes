"""
Unit tests for Blacklist model.
"""
import pytest
from datetime import datetime
from app import db
from app.models import Blacklist


class TestBlacklistModel:
    """Test cases for the Blacklist model."""
    
    def test_create_blacklist_entry(self, app):
        """Test creating a blacklist entry."""
        with app.app_context():
            entry = Blacklist(
                email='test@example.com',
                app_uuid='app-123',
                blocked_reason='testing'
            )
            db.session.add(entry)
            db.session.commit()
            
            assert entry.id is not None
            assert entry.email == 'test@example.com'
            assert entry.app_uuid == 'app-123'
            assert entry.blocked_reason == 'testing'
            assert isinstance(entry.created_at, datetime)
    
    def test_blacklist_entry_without_optional_fields(self, app):
        """Test creating a blacklist entry without optional fields."""
        with app.app_context():
            entry = Blacklist(email='minimal@example.com')
            db.session.add(entry)
            db.session.commit()
            
            assert entry.id is not None
            assert entry.email == 'minimal@example.com'
            assert entry.app_uuid is None
            assert entry.blocked_reason is None
            assert isinstance(entry.created_at, datetime)
    
    def test_blacklist_repr(self, app):
        """Test the string representation of Blacklist."""
        with app.app_context():
            entry = Blacklist(email='repr@example.com')
            assert repr(entry) == '<Blacklist repr@example.com>'
    
    def test_query_by_email(self, app, sample_blacklist):
        """Test querying blacklist entries by email."""
        with app.app_context():
            entries = Blacklist.query.filter_by(email='blocked1@example.com').all()
            assert len(entries) == 1
            assert entries[0].email == 'blocked1@example.com'
            assert entries[0].blocked_reason == 'spam'
    
    def test_multiple_entries_same_email(self, app, sample_blacklist):
        """Test that multiple entries can exist for the same email."""
        with app.app_context():
            entries = Blacklist.query.filter_by(email='duplicate@example.com').all()
            assert len(entries) == 2
    
    def test_order_by_created_at(self, app, sample_blacklist):
        """Test ordering entries by creation time."""
        with app.app_context():
            entry = Blacklist.query.filter_by(
                email='duplicate@example.com'
            ).order_by(Blacklist.created_at.desc()).first()
            
            assert entry.blocked_reason == 'second entry - most recent'
