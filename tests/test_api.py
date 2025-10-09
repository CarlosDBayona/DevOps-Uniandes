"""
Unit tests for Blacklist API endpoints.
"""
import json
import pytest


class TestBlacklistEndpoints:
    """Test cases for the Blacklist API endpoints."""
    
    # POST /blacklists tests
    
    def test_add_blacklist_success(self, client, auth_headers):
        """Test successfully adding an email to blacklist."""
        data = {
            'email': 'test@example.com',
            'app_uuid': 'app-123',
            'blocked_reason': 'spam'
        }
        response = client.post(
            '/blacklists',
            data=json.dumps(data),
            headers=auth_headers
        )
        
        assert response.status_code == 201
        assert response.json['msg'] == 'Email added to blacklist'
    
    def test_add_blacklist_minimal_data(self, client, auth_headers):
        """Test adding blacklist with only required email field."""
        data = {'email': 'minimal@example.com'}
        response = client.post(
            '/blacklists',
            data=json.dumps(data),
            headers=auth_headers
        )
        
        assert response.status_code == 201
        assert response.json['msg'] == 'Email added to blacklist'
    
    def test_add_blacklist_missing_email(self, client, auth_headers):
        """Test adding blacklist without required email field."""
        data = {
            'app_uuid': 'app-123',
            'blocked_reason': 'spam'
        }
        response = client.post(
            '/blacklists',
            data=json.dumps(data),
            headers=auth_headers
        )
        
        assert response.status_code == 400
        assert 'email' in response.json['msg'].lower()
        assert 'required' in response.json['msg'].lower()
    
    def test_add_blacklist_empty_email(self, client, auth_headers):
        """Test adding blacklist with empty email string."""
        data = {'email': ''}
        response = client.post(
            '/blacklists',
            data=json.dumps(data),
            headers=auth_headers
        )
        
        assert response.status_code == 400
    
    def test_add_blacklist_no_token(self, client):
        """Test adding blacklist without authorization token."""
        data = {'email': 'test@example.com'}
        response = client.post(
            '/blacklists',
            data=json.dumps(data),
            headers={'Content-Type': 'application/json'}
        )
        
        assert response.status_code == 401
        assert 'token' in response.json['msg'].lower()
    
    def test_add_blacklist_invalid_token(self, client):
        """Test adding blacklist with invalid token."""
        data = {'email': 'test@example.com'}
        headers = {
            'Authorization': 'Bearer wrong-token',
            'Content-Type': 'application/json'
        }
        response = client.post(
            '/blacklists',
            data=json.dumps(data),
            headers=headers
        )
        
        assert response.status_code == 401
        assert 'token' in response.json['msg'].lower()
    
    def test_add_blacklist_malformed_auth_header(self, client):
        """Test adding blacklist with malformed authorization header."""
        data = {'email': 'test@example.com'}
        headers = {
            'Authorization': 'InvalidFormat token',
            'Content-Type': 'application/json'
        }
        response = client.post(
            '/blacklists',
            data=json.dumps(data),
            headers=headers
        )
        
        assert response.status_code == 401
    
    def test_add_blacklist_no_json_body(self, client, auth_headers):
        """Test adding blacklist with no JSON body."""
        response = client.post('/blacklists', headers=auth_headers)
        
        assert response.status_code == 400
    
    # GET /blacklists/<email> tests
    
    def test_check_blacklist_found(self, client, auth_headers, sample_blacklist):
        """Test checking blacklist for an existing email."""
        response = client.get(
            '/blacklists/blocked1@example.com',
            headers=auth_headers
        )
        
        assert response.status_code == 200
        assert response.json['blocked'] is True
        assert response.json['reason'] == 'spam'
    
    def test_check_blacklist_not_found(self, client, auth_headers):
        """Test checking blacklist for a non-existent email."""
        response = client.get(
            '/blacklists/notfound@example.com',
            headers=auth_headers
        )
        
        assert response.status_code == 200
        assert response.json['blocked'] is False
        assert response.json['reason'] is None
    
    def test_check_blacklist_returns_most_recent(self, client, auth_headers, sample_blacklist):
        """Test that checking blacklist returns the most recent entry."""
        response = client.get(
            '/blacklists/duplicate@example.com',
            headers=auth_headers
        )
        
        assert response.status_code == 200
        assert response.json['blocked'] is True
        assert response.json['reason'] == 'second entry - most recent'
    
    def test_check_blacklist_no_token(self, client):
        """Test checking blacklist without authorization token."""
        response = client.get('/blacklists/test@example.com')
        
        assert response.status_code == 401
        assert 'token' in response.json['msg'].lower()
    
    def test_check_blacklist_invalid_token(self, client):
        """Test checking blacklist with invalid token."""
        headers = {'Authorization': 'Bearer wrong-token'}
        response = client.get(
            '/blacklists/test@example.com',
            headers=headers
        )
        
        assert response.status_code == 401
        assert 'token' in response.json['msg'].lower()
    
    def test_check_blacklist_special_characters_in_email(self, client, auth_headers, app):
        """Test checking blacklist with special characters in email."""
        with app.app_context():
            from app import db
            from app.models import Blacklist
            entry = Blacklist(
                email='test+special@example.com',
                blocked_reason='testing special chars'
            )
            db.session.add(entry)
            db.session.commit()
        
        response = client.get(
            '/blacklists/test+special@example.com',
            headers=auth_headers
        )
        
        assert response.status_code == 200
        assert response.json['blocked'] is True


