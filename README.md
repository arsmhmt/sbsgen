
# SmartBetSlip

## Setup Instructions

1. Clone the repository:
   ```sh
   git clone https://github.com/arsmhmt/sbsgen.git
   cd sbsgen
   ```

2. Copy and configure environment variables:
   ```sh
   cp .env.example .env
   # Edit .env with your secrets
   ```

3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

4. Run the app locally:
   ```sh
   uvicorn app.main:app --reload
   ```

5. Deployment (Fly.io or GCP Cloud Run):
   - Use the provided `Procfile` or `Dockerfile`.
   - Move secrets (FLASK_SECRET_KEY, GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET) to your platform's secret manager.

## Features
- FastAPI backend
- Freemium controls
- Email verification
- Admin panel
- Monetization (ads, pricing)
- Internationalization (EN/TR)
- AI-powered betslip predictions

## Contributing
Pull requests and issues welcome!
