import sqlite3
from datetime import datetime
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

def generate_visualizations_data(subreddit_name):
    # Connect to the database
    conn = sqlite3.connect('reddit.db')

    # Query the posts table for data
    c = conn.cursor()
    c.execute('''SELECT created, num_comments, score FROM posts WHERE subreddit = ?''', (subreddit_name,))
    posts = c.fetchall()

    # Create a dictionary to store the data for the three visualizations
    data = {
        "posts_per_day": {},
        "comments_per_day": {},
        "average_upvotes_per_day": {}
    }

    # Loop through the posts and aggregate the data
    for post in posts:
        date = datetime.fromtimestamp(post[0]).date()

        # Convert the date to a string in the format YYYY-MM-DD
        date_str = date.strftime("%Y-%m-%d")

        # Aggregate posts per day
        if date_str in data["posts_per_day"]:
            data["posts_per_day"][date_str] += 1
        else:
            data["posts_per_day"][date_str] = 1

        # Aggregate comments per day
        if date_str in data["comments_per_day"]:
            data["comments_per_day"][date_str] += post[1]
        else:
            data["comments_per_day"][date_str] = post[1]

        # Aggregate upvotes per day
        if date_str in data["average_upvotes_per_day"]:
            data["average_upvotes_per_day"][date_str]["sum"] += post[2]
            data["average_upvotes_per_day"][date_str]["count"] += 1
        else:
            data["average_upvotes_per_day"][date_str] = {"sum": post[2], "count": 1}

    # Calculate the average upvotes per day
    for date_str in data["average_upvotes_per_day"]:
        data["average_upvotes_per_day"][date_str] = data["average_upvotes_per_day"][date_str]["sum"] / data["average_upvotes_per_day"][date_str]["count"]

    # Close the database connection
    conn.close()

    return data

if __name__ == "__main__":
    import sys
    import pprint
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '')))
    from data_collector import collector

    if not check_subreddit_data_exists("python"):
        collector.get_top_posts("python")
    print("Analyzed data for Python subreddit:\n")
    pprint.pprint(generate_visualizations_data("python"))
