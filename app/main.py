from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import sports, leagues, fixtures, betslip, main as main_routes, mail, verify

app = FastAPI(title="SmartSlip API", version="1.0.0")

# CORS for local frontend dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(sports.router, prefix="/api/sports", tags=["Sports"])
app.include_router(leagues.router, prefix="/api/leagues", tags=["Leagues"])
app.include_router(fixtures.router, prefix="/api/fixtures", tags=["Fixtures"])
app.include_router(betslip.router, prefix="/api/betslip", tags=["Betslip"])
app.include_router(main_routes.router)
app.include_router(mail.router, prefix="/api/mail", tags=["Mail"])
app.include_router(verify.router, prefix="/api", tags=["Verify"])

@app.get("/")
def root():
    return {"message": "SmartSlip is running"}
