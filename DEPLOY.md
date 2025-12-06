# Deployment Guide

The easiest way to deploy this project (Frontend + Backend) for free is using **Vercel**.

## Recommended: Vercel (Frontend + Backend)

This method deploys both the Next.js frontend and the Python Flask backend to Vercel. It's free, fast, and doesn't "sleep" like Render.

### Prerequisites
1.  A [GitHub](https://github.com) account.
2.  A [Vercel](https://vercel.com) account (you can sign up with GitHub).

### Steps

1.  **Push to GitHub**:
    *   Create a new repository on GitHub.
    *   Push this entire project code to that repository.

2.  **Import to Vercel**:
    *   Go to your [Vercel Dashboard](https://vercel.com/dashboard).
    *   Click **"Add New..."** -> **"Project"**.
    *   Select your GitHub repository and click **"Import"**.

3.  **Configure Project**:
    *   **Framework Preset**: Vercel should automatically detect `Next.js`.
    *   **Root Directory**: Leave as `./` (default).
    *   **Build Command**: `npm install --prefix frontend && npm run build --prefix frontend`
        *   *Note*: You might need to override the default build command in the "Build & Development Settings" section.
    *   **Output Directory**: `frontend/.next`
    *   **Environment Variables**:
        *   Add `SECRET_KEY` with a random value (e.g., `my-super-secret-key`).
        *   *You do NOT need to set `NEXT_PUBLIC_API_URL` - the code automatically handles it.*

4.  **Deploy**:
    *   Click **"Deploy"**.
    *   Vercel will build the frontend and set up the Python serverless functions.

5.  **Done!**
    *   Visit your new URL (e.g., `https://disease-prediction.vercel.app`).
    *   The frontend will automatically talk to the backend on the same domain.

---

## Alternative: Docker (Local / VPS)

If you want to run it locally or on a VPS:

1.  Install Docker and Docker Compose.
2.  Run:
    ```bash
    docker-compose up --build
    ```
3.  Open `http://localhost:3000`.
