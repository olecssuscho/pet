from fastapi import FastAPI,Request
from database import engine
import dbmodels
from routers import tasks,users
import uvicorn
from fastapi.responses import JSONResponse
import logging
app=FastAPI()

dbmodels.Base.metadata.create_all(bind=engine)
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled error: {exc}", exc_info=True)
    return JSONResponse(status_code=500, content={"detail": str(exc)})

app.include_router(tasks.router)
app.include_router(users.router)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        reload_excludes=["__pycache__"],
        log_level="debug"
    )

