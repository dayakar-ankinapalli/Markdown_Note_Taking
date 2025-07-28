# Markdown Note-Taking API

A RESTful API for a note-taking application that allows users to create, read, update, and delete notes in Markdown, render them as HTML, and check their grammar.

## Features

- **Full CRUD for Notes**: Create, retrieve, update, and delete notes.
- **Markdown Rendering**: Convert a Markdown note into HTML on the fly.
- **Grammar Checking**: Check the grammar of any given text.
- **Structured Project**: Built with Flask Blueprints for scalability.
- **Tested**: Includes a full suite of unit tests with `pytest`.

## Prerequisites

- Python 3.7+
- `pip` for installing packages.
- Java (required by the `language-tool-python` library).

## Getting Started

### 1. Clone the Repository

```sh
git clone <repository-url>
cd markdown-note-app
```

### 2. Create a Virtual Environment

It's recommended to use a virtual environment to manage project dependencies.

```sh
# For Unix/macOS
python3 -m venv venv
source venv/bin/activate

# For Windows
python -m venv venv
.\venv\Scripts\activate
```

### 3. Install Dependencies

```sh
pip install -r requirements.txt
```

**Note**: The first time you run the application, `language-tool-python` will download its language models, which requires an internet connection.

### 4. Run the Application

```sh
python run.py
```

The API server will start on `http://localhost:5000`.

### 5. Run Tests

```sh
pytest
```

## API Endpoints

### Notes (`/notes`)

- **`POST /notes`**: Creates a new note.
- **`GET /notes`**: Retrieves a list of all note filenames.
- **`GET /notes/<filename>`**: Retrieves the raw Markdown content of a specific note.
- **`PUT /notes/<filename>`**: Updates the content of an existing note.
- **`DELETE /notes/<filename>`**: Deletes a specific note.
- **`GET /notes/<filename>/render`**: Renders a specific note as HTML.

### Grammar (`/check-grammar`)

- **`POST /check-grammar`**: Checks the grammar of a given text.

