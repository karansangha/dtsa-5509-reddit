import logging
from flask import Flask, request, render_template, redirect, url_for
from .data_collector import collector
from .data_analyzer import analyzer
from prometheus_flask_exporter import PrometheusMetrics

logging.basicConfig(level=logging.INFO)
logging.info("Setting LOGLEVEL to INFO")

app = Flask(__name__)
metrics = PrometheusMetrics(app, group_by='endpoint')
metrics.info("app_info", "App Info, this can be anything you want", version="1.0.0")
common_counter = metrics.counter(
    'by_endpoint_counter', 'Request count by endpoints',
    labels={'endpoint': lambda: request.endpoint}
)

@app.route("/")
@common_counter
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
@common_counter
@metrics.counter(
    'cnt_subreddit', 'Number of invocations per subreddit', labels={
        'subreddit': lambda: request.view_args['subreddit_name'],
        'status': lambda resp: resp.status_code
    })
def subreddit_graphs(subreddit_name):
    if not analyzer.check_subreddit_data_exists(subreddit_name):
        collector.get_top_posts(subreddit_name)

    data = analyzer.generate_visualizations_data(subreddit_name)
    return render_template('subreddit.html', subreddit_name=subreddit_name, data=data)

@app.route("/r/", methods=["POST"])
@common_counter
def subreddit_graphs_form():
    return redirect(url_for("subreddit_graphs", subreddit_name=request.form.get("subreddit_name", "")))

@app.route("/echo_user_input", methods=["POST"])
@common_counter
def echo_input():
    input_text = request.form.get("user_input", "")
    return "<h1>Thank you for using the form!</h1><p>You entered: " + input_text + "</p>"

@app.route("/health")
@common_counter
def health_check():
    return "I'm healthy!"

if __name__ == '__main__':
    app.run()
