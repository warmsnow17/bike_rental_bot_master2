from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware
from database.models import Option


class OptionMiddleware(BaseMiddleware):

    async def load_options(self, data: dict):
        options = await Option.all()
        data['options'] = {}
        for option in options:
            data['options'][option.key] = option.value

    async def on_pre_process_message(self, message: types.Message, data: dict):
        await self.load_options(data)

    async def on_pre_process_callback_query(self, query: types.InlineQuery, data: dict):
        await self.load_options(data)



from math import radians, sin, cos, sqrt, atan2

def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371  # радиус Земли в километрах

    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))

    distance = R * c
    return distance
