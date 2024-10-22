<h1 align="center" style="font-weight: bold;">Notes</h1>

<p align="center">
 <a href="#layout">Layout</a> •
 <a href="#features">Features</a> •
 <a href="#tech">Technologies</a> •
 <a href="#started">Getting Started</a> •
 <a href="#contribute">Contribute</a>
</p>

<p align="center">
  <b>Organize and share your thoughts, projects, ideas and reminders effortlessly</b>
</p>

<div align="center">
  <a href="https://django-note-taking-app.vercel.app/">Visit this project</a>
</div>

<h2 id="layout">🎨 Layout</h2>

<div align="center">
  <img src="/static/img/home.png" alt="Image example" width="800" />
</div>

<h2 id="features">🛠️ Features</h2>

- User authentication
- Create, Read, Update and Delete notes, folders, permissions and tags
- Favorite and Restore notes
- Share notes and folders with other users
- API endpoints for every system operation

<h2 id="tech">💻 Technologies</h2>

- Django
- Django REST
- Postgres
- Tailwind

<h2 id="started">🚀 Getting started</h2>

<h3>Prerequisites</h3>

- Git
- Docker & Docker Compose
- Python

<h3>Cloning</h3>

```bash
git clone https://github.com/lucasNBS/django-note-taking-app.git
cd django-note-taking-app
```

<h3>Config .env variables</h2>

Rename `.env.example` file to `.env` or create your own `.env`using `.env.example` as reference

<h3>Starting</h3>

```bash
python -m venv venv
docker-compose up -d

# Run this on linux or mac
source venv/bin/activate

# Run this on windows
\venv\Scripts\activate

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

```

Project will be runnning on http://localhost:8000

<h2 id="contribute">📫 Contribute</h2>

Found a bug or something that doesn't seem correct? Have ideas for new features? Think that some section of the code can be improved?

Feel free to [create a new issue](https://github.com/lucasNBS/django-note-taking-app/issues/new)
