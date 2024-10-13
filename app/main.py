import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, APIRouter, UploadFile, File, HTTPException, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse

from app.services.file_service import FileService
from app.utils.cache import connect_redis, disconnect_redis
from app.utils.exceptions import FLException
import app.utils.logger

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    connect_redis()
    yield

    disconnect_redis()

app = FastAPI(lifespan=lifespan)
api_router = APIRouter()

templates = Jinja2Templates(directory="app/templates")

file_service = FileService("file_storage")


@app.get("/")
async def main():
    logger.info('main...')
    return FileResponse(path='app/templates/index.html', status_code=200)


@api_router.post("/upload")
async def upload_file(request: Request, file: UploadFile = File(...), search_word: str = "Quantori"):
    logger.info('upload_file...')
    if not file:
        raise HTTPException(status_code=400, detail="File not exists")

    try:
        is_word_exists, output_valid_file, output_invalid_file = await file_service.process_file(file, search_word)
        logger.info(f'results: {is_word_exists}, {output_valid_file}, {output_invalid_file}')
        res = {
            "is_word_exists": is_word_exists
        }
        if output_valid_file:
            res["output_valid_file"] = output_valid_file
        if output_invalid_file:
            res["output_invalid_file"] = output_invalid_file

        return templates.TemplateResponse("result.html", {
            "request": request,
            **res
        })
    except FLException as e:
        logger.error(e.message)
        raise HTTPException(status_code=e.status_code, detail=e.message)
    # except Exception as e:
    #     logger.error(e.message)
    #     raise HTTPException(status_code=500, detail=str(e))


app.include_router(api_router, prefix="/api")
