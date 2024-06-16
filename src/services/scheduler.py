import aiohttp
import logging

from datetime import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.jobstores.base import JobLookupError

from src.config import Settings
from src.services.mingo import (
    get_all_users_articuls_of_specific_marketplace,
    add_new_prices_to_products
)

scheduler = AsyncIOScheduler()


async def get_product_prices_by_articuls(articuls: list[int], marketplace_name: str) -> dict[int, float]:
    '''Отправляет запрос на сервис парсинга с данными о артикулах и возвращает список цен на эти товары'''
    url = '{}:{}/{}'.format(
        Settings().MARKETPLACE_PRICE_PARSER_SERVICE_HOST,
        Settings().MARKETPLACE_PRICE_PARSER_SERVICE_PORT,
        marketplace_name
    )

    request_body = {
        'articuls': articuls
    }

    prices = dict()

    async with aiohttp.ClientSession() as session:
        response = await session.post(url, json=request_body)
        json_answer = await response.json()
        prices = json_answer['prices']

    return prices


async def write_prices_to_marketpalce_products(chat_id: int, marketplace_name: str) -> None:
    articuls = await get_all_users_articuls_of_specific_marketplace(chat_id, marketplace_name)
    prices = get_product_prices_by_articuls(articuls)
    await add_new_prices_to_products(chat_id, marketplace_name, prices)


def remove_job_by_id(job_id: str) -> None:
    try:
        scheduler.remove_job(job_id)
    except JobLookupError:
        pass


def create_parsing_job_for_user_by_marketplace(chat_id: int, marketplace_name: str, hour: int, minute: int, second: int) -> None:
    job_id = '{}: {}'.format(str(chat_id), marketplace_name)
    remove_job_by_id(job_id)

    time_trigger = CronTrigger(
        hour=hour,
        minute=minute,
        second=second,
        timezone='Europe/Moscow'
    )

    job_kwargs = {
        'chat_id': chat_id,
        'marketplace_name': marketplace_name,
    }

    scheduler.add_job(
        func=write_prices_to_marketpalce_products,
        kwargs=job_kwargs,
        id=job_id,
        trigger=time_trigger,
    )
