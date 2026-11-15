# Personal Blog

A simple, server-rendered personal blog built with **Python + Flask**. It has a public guest section (read articles) and a password-protected admin section (create, edit, delete articles). Articles are stored as plain JSON on the filesystem — no database required.

Built as a solution to the [roadmap.sh Personal Blog project](https://roadmap.sh/projects/personal-blog).

---

## ✨ Features

### Guest section (public)

- **Home page** — lists all published articles, newest first
- **Article page** — shows the full article with its publication date

### Admin section (protected)

- **Login** — session-based authentication (single admin account)
- **Dashboard** — table of all articles with edit/delete actions
- **Add Article** — form with title, date, and content fields
- **Edit Article** — pre-filled form to update an existing article
- **Delete** — confirmation prompt before removing an article

---

## 🧰 Tech Stack

| Layer      | Technology                                    |
| ---------- | --------------------------------------------- |
| Backend    | Python 3.8+, Flask                            |
| Templating | Jinja2 (bundled with Flask)                   |
| Storage    | JSON file (`data/posts.json`)                 |
| Frontend   | HTML + CSS (no JavaScript framework)          |
| Auth       | Flask sessions + hardcoded secret credentials |

---

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or newer
- `pip`

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/personal-blog.git
cd personal-blog

# 2. (Recommended) create a virtual environment
python -m venv venv
source venv/bin/activate        # macOS / Linux
# venv\Scripts\activate         # Windows

# 3. Install dependencies
pip install -r requirements.txt
```