class TestIntegrationScenarios:
    """Integration test scenarios."""
    
    def test_add_and_check_workflow(self, client, auth_headers):
        """Test complete workflow: add email then check it."""
        # Add email to blacklist
        add_data = {
            'email': 'workflow@example.com',
            'app_uuid': 'app-workflow',
            'blocked_reason': 'integration test'
        }
        add_response = client.post(
            '/blacklists',
            data=json.dumps(add_data),
            headers=auth_headers
        )
        assert add_response.status_code == 201
        
        # Check the email
        check_response = client.get(
            '/blacklists/workflow@example.com',
            headers=auth_headers
        )
        assert check_response.status_code == 200
        assert check_response.json['blocked'] is True
        assert check_response.json['reason'] == 'integration test'
    
    def test_multiple_additions_same_email(self, client, auth_headers):
        """Test adding the same email multiple times."""
        email = 'multiple@example.com'
        
        # Add first time
        data1 = {
            'email': email,
            'blocked_reason': 'first reason'
        }
        response1 = client.post(
            '/blacklists',
            data=json.dumps(data1),
            headers=auth_headers
        )
        assert response1.status_code == 201
        
        # Add second time
        data2 = {
            'email': email,
            'blocked_reason': 'second reason'
        }
        response2 = client.post(
            '/blacklists',
            data=json.dumps(data2),
            headers=auth_headers
        )
        assert response2.status_code == 201
        
        # Check - should return most recent
        check_response = client.get(
            f'/blacklists/{email}',
            headers=auth_headers
        )
        assert check_response.status_code == 200
        assert check_response.json['reason'] == 'second reason'
    
    def test_different_emails_independent(self, client, auth_headers):
        """Test that different emails are tracked independently."""
        # Add multiple emails
        emails = [
            {'email': 'user1@example.com', 'blocked_reason': 'reason1'},
            {'email': 'user2@example.com', 'blocked_reason': 'reason2'},
            {'email': 'user3@example.com', 'blocked_reason': 'reason3'},
        ]
        
        for data in emails:
            response = client.post(
                '/blacklists',
                data=json.dumps(data),
                headers=auth_headers
            )
            assert response.status_code == 201
        
        # Verify each email independently
        for data in emails:
            response = client.get(
                f'/blacklists/{data["email"]}',
                headers=auth_headers
            )
            assert response.status_code == 200
            assert response.json['blocked'] is True
            assert response.json['reason'] == data['blocked_reason']


class TestAuthenticationMechanisms:
    """Test authentication edge cases."""
    
    def test_token_case_sensitive(self, client):
        """Test that bearer token is case-sensitive."""
        data = {'email': 'test@example.com'}
        headers = {
            'Authorization': 'Bearer TEST-TOKEN',  # Wrong case
            'Content-Type': 'application/json'
        }
        response = client.post(
            '/blacklists',
            data=json.dumps(data),
            headers=headers
        )
        
        assert response.status_code == 401
    
    def test_bearer_prefix_required(self, client):
        """Test that 'Bearer' prefix is required."""
        data = {'email': 'test@example.com'}
        headers = {
            'Authorization': 'test-token',  # Missing 'Bearer'
            'Content-Type': 'application/json'
        }
        response = client.post(
            '/blacklists',
            data=json.dumps(data),
            headers=headers
        )
        
        assert response.status_code == 401
    
    def test_extra_spaces_in_auth_header(self, client):
        """Test authorization header with extra spaces."""
        data = {'email': 'test@example.com'}
        headers = {
            'Authorization': 'Bearer  test-token',  # Extra space
            'Content-Type': 'application/json'
        }
        response = client.post(
            '/blacklists',
            data=json.dumps(data),
            headers=headers
        )
        
        # Should fail due to token mismatch
        assert response.status_code == 401
