def test_user_workflow(client):
    """Test an end-to-end user flow with filter, pagination, and reset."""
    form_data = {
        "param_title": "tokyo",
        "param_genre": "10"
    }
    # Apply filter
    client.post('/update_session', data=form_data, follow_redirects=True)
    with client.session_transaction() as sess:
        assert sess['params']['q'] == "tokyo"
        assert sess['params']['genres'] == "10"

    # Go to next page
    client.post('/inc', follow_redirects=True)
    with client.session_transaction() as sess:
        assert sess['page'] == 2  # Page should increment

    # Reset page
    client.get('/reset', follow_redirects=True)
    with client.session_transaction() as sess:
        assert sess['page'] == 1  # Page should reset to 1
