import pytest
import sqlite3

import sqlite3
import pytest

@pytest.fixture
def conn():
    conn = sqlite3.connect(":memory:")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE posts (
            id TEXT PRIMARY KEY,
            title TEXT,
            score INTEGER,
            subreddit TEXT,
            url TEXT,
            num_comments INTEGER,
            body TEXT,
            created INTEGER,
            got_comments BOOLEAN DEFAULT NULL
        )
    """)
    conn.commit()
    yield conn
    conn.close()

def test_insert_post(conn):
    c = conn.cursor()
    post = {
        'id': '12345',
        'title': 'Test Post',
        'score': 100,
        'subreddit': 'test_subreddit',
        'url': 'https://www.example.com',
        'num_comments': 5,
        'body': 'This is a test post',
        'created': 1644547200,
        'got_comments': None
    }
    insert_post_query = """
        INSERT INTO posts (id, title, score, subreddit, url, num_comments, body, created, got_comments)
        VALUES (:id, :title, :score, :subreddit, :url, :num_comments, :body, :created, :got_comments)
    """
    c.execute(insert_post_query, post)
    conn.commit()
    c.execute("SELECT * FROM posts WHERE id='12345'")
    result = c.fetchone()
    assert result == ('12345', 'Test Post', 100, 'test_subreddit', 'https://www.example.com', 5, 'This is a test post', 1644547200, None)


@pytest.fixture
def insert_post(conn):
    c = conn.cursor()
    post = {
        'id': '12345',
        'title': 'Test Post',
        'score': 100,
        'subreddit': 'test_subreddit',
        'url': 'https://www.example.com',
        'num_comments': 5,
        'body': 'This is a test post',
        'created': 1644547200,
        'got_comments': None
    }
    insert_post_query = """
        INSERT INTO posts (id, title, score, subreddit, url, num_comments, body, created, got_comments)
        VALUES (:id, :title, :score, :subreddit, :url, :num_comments, :body, :created, :got_comments)
    """
    c.execute(insert_post_query, post)
    conn.commit()

@pytest.mark.usefixtures("insert_post")
def test_existence_post(conn):
    c = conn.cursor()
    c.execute("SELECT * FROM posts")
    results = c.fetchall()
    print("Results: ", results)
    print(results)
    assert len(results) == 1
    assert results[0][1] == "Test Post"
    assert results[0][2] == 100
    assert results[0][3] == "test_subreddit"
    assert results[0][4] == "https://www.example.com"
    assert results[0][5] == 5
    assert results[0][6] == "This is a test post"
    assert results[0][7] == 1644547200
    assert results[0][8] == None
