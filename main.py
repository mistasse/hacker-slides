from flask import Flask, render_template, request
from argparse import ArgumentParser
import os

parser = ArgumentParser(description="Runs a OrgSlides instance")

parser.add_argument("-d", "--directory", default="slides",
                    help="Directory to load and save the files from")

args = parser.parse_args()

root = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)

@app.route("/")
@app.route("/list")
def index():
    files = []
    for dirpath, dirnames, filenames in os.walk(args.directory):
        for filename in filenames:
            path = os.path.join(dirpath, filename)
            path = os.path.relpath(path, args.directory)
            files.append(path)
    files.sort()
    return render_template("list.html", files=files)

@app.route("/edit/<filename>", methods=["GET"])
def edit(filename):
    return render_template("edit.html", filename=filename)

@app.route("/get/<filename>", methods=["GET"])
def get(filename):
    with open(os.path.join(args.directory, filename), "r") as f:
        content = f.readlines()
    return "".join(content)

@app.route("/save/<filename>", methods=["POST"])
def save(filename):
    with open(os.path.join(args.directory, filename), "w") as f:
        f.write(request.form["content"])
    return "ok"

@app.route("/published/<filename>")
def preview(filename):
    return render_template("slides.html", filename=filename)

if __name__ == "__main__":
    app.run(port=5000)