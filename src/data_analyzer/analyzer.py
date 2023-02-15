import sqlite3
import datetime as dt
import os


def check_subreddit_data_exists(subreddit_name):
    if not os.path.isfile("reddit.db"):
        return False

    conn = sqlite3.connect("reddit.db")
    cursor = conn.cursor()

    cursor.execute("SELECT count(*) FROM posts WHERE subreddit = ?", (subreddit_name,))
    count = cursor.fetchone()[0]
    conn.close()

    return count > 0
    conn.close()

def generate_visualizations(subreddit_name):
    conn = sqlite3.connect('reddit.db')
    c = conn.cursor()

    c.execute("SELECT created FROM posts WHERE subreddit=?", (subreddit_name,))
    timestamps = c.fetchall()

    dates = [dt.datetime.fromtimestamp(ts[0]) for ts in timestamps]

    post_counts = {}
    for date in dates:
        if date.date() not in post_counts:
            post_counts[date.date()] = 1
        else:
            post_counts[date.date()] += 1

    c.execute("SELECT num_comments, score FROM posts WHERE subreddit=?", (subreddit_name,))
    comments_scores = c.fetchall()

    comment_counts = {}
    score_counts = {}
    for i, date in enumerate(dates):
        if date.date() not in comment_counts:
            comment_counts[date.date()] = 0
            score_counts[date.date()] = 0
        comment_counts[date.date()] += comments_scores[i][0]
        score_counts[date.date()] += comments_scores[i][1]

    avg_scores = {date: score_counts[date]/post_counts[date] for date in score_counts}

    labels = list(post_counts.keys())
    post_data = list(post_counts.values())
    comment_data = list(comment_counts.values())
    avg_score_data = list(avg_scores.values())

    return labels, post_data, comment_data, avg_score_data
