def test_index_response_code(app, client):
    res = client.get('/')
    assert res.status_code == 200

def test_index_headers(app, client):
    res = client.get('/')
    assert 'Content-Type' in res.headers
    assert res.headers['Content-Type'] == 'text/html; charset=utf-8'

def test_index_content(app, client):
    res = client.get('/')
    assert b'<h1>Twitter Analyzer</h1>' in res.data
    assert b'<form action="/echo_user_input" method="POST">' in res.data
    assert b'<label for="user_input">Enter any text - </label>' in res.data
    assert b'<input name="user_input">' in res.data
    assert b'<input type="submit" value="Submit!">' in res.data
