import json

NOTE_FILENAME = "test-note.md"
NOTE_CONTENT = "# Test Note\n\nThis is a test."
UPDATED_NOTE_CONTENT = "# Updated Note\n\nThis content has been updated."

def test_create_note_success(test_client, init_test_notes_dir):
    """Test creating a new note successfully."""
    response = test_client.post('/notes',
                                json={'filename': NOTE_FILENAME, 'content': NOTE_CONTENT},
                                content_type='application/json')
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['message'] == f"Note '{NOTE_FILENAME}' created successfully."

def test_create_note_conflict(test_client, init_test_notes_dir):
    """Test creating a note that already exists."""
    # Create the note first
    test_client.post('/notes', json={'filename': NOTE_FILENAME, 'content': NOTE_CONTENT})
    # Attempt to create it again
    response = test_client.post('/notes',
                                json={'filename': NOTE_FILENAME, 'content': NOTE_CONTENT},
                                content_type='application/json')
    assert response.status_code == 409  # Conflict
    data = json.loads(response.data)
    assert "already exists" in data['message']

def test_create_note_bad_request(test_client, init_test_notes_dir):
    """Test creating a note with missing data."""
    response = test_client.post('/notes',
                                json={'filename': NOTE_FILENAME},
                                content_type='application/json')
    assert response.status_code == 400

def test_list_notes(test_client, init_test_notes_dir):
    """Test listing all notes."""
    # Create a note to ensure the list is not empty
    test_client.post('/notes', json={'filename': NOTE_FILENAME, 'content': NOTE_CONTENT})
    response = test_client.get('/notes')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert NOTE_FILENAME in data

def test_get_note_content(test_client, init_test_notes_dir):
    """Test getting the raw content of a specific note."""
    test_client.post('/notes', json={'filename': NOTE_FILENAME, 'content': NOTE_CONTENT})
    response = test_client.get(f'/notes/{NOTE_FILENAME}')
    assert response.status_code == 200
    assert response.mimetype == 'text/markdown; charset=utf-8'
    assert response.data.decode('utf-8') == NOTE_CONTENT

def test_get_note_not_found(test_client, init_test_notes_dir):
    """Test getting a note that does not exist."""
    response = test_client.get('/notes/non-existent-note.md')
    assert response.status_code == 404

def test_update_note_success(test_client, init_test_notes_dir):
    """Test updating an existing note."""
    test_client.post('/notes', json={'filename': NOTE_FILENAME, 'content': NOTE_CONTENT})
    response = test_client.put(f'/notes/{NOTE_FILENAME}',
                               json={'content': UPDATED_NOTE_CONTENT},
                               content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['message'] == f"Note '{NOTE_FILENAME}' updated successfully."

    # Verify the content was actually updated
    getResponse = test_client.get(f'/notes/{NOTE_FILENAME}')
    assert getResponse.data.decode('utf-8') == UPDATED_NOTE_CONTENT

def test_update_note_not_found(test_client, init_test_notes_dir):
    """Test updating a note that does not exist."""
    response = test_client.put('/notes/non-existent-note.md',
                               json={'content': UPDATED_NOTE_CONTENT},
                               content_type='application/json')
    assert response.status_code == 404

def test_render_note_success(test_client, init_test_notes_dir):
    """Test rendering a note to HTML."""
    test_client.post('/notes', json={'filename': NOTE_FILENAME, 'content': NOTE_CONTENT})
    response = test_client.get(f'/notes/{NOTE_FILENAME}/render')
    assert response.status_code == 200
    assert response.mimetype == 'text/html'
    html = response.data.decode('utf-8')
    assert '<h1>Test Note</h1>' in html
    assert '<p>This is a test.</p>' in html

def test_render_note_not_found(test_client, init_test_notes_dir):
    """Test rendering a note that does not exist."""
    response = test_client.get('/notes/non-existent-note.md/render')
    assert response.status_code == 404

def test_delete_note_success(test_client, init_test_notes_dir):
    """Test deleting a note successfully."""
    test_client.post('/notes', json={'filename': NOTE_FILENAME, 'content': NOTE_CONTENT})

    # Ensure it exists before deleting
    list_response = test_client.get('/notes')
    assert NOTE_FILENAME in json.loads(list_response.data)

    # Delete it
    delete_response = test_client.delete(f'/notes/{NOTE_FILENAME}')
    assert delete_response.status_code == 204  # No Content

    # Verify it's gone
    get_response = test_client.get(f'/notes/{NOTE_FILENAME}')
    assert get_response.status_code == 404

    list_response_after = test_client.get('/notes')
    assert NOTE_FILENAME not in json.loads(list_response_after.data)

def test_delete_note_not_found(test_client, init_test_notes_dir):
    """Test deleting a note that does not exist."""
    response = test_client.delete('/notes/non-existent-note.md')
    assert response.status_code == 404