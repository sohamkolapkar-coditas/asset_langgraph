from fastapi import FastAPI, Request
from app.services.gmail.parser import process_gmail_update
from app.services.gmail.watcher import watch_gmail
from app.routers.mock import mock_router
from app.routers.auth import auth_router

app = FastAPI()
app.include_router(mock_router, tags=["Mock"])
app.include_router(auth_router, tags=["Auth"])


@app.post("/webhook")
async def gmail_webhook(request: Request):
    """
    Receives the push notification and processes it in the background.
    """
    data = await request.json()

    # Verify this is a valid Pub/Sub push
    if not data.get("message"):
        return {"status": "ignored", "reason": "Missing message data"}

    # Run processing in background to keep the webhook response fast
    # background_tasks.add_task(process_gmail_update, data)
    result = process_gmail_update(data=data)


    return result


@app.get("/refresh")
async def refresh_token():
    watch_gmail()
