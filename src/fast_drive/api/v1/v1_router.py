from fastapi import APIRouter

from .auth.api import router as auth_router
from .file.api import router as file_router
from .test.api import router as test_router

router = APIRouter(prefix="/api/v1")

router.include_router(auth_router)
router.include_router(file_router)
router.include_router(test_router)

__all__ = ["router"]
