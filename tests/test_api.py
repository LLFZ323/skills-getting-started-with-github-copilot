"""
Test suite for FastAPI activities application.
Using Arrange-Act-Assert pattern.
"""

import pytest
from fastapi.testclient import TestClient
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from app import app

client = TestClient(app)


class TestActivitiesEndpoint:
    """Tests for GET /activities"""

    def test_get_activities_returns_dict(self):
        # Arrange & Act
        response = client.get("/activities")
        
        # Assert
        assert response.status_code == 200
        assert isinstance(response.json(), dict)

    def test_activity_contains_required_fields(self):
        # Arrange
        expected_fields = ["description", "schedule", "max_participants", "participants"]
        
        # Act
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        for activity_name, details in activities.items():
            for field in expected_fields:
                assert field in details


class TestSignupEndpoint:
    """Tests for POST /activities/{name}/signup"""

    def test_signup_success_for_valid_activity(self):
        # Arrange
        test_email = "newstudent@mergington.edu"
        
        # Act
        response = client.post(f"/activities/Chess Club/signup?email={test_email}")
        
        # Assert
        assert response.status_code == 200

    def test_signup_fails_for_invalid_activity(self):
        # Arrange
        invalid_activity = "Non-Existent Club"
        
        # Act
        response = client.post(f"/activities/{invalid_activity}/signup?email=test@test.com")
        
        # Assert
        assert response.status_code == 404

    def test_duplicate_registration_is_blocked(self):
        # Arrange
        duplicate_email = "duplicate@mergington.edu"
        
        # Act
        client.post(f"/activities/Programming Class/signup?email={duplicate_email}")
        response = client.post(f"/activities/Programming Class/signup?email={duplicate_email}")
        
        # Assert
        assert response.status_code == 400


class TestUnregisterEndpoint:
    """Tests for POST /activities/{name}/unregister"""

    def test_unregister_success_for_registered_student(self):
        # Arrange
        test_email = "unreg@mergington.edu"
        client.post(f"/activities/Gym Class/signup?email={test_email}")
        
        # Act
        response = client.post(f"/activities/Gym Class/unregister?email={test_email}")
        
        # Assert
        assert response.status_code == 200

    def test_unregister_fails_for_non_participant(self):
        # Arrange
        non_participant_email = "notregistered@mergington.edu"
        
        # Act
        response = client.post(f"/activities/Chess Club/unregister?email={non_participant_email}")
        
        # Assert
        assert response.status_code == 404