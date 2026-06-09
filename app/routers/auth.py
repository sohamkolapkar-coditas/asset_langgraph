from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from google_auth_oauthlib.flow import Flow

SCOPES = ["https://mail.google.com/"]
REDIRECT_URI = "http://localhost:8000/oauth2callback"

auth_router = APIRouter()


@auth_router.get("/reauth")
async def reauth():
    flow = Flow.from_client_secrets_file(
        "credentials.json",
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI,
    )
    auth_url, _ = flow.authorization_url(
        access_type="offline",
        prompt="consent",
        include_granted_scopes="true",
    )
    return RedirectResponse(auth_url)


@auth_router.get("/oauth2callback")
async def oauth2callback(code: str, state: str = None):
    flow = Flow.from_client_secrets_file(
        "credentials.json",
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI,
    )
    flow.fetch_token(code=code)
    creds = flow.credentials
    with open("token.json", "w") as token:
        token.write(creds.to_json())
    return {"status": "authenticated", "message": "Gmail token saved. Server is ready."}
