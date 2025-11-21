import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware

from src.service.config import config
from src.service.router import router as api_router


# -- init app --
app = FastAPI(
    title=config.APP_TITLE,
    description=config.APP_DESCRIPTION,
    version=config.APP_VERSION,
    # lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

@app.get("/healthz", include_in_schema=False)
def healthz():
    return Response(status_code=204)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=9090, reload=True)
