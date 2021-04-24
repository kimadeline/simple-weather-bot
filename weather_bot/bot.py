# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os
import aiohttp

from botbuilder.core import (
    ActivityHandler,
    TurnContext,
)
from botbuilder.schema import (
    ChannelAccount,
)
from dotenv import load_dotenv

# POST request
URL = "https://api.openweathermap.org/data/2.5/weather"
ENV_KEY = "OWM_API_KEY"

load_dotenv(".env")

OWM_API_KEY = os.getenv(ENV_KEY)


class MyBot(ActivityHandler):
    # See https://aka.ms/about-bot-activity-message to learn more about the message and other activity types.

    async def on_message_activity(self, turn_context: TurnContext):
        city = turn_context.activity.text
        result = await self.get_weather(city)
        weather = result["weather"][0]["description"]

        await turn_context.send_activity(f"Weather for {city}: '{ weather }'")

    async def on_members_added_activity(
        self, members_added: ChannelAccount, turn_context: TurnContext
    ):
        for member_added in members_added:
            if member_added.id != turn_context.activity.recipient.id:
                await turn_context.send_activity("Hello and welcome!")

    async def get_weather(self, city: str):
        """Gets the weather using the OpenWeatherMap API.

        Arguments:
        city {str} -- The city to get weather for.

        Returns:
        dict -- A dictionary containing weather information.
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(
                URL, params={"q": city, "appid": OWM_API_KEY}
            ) as resp:
                return await resp.json()
