import os
import json
from flask import Flask, render_template, request, redirect, url_for, session, abort
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)
app.secret_key = os.urandom(24)

DATA_FILE = "data/posts.json"
ADMIN_USERNAME = os.getenv("username", "admin")
ADMIN_PASSWORD = os.getenv("password", "secret")


def load_posts():
    """Read articles from JSON file. Return [] if file doesn't exist or is empty."""
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        content = f.read().strip()
        if not content:
            return []
        return json.loads(content)


def save_posts(posts):
    """Write the list of articles back to disk."""
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(posts, f, ensure_ascii=False, indent=2)


def get_next_id(posts):
    """Simple incrementing ID."""
    if not posts:
        return 1
    return max(post["id"] for post in posts) + 1


def is_admin():
    return session.get("logged_in") is True


@app.route("/")
def index():
    posts = load_posts()
    posts.sort(key=lambda post: post.get("created_at", ""), reverse=True)
    return render_template("index.html", posts=posts)


@app.route("/post/<int:post_id>")
def article(post_id):
    posts = load_posts()
    for post in posts:
        if post["id"] == post_id:
            return render_template("view_article.html", post=post)
    abort(404)


@app.route("/admin/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session["logged_in"] = True
            return redirect(url_for("dashboard"))
        return render_template("login.html", error="Invalid credentials")
    return render_template("login.html")


@app.route("/admin")
def dashboard():
    if not is_admin():
        return redirect(url_for("login"))
    posts = load_posts()
    posts.sort(key=lambda post: post.get("created_at", ""), reverse=True)
    return render_template("dashboard.html", posts=posts)


@app.route("/admin/add", methods=["GET", "POST"])
def add_article():
    if not is_admin():
        return redirect(url_for("login"))
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        content = request.form.get("content", "").strip()
        date = request.form.get("date", "").strip()
        if not title or not content or not date:
            return render_template("add_article.html", error="Title, content, and date are required")
        posts = load_posts()
        new_post = {
            "id": get_next_id(posts),
            "title": title,
            "content": content,
            "created_at": date,
        }
        posts.append(new_post)
        save_posts(posts)
        return redirect(url_for("dashboard"))
    return render_template("add_article.html")


@app.route("/admin/edit/<int:post_id>", methods=["GET", "POST"])
def edit_article(post_id):
    if not is_admin():
        return redirect(url_for("login"))
    posts = load_posts()
    post = next((p for p in posts if p["id"] == post_id), None)
    if not post:
        abort(404)
    if request.method == "POST":
        post["title"] = request.form.get("title", "").strip()
        post["content"] = request.form.get("content", "").strip()
        post["created_at"] = request.form.get("date", "").strip()
        save_posts(posts)
        return redirect(url_for("dashboard"))
    return render_template("edit_article.html", post=post)


@app.route("/admin/delete/<int:post_id>", methods=["POST"])
def delete_article(post_id):
    if not is_admin():
        return redirect(url_for("login"))
    posts = load_posts()
    posts = [post for post in posts if post["id"] != post_id]
    save_posts(posts)
    return redirect(url_for("dashboard"))


@app.route("/admin/logout")
def logout():
    session.pop("logged_in", None)
    return redirect(url_for("login"))


def main():
    app.run(debug=True)


if __name__ == "__main__":
    main()
