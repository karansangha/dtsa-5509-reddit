from flask import Flask, request

app = Flask(__name__)


@app.route("/")
def main():
    return '''
     <h1>Twitter Analyzer</h1>
     <form action="/echo_user_input" method="POST">
         <label for="user_input">Enter any text - </label>
         <input name="user_input">
         <input type="submit" value="Submit!">
     </form>
     '''


@app.route("/echo_user_input", methods=["POST"])
def echo_input():
    input_text = request.form.get("user_input", "")
    return "<h1>Thank you for using the form!</h1><p>You entered: " + input_text + "</p>"

if __name__ == '__main__':
    app.run(debug=True)
