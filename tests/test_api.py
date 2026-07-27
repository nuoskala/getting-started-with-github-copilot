import pytest


class TestGetActivities:
    """Tests for GET /activities endpoint"""
    
    def test_get_all_activities_returns_dict(self, client, reset_activities):
        """Test that GET /activities returns all activities as a dictionary"""
        # Arrange
        expected_activities = ["Chess Club", "Programming Class", "Full Activity"]
        
        # Act
        response = client.get("/activities")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        for activity in expected_activities:
            assert activity in data
    
    def test_get_activities_structure(self, client, reset_activities):
        """Test that each activity has required fields"""
        # Arrange
        required_fields = ["description", "schedule", "max_participants", "participants"]
        
        # Act
        response = client.get("/activities")
        data = response.json()
        
        # Assert
        for activity_name, activity_data in data.items():
            for field in required_fields:
                assert field in activity_data, f"Missing {field} in {activity_name}"


class TestRootRedirect:
    """Tests for GET / endpoint"""
    
    def test_root_redirects_to_index(self, client):
        """Test that root path redirects to static/index.html"""
        # Arrange & Act
        response = client.get("/", follow_redirects=False)
        
        # Assert
        assert response.status_code == 307
        assert response.headers["location"] == "/static/index.html"


class TestSignup:
    """Tests for POST /activities/{activity_name}/signup endpoint"""
    
    def test_signup_success(self, client, reset_activities):
        """Test successful signup for an activity"""
        # Arrange
        activity = "Chess Club"
        email = "sarah@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity}/signup?email={email}",
            follow_redirects=False
        )
        
        # Assert
        assert response.status_code == 200
        assert "Signed up" in response.json()["message"]
        assert email in reset_activities[activity]["participants"]
    
    def test_signup_activity_not_found(self, client, reset_activities):
        """Test signup fails when activity doesn't exist"""
        # Arrange
        activity = "Non-existent Activity"
        email = "sarah@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity}/signup?email={email}"
        )
        
        # Assert
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()
    
    def test_signup_already_registered(self, client, reset_activities):
        """Test signup fails when student is already registered"""
        # Arrange
        activity = "Chess Club"
        email = "michael@mergington.edu"  # Already registered
        
        # Act
        response = client.post(
            f"/activities/{activity}/signup?email={email}"
        )
        
        # Assert
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"].lower()
    
    def test_signup_activity_full(self, client, reset_activities):
        """Test signup fails when activity is at capacity"""
        # Arrange
        activity = "Full Activity"
        email = "alex@mergington.edu"  # New participant, but activity is full
        
        # Act
        response = client.post(
            f"/activities/{activity}/signup?email={email}"
        )
        
        # Assert
        assert response.status_code == 400
        assert "full" in response.json()["detail"].lower()
    
    def test_signup_updates_participant_list(self, client, reset_activities):
        """Test that signup adds participant to the activity's participants list"""
        # Arrange
        activity = "Programming Class"
        initial_count = len(reset_activities[activity]["participants"])
        email = "noah@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity}/signup?email={email}"
        )
        
        # Assert
        assert response.status_code == 200
        assert len(reset_activities[activity]["participants"]) == initial_count + 1
        assert email in reset_activities[activity]["participants"]


class TestUnregister:
    """Tests for POST /activities/{activity_name}/unregister endpoint"""
    
    def test_unregister_success(self, client, reset_activities):
        """Test successful unregister from an activity"""
        # Arrange
        activity = "Chess Club"
        email = "michael@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity}/unregister?email={email}"
        )
        
        # Assert
        assert response.status_code == 200
        assert "Removed" in response.json()["message"]
        assert email not in reset_activities[activity]["participants"]
    
    def test_unregister_activity_not_found(self, client, reset_activities):
        """Test unregister fails when activity doesn't exist"""
        # Arrange
        activity = "Non-existent Activity"
        email = "michael@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity}/unregister?email={email}"
        )
        
        # Assert
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()
    
    def test_unregister_not_registered(self, client, reset_activities):
        """Test unregister fails when student is not registered"""
        # Arrange
        activity = "Chess Club"
        email = "notregistered@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity}/unregister?email={email}"
        )
        
        # Assert
        assert response.status_code == 400
        assert "not signed up" in response.json()["detail"].lower()
    
    def test_unregister_updates_participant_list(self, client, reset_activities):
        """Test that unregister removes participant from the activity's participants list"""
        # Arrange
        activity = "Chess Club"
        email = "michael@mergington.edu"
        initial_count = len(reset_activities[activity]["participants"])
        
        # Act
        response = client.post(
            f"/activities/{activity}/unregister?email={email}"
        )
        
        # Assert
        assert response.status_code == 200
        assert len(reset_activities[activity]["participants"]) == initial_count - 1
        assert email not in reset_activities[activity]["participants"]
