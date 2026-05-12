def test_create_note(client, auth_headers):
    response = client.post('/api/notes/', headers=auth_headers, json={
        'title': 'Test Note',
        'content': 'Test Content'
    })
    assert response.status_code == 201
    assert response.json['success'] is True
    assert response.json['data']['note']['title'] == 'Test Note'
    
    # Store note_id for further tests if needed in advanced flows

def test_get_notes(client, auth_headers):
    # Create a note first
    client.post('/api/notes/', headers=auth_headers, json={
        'title': 'Note 1',
        'content': 'Content 1'
    })
    
    response = client.get('/api/notes/', headers=auth_headers)
    assert response.status_code == 200
    assert response.json['success'] is True
    assert len(response.json['data']['notes']) > 0

def test_get_notes_unauthorized(client):
    response = client.get('/api/notes/')
    assert response.status_code == 401

def test_create_note_validation_error(client, auth_headers):
    response = client.post('/api/notes/', headers=auth_headers, json={
        'title': '', # Empty title
        'content': ''
    })
    assert response.status_code == 400
    assert response.json['success'] is False
    assert 'error' in response.json

def test_update_note(client, auth_headers):
    # Create
    create_resp = client.post('/api/notes/', headers=auth_headers, json={
        'title': 'To Update',
        'content': 'Content'
    })
    note_id = create_resp.json['data']['note']['id']
    
    # Update
    response = client.put(f'/api/notes/{note_id}', headers=auth_headers, json={
        'title': 'Updated Title',
        'is_pinned': True
    })
    assert response.status_code == 200
    assert response.json['data']['note']['title'] == 'Updated Title'
    assert response.json['data']['note']['is_pinned'] is True

def test_delete_note(client, auth_headers):
    # Create
    create_resp = client.post('/api/notes/', headers=auth_headers, json={
        'title': 'To Delete',
        'content': 'Content'
    })
    note_id = create_resp.json['data']['note']['id']
    
    # Delete
    response = client.delete(f'/api/notes/{note_id}', headers=auth_headers)
    assert response.status_code == 200
    
    # Verify deletion
    get_resp = client.get(f'/api/notes/{note_id}', headers=auth_headers)
    assert get_resp.status_code == 404
