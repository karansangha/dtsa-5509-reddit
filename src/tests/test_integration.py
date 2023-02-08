def test_echo_input_response_code(app, client):
    res = client.post('/echo_user_input', data={'user_input': 'Hello World!'})
    assert res.status_code == 200

def test_echo_input_headers(app, client):
    res = client.post('/echo_user_input', data={'user_input': 'Hello World!'})
    assert 'Content-Type' in res.headers
    assert res.headers['Content-Type'] == 'text/html; charset=utf-8'

def test_echo_input_content(app, client):
    res = client.post('/echo_user_input', data={'user_input': 'Hello World!'})
    assert b'<h1>Thank you for using the form!</h1>' in res.data
    assert b'<p>You entered: Hello World!</p>' in res.data
