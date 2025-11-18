# Disease Prediction and Medicine Recommendation System

This Flask app predicts diseases from user-provided symptoms and returns precautions, medications, diets, and workout recommendations.

## Deploying to Render (free tier)

Prerequisites:

- Push this repository to GitHub (or connect your git provider to Render).
- Ensure `svc.pkl` and all CSV files (`symptoms.csv`, `medications.csv`, etc.) are in the repo and committed.

Recommended changes already applied in this repo:

- Loads CSVs and `svc.pkl` using project-relative paths.
- Uses `SECRET_KEY` environment variable for Flask secret.
- Reads `PORT` and `HOST` environment variables for production.
- Added `/health` endpoint for health checks.

Steps to deploy:

1. Go to https://render.com and sign up (free tier available).
2. Create a new **Web Service** and connect your GitHub repo.
3. Build Command: `pip install -r requirements.txt`
4. Start Command: `gunicorn main:app`
5. Add Environment Variables in Render service settings:
   - `SECRET_KEY` : a secure random string
   - `FLASK_DEBUG` : `0` (ensure debug is off in production)
6. Deploy. Render will run the build and start the service.

Health check: Render will hit `https://<your-service>.onrender.com/health` — this returns `ok`.

Local testing:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:SECRET_KEY = 'replace-with-a-secret'
$env:FLASK_DEBUG = '1'  # optional for local debugging
python .\main.py
```

Notes & Recommendations:

- Pinning versions in `requirements.txt` helps avoid surprises.
- Make sure `svc.pkl` was created by you/trusted source; loading arbitrary pickles can be unsafe.
- Consider adding a `Dockerfile` for more consistent deployments across providers.

If you want, I can:

- Create a `Dockerfile` for container deployment.
- Add a small `render.yaml` for infrastructure as code with Render.
- Run a quick smoke test locally (requires installing packages and having the model file present).

Docker (quick start)

Build the image from the repo root and run it locally:

```powershell
docker build -t disease-predict:latest .
docker run -e SECRET_KEY='dev-secret' -p 5000:5000 disease-predict:latest
```

On the container the app listens on the port provided by the `PORT` environment variable (defaults to `5000`).

Quick Render notes

- If you prefer Docker, in Render choose **Deploy using a Dockerfile** when creating the Web Service.
- Otherwise use the Build and Start commands from the Render steps above.

If you'd like, I already added a minimal `Dockerfile` — tell me if you want me to also add a `render.yaml` or run a local smoke test now.
