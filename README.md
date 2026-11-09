# Gasiram P Portfolio

## Run locally

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

Open `http://127.0.0.1:5000`. Contact form submissions are validated by the Flask
API and stored in `instance/contacts.sqlite3`.
