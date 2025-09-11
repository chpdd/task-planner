import uvicorn
from app.logging_middleware import log_config

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True, access_log=False, log_config=log_config)
