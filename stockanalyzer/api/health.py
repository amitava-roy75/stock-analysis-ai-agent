from fastapi import APIRouter
from config.settings import settings

router = APIRouter()


@router.get("/")
def home():

    return {
        "application": settings.app_name,
        "version": settings.app_version,
        "status": "UP"
    }


@router.get("/health")
def health():

    return {
        "status": "UP"
    }