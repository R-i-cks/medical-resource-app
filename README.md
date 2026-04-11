# Medical Resource App

A Flask web application for browsing and searching a multilingual medical terminology database, with built-in on-demand translation and Word2Vec semantic similarity support.

## Features

- Browse medical concepts in Portuguese, English, and Spanish
- Full-text search across concept names and definitions
- On-demand translation to any language via Google Translate
- Word2Vec-based semantic similarity between medical terms (pre-computed; Gensim not required at runtime)
- Concept detail pages showing definitions, synonyms, related terms, sources, and grammatical category
- Q&A interface scaffolding for NLP-based question answering
- Deployed on Render with Gunicorn

## Tech Stack

| Layer | Technology |
|---|---|
| Web framework | Flask 3.0.3 |
| NLP / embeddings | NumPy |
| Translation | deep-translator (Google Translate) |
| Templating | Jinja2 |
| Server | Gunicorn |
| Runtime | Python 3.11.5 |

## Run Locally

**Prerequisites:** Python 3.11.5

```bash
# 1. Clone the repository
git clone https://github.com/R-i-cks/medical-resource-app.git
cd medical-resource-app

# 2. Create and activate a virtual environment
python3 -m venv env
source env/bin/activate        # Windows: env\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Start the development server
flask run
```

The app will be available at `http://127.0.0.1:5000`.

## Live Demo

https://medical-resource-app.onrender.com

## Project Structure

```
medical-resource-app/
├── app.py                              # Flask application and route handlers
├── requirements.txt                    # Python dependencies
├── runtime.txt                         # Python version for Render
├── Procfile                            # Gunicorn startup command for Render
├── modelo.w2v                          # Pre-computed Word2Vec model
├── medicina.json                       # Core medical data
├── conceitos_relacoes_e_sinonimos.json # Concept relationships and synonyms
├── dicionarios/                        # Multilingual concept dictionaries (pt/en/es)
├── similaridade/                       # Word2Vec similarity scripts and models
├── templates/                          # Jinja2 HTML templates
│   ├── layout.html
│   ├── home.html
│   ├── conceitos.html                  # Concept search/browse page
│   ├── conc.html                       # Individual concept detail page
│   ├── pesquisaDetalhada.html          # Detailed search results page
│   ├── table.html                      # Tabular results view
│   └── qa.html                         # Q&A interface
└── static/                             # CSS, JS, and other static assets
```
