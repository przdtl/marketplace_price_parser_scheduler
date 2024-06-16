from datetime import datetime

from fastapi import APIRouter

from src.services.scheduler import create_parsing_job_for_user_by_marketplace

router = APIRouter()


@router.post(
    '/scrapping_time',
)
async def set_time_handler(chat_id: int, marketplace_name: str, hour: int, minute: int, second: int):
    create_parsing_job_for_user_by_marketplace(
        chat_id, marketplace_name, hour, minute, second
    )
