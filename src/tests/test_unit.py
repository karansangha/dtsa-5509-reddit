def test_index_response_code(app, client):
    res = client.get('/')
    assert res.status_code == 200

def test_index_headers(app, client):
    res = client.get('/')
    assert 'Content-Type' in res.headers
    assert res.headers['Content-Type'] == 'text/html; charset=utf-8'

def test_index_content(app, client):
    res = client.get('/')
    assert b'<h1>Reddit Analyzer</h1>' in res.data
    assert b'<form action="/r/" method="POST">' in res.data
    assert b'<label for="subreddit_name">Enter any VALID subreddit name - </label>' in res.data
    assert b'<input name="subreddit_name" value="python">' in res.data
    assert b'<input type="submit" value="Submit!">' in res.data

def test_health_check(app, client):
    res = client.get('/health')
    assert res.status_code == 200
    assert b"I'm healthy!" in res.data

def test_metrics(app, client):
    res = client.get('/metrics')
    assert res.status_code == 200
    assert b'# TYPE app_info gauge' in res.data
    assert b'app_info{version="1.0.0"} 1.0' in res.data
