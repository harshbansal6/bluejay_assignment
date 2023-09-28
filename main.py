from fastapi import FastAPI
import uvicorn
from starlette.middleware.cors import CORSMiddleware
from app.excel.routes.excel_r import router

def get_application() -> FastAPI:
    application = FastAPI()

    origins = ["*"]
    application.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return application

app = get_application()

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app=app, host="0.0.0.0", port=8008)
