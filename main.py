from fastapi import BackgroundTasks, FastAPI, Request

from app.routers.mock import mock_router
from app.services.gmail.parser import process_gmail_update
from app.services.gmail.watcher import watch_gmail

app = FastAPI()
app.include_router(mock_router, tags=["Mock"])


@app.post("/webhook")
async def gmail_webhook(request: Request, background_tasks: BackgroundTasks):
    """
    Receives Gmail Pub/Sub push notifications.
    Returns 200 immediately so Pub/Sub does not retry; processing runs in background.
    """
    data = await request.json()

    if not data.get("message"):
        return {"status": "ignored", "reason": "Missing message data"}

    background_tasks.add_task(process_gmail_update, data)
    return {"status": "accepted"}


@app.get("/refresh")
async def refresh_token():
    watch_gmail()
