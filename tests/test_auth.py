def test_register_success(client):
    response = client.post('/api/auth/register', json={
        'username': 'newuser',
        'email': 'new@test.com',
        'password': 'password123'
    })
    assert response.status_code == 201
    assert response.json['success'] is True
    assert 'user' in response.json['data']

def test_register_duplicate_username(client, test_user):
    response = client.post('/api/auth/register', json={
        'username': 'testuser',
        'email': 'different@test.com',
        'password': 'password123'
    })
    assert response.status_code == 409
    assert response.json['success'] is False

def test_login_success(client, test_user):
    response = client.post('/api/auth/login', json={
        'username': 'testuser',
        'password': 'password123'
    })
    assert response.status_code == 200
    assert response.json['success'] is True
    assert 'access_token' in response.json['data']

def test_login_failure(client, test_user):
    response = client.post('/api/auth/login', json={
        'username': 'testuser',
        'password': 'wrongpassword'
    })
    assert response.status_code == 401
    assert response.json['success'] is False

def test_profile_protected(client):
    # Without token
    response = client.get('/api/auth/profile')
    assert response.status_code == 401
    
def test_profile_with_token(client, auth_headers):
    # With token
    response = client.get('/api/auth/profile', headers=auth_headers)
    assert response.status_code == 200
    assert response.json['success'] is True
