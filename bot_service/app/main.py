from fastapi import FastAPI


app = FastAPI(
    title="Bot Service",
    description="Telegram bot service",
    version="1.0.0",
)


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "bot_service",
    }

