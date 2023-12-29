from flask import Flask, request, render_template
import os

app = Flask(__name__)

# Set the environment variables in your system or container

os.environ["OPENAI_API_KEY"] = ""
os.environ["key"] = "some_key"
os.environ["server"] = "some_server"
os.environ["dbname"] = "some_dbname"
os.environ["api_key"] = "some_api_key"

@app.route("/api", methods=["GET", "POST"])
def api():
    # If the request is a GET, render the HTML form
    if request.method == "GET":
        return render_template("form.html")
    # If the request is a POST, get the form data and save it as environment variables
    elif request.method == "POST":
        key = request.form.get("key")
        server = request.form.get("server")
        dbname = request.form.get("dbname")
        api_key = request.form.get("api_key")
        os.environ["key"] = key
        os.environ["server"] = server
        os.environ["dbname"] = dbname
        os.environ["OPENAI_API_KEY"] = api_key
        return "Environment variables saved successfully."


<form action="/api" method="post">
    <label for="key">Key:</label>
    <input type="text" id="key" name="key" value="{{ key }}">
    <label for="server">Server:</label>
    <input type="text" id="server" name="server" value="{{ server }}">
    <label for="dbname">Database name:</label>
    <input type="text" id="dbname" name="dbname" value="{{ dbname }}">
    <label for="api_key">API key:</label>
    <input type="text" id="api_key" name="api_key" value="{{ api_key }}">
    <input type="submit" value="Save">
</form>
