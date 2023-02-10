from flask import Flask, request, render_template, redirect, url_for
from data_collector import collector
from data_analyzer import analyzer

app = Flask(__name__)


@app.route("/")
def main():
    return '''
     <h1>Reddit Analyzer</h1>
     <form action="/r/" method="POST">
         <label for="subreddit_name">Enter any VALID subreddit name - </label>
         <input name="subreddit_name" value="python">
         <input type="submit" value="Submit!">
     </form>
     '''

@app.route("/r/<subreddit_name>")
def subreddit_graphs(subreddit_name):
    if not analyzer.check_subreddit_data_exists(subreddit_name):
        collector.get_top_posts(subreddit_name)

    labels, post_data, comment_data, avg_score_data = analyzer.generate_visualizations(subreddit_name)
    return render_template('subreddit.html', labels=labels, post_data=post_data, comment_data=comment_data, avg_score_data=avg_score_data)

@app.route("/r/", methods=["POST"])
def subreddit_graphs_form():
    return redirect(url_for("subreddit_graphs", subreddit_name=request.form.get("subreddit_name", "")))

if __name__ == '__main__':
    app.run(debug=True)
