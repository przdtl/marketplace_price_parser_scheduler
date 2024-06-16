from src.database import db


collection = db.document_collection


async def get_all_users_articuls_of_specific_marketplace(chat_id: int, marketplace_name: str) -> list[int]:
    '''Возвращает список артикулов у конкретного пользователя по желаемому маркетплейсу'''
    product_filter = {
        'chat_id': chat_id,
        'marketplace_name': marketplace_name,
    }
    articuls_projection = {
        'articul': True,
        '_id': False
    }
    articuls_cursor = collection.find(product_filter, articuls_projection)
    list_of_articuls_objects = await articuls_cursor.to_list(None)
    list_of_articuls = [obj['articul'] for obj in list_of_articuls_objects]

    return list_of_articuls


async def add_new_price_to_product(chat_id: int, marketplace_name: str, articul: int, new_price: float) -> None:
    '''Добавляет цену в список конкретному товару'''
    product_filter = {
        'chat_id': chat_id,
        'articul': articul,
        'marketplace_name': marketplace_name,
    }

    await collection.update_one(product_filter, {'$push': {'prices': new_price}})


async def add_new_prices_to_products(chat_id: int, marketplace_name: str, prices: dict[int, float]) -> None:

    for articul, new_price in prices.items():
        await add_new_price_to_product(chat_id, marketplace_name, articul, new_price)
