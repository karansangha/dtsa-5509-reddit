import praw
import os
import sqlite3

def authenticate():
    reddit = praw.Reddit(
        client_id=os.environ.get("REDDIT_CLIENT_ID"), 
        client_secret=os.environ.get('REDDIT_CLIENT_SECRET'), 
        user_agent=os.environ.get('REDDIT_USER_AGENT')
        )
    return reddit

def get_conn():
    conn = sqlite3.connect('reddit.db')
    conn.execute("PRAGMA journal_mode = WAL")
    conn.commit()
    return conn

def get_top_posts(subreddit_name):
    # Connect to the database
    conn = get_conn()
    
    cursor = conn.cursor()

    # Create the posts table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS posts (
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
    ''')

    # Fetch the top posts using PRAW
    reddit = authenticate()
    
    top_posts = reddit.subreddit(subreddit_name).top(time_filter='month',limit=100)

    # Prepare the data for bulk insert
    data = [(post.id, post.title, post.score, subreddit_name, post.url, post.num_comments, post.selftext, int(post.created), None) for post in top_posts]

    # Start a transaction
    cursor.execute('BEGIN TRANSACTION')

    # Insert the data in a bulk insert
    cursor.executemany('INSERT OR IGNORE INTO posts (id, title, score, subreddit, url, num_comments, body, created, got_comments) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', data)

    # Commit the transaction
    conn.commit()

    # Close the connection
    conn.close()

def get_comments(post_id):
    reddit = authenticate()
    
    conn = get_conn()
    cursor = conn.cursor()
    
    cursor.execute("CREATE TABLE IF NOT EXISTS comments (post_id TEXT, comment_id TEXT, author TEXT, body TEXT, created INTEGER)")
    
    cursor.execute("SELECT * FROM comments WHERE post_id=?", (post_id,))
    result = cursor.fetchone()
    
    post = cursor.fetchone()
    if post is not None and post[8] == 1:
        return

    submission = reddit.submission(id=post_id)
    comments = []
    for comment in submission.comments:
        comments.append((
            comment.id,
            post_id,
            comment.body,
            comment.score,
            comment.created_utc
        ))

    # Insert the extracted comments into the database
    cursor.executemany("""
        INSERT OR IGNORE INTO comments (comment_id, post_id, body, score, created_utc)
        VALUES (?,?,?,?,?)
    """, comments)
    conn.commit()

    # Mark the post as having had its comments extracted
    cursor.execute("UPDATE posts SET got_comments=1 WHERE post_id=?", (post_id,))
    conn.commit()

def retrieve_comments():
    conn = sqlite3.connect('reddit.db')
    c = conn.cursor()
    
    c.execute("SELECT id FROM posts WHERE got_comments IS NULL")
    post_ids = c.fetchall()
    
    for post_id in post_ids:
        post_id = post_id[0]
        get_comments(post_id)
        
    conn.close()

if __name__ == '__main__':
    get_top_posts('python')
