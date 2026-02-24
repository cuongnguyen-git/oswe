#!/usr/bin/env python3
"""
Clean Python snippet builder – extended with Flask & CLI examples
"""

import sys
from textwrap import dedent

SNIPPETS = {
    "Command Line Arguments": {
        "basic argparse usage": dedent("""\
            import argparse

            parser = argparse.ArgumentParser(
                description="Simple script with arguments"
            )
            parser.add_argument("input_file", help="Path to the input file")
            parser.add_argument("-o", "--output", default="result.txt",
                                help="Output file name (default: result.txt)")
            parser.add_argument("-v", "--verbose", action="store_true",
                                help="Increase output verbosity")

            args = parser.parse_args()

            print(f"Input  : {args.input_file}")
            print(f"Output : {args.output}")
            print(f"Verbose: {args.verbose}")
            """),

        "argparse with subcommands": dedent("""\
            import argparse

            def process(args):
                print(f"Processing {args.file} ...")

            def convert(args):
                print(f"Converting {args.source} → {args.target}")

            parser = argparse.ArgumentParser()
            subparsers = parser.add_subparsers(dest="command", required=True)

            p1 = subparsers.add_parser("process")
            p1.add_argument("file")
            p1.set_defaults(func=process)

            p2 = subparsers.add_parser("convert")
            p2.add_argument("source")
            p2.add_argument("target")
            p2.set_defaults(func=convert)

            args = parser.parse_args()
            args.func(args)
            """),
    },

    "Flask – Basic Setup": {
        "minimal Flask application": dedent("""\
            from flask import Flask

            app = Flask(__name__)

            @app.route("/")
            def home():
                return "<h1>Hello from Flask!</h1>"

            @app.route("/hello/<name>")
            def hello(name):
                return f"<h2>Hello, {name}!</h2>"

            if __name__ == "__main__":
                app.run(host="0.0.0.0", port=5000, debug=True)
            """),

        "Flask with templates (recommended)": dedent("""\
            # File: app.py
            from flask import Flask, render_template

            app = Flask(__name__)

            @app.route("/")
            def index():
                return render_template("index.html", title="Welcome")

            if __name__ == "__main__":
                app.run(debug=True)

            # File: templates/index.html
            <!doctype html>
            <html>
            <head><title>{{ title }}</title></head>
            <body>
              <h1>Hello from Flask</h1>
              <p>Using Jinja2 templates is recommended.</p>
            </body>
            </html>
            """),
    },

    "Flask – Static Files": {
        "serve static files (css/js/images)": dedent("""\
            # Place files in the "static" folder next to app.py

            from flask import Flask, send_from_directory

            app = Flask(__name__, static_folder="static")

            # Optional: custom static route
            @app.route("/assets/<path:filename>")
            def custom_static(filename):
                return send_from_directory("static", filename)

            # Normal usage (recommended):
            # <link rel="stylesheet" href="/static/style.css">
            # <img src="/static/logo.png">
            """),
    },

    "Flask – File Upload": {
        "basic file upload endpoint": dedent("""\
            from flask import Flask, request, redirect, url_for
            from werkzeug.utils import secure_filename
            import os

            app = Flask(__name__)
            UPLOAD_FOLDER = "uploads"
            ALLOWED_EXTENSIONS = {"txt", "pdf", "png", "jpg", "jpeg", "gif"}

            app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)

            def allowed_file(filename):
                return "." in filename and \\
                       filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

            @app.route("/", methods=["GET", "POST"])
            def upload_file():
                if request.method == "POST":
                    if "file" not in request.files:
                        return "No file part", 400
                    file = request.files["file"]
                    if file.filename == "":
                        return "No selected file", 400
                    if file and allowed_file(file.filename):
                        filename = secure_filename(file.filename)
                        file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
                        return f"File '{filename}' uploaded successfully!"
                    else:
                        return "File type not allowed", 400
                return '''
                <!doctype html>
                <title>Upload File</title>
                <h1>Upload a file</h1>
                <form method=post enctype=multipart/form-data>
                  <input type=file name=file>
                  <input type=submit value=Upload>
                </form>
                '''

            if __name__ == "__main__":
                app.run(debug=True)
            """),
    },

    "Flask – Download / Serve Uploaded Files": {
        "download uploaded file": dedent("""\
            from flask import Flask, send_from_directory, abort
            import os

            app = Flask(__name__)
            UPLOAD_FOLDER = "uploads"
            app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

            @app.route("/uploads/<filename>")
            def uploaded_file(filename):
                if os.path.exists(os.path.join(app.config["UPLOAD_FOLDER"], filename)):
                    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)
                else:
                    abort(404)

            # Example link: <a href="/uploads/report.pdf">Download report</a>
            """),
    },

    # ── keep your previous categories ──
    "HTTP / Requests": {  # ... your original content ...
    },
    "Small Web Servers": {  # ... your original content ...
    },
    "File & Data Handling": {  # ... your original content ...
    },
    "Concurrency Basics": {  # ... your original content ...
    }
}

# ────────────────────────────────────────────────────────────────
# The rest of the code (menu, get_nested, main, etc.) stays exactly the same
# Just copy-paste your original menu/navigation logic here
# ────────────────────────────────────────────────────────────────

def print_menu(d, level=0, prefix=""):
    for i, (k, v) in enumerate(d.items(), 1):
        if isinstance(v, dict):
            print(f"{'  ' * level}{prefix}{i}) {k}/")
            print_menu(v, level + 1, f"{prefix}{i}.")
        else:
            print(f"{'  ' * level}{prefix}{i}) {k}")


def get_nested(d, path):
    current = d
    for part in path.split("."):
        if part.isdigit():
            idx = int(part) - 1
            current = list(current.values())[idx]
        else:
            current = current[part]
    return current


def main():
    print("Clean Snippet Builder  (q = quit)\n")

    while True:
        print_menu(SNIPPETS)
        print()
        choice = input("→ ").strip()

        if choice.lower() in ("q", "quit", "exit", ""):
            return

        try:
            snippet = get_nested(SNIPPETS, choice)
        except:
            print("Invalid selection.\n")
            continue

        code = snippet

        print("\n" + "═" * 70)
        print(code.strip())
        print("═" * 70 + "\n")

        if input("Copy to clipboard? [Y/n] ").strip().lower() not in ("n", "no"):
            try:
                import pyperclip
                pyperclip.copy(code.strip())
                print("(copied)\n")
            except ImportError:
                print("(install pyperclip → pip install pyperclip)\n")

        if input("Another? [Y/n] ").strip().lower() in ("n", "no"):
            break
        print("─" * 60 + "\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nBye.")
