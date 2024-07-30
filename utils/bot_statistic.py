import os
from datetime import datetime

import logging
from data_access.statistic import StatisticDataAccess
from data_models.bot import BotData
from data_models.statistic import StatisticData

logger = logging.getLogger(__name__)


class BotStatisticDataAccess:
    def __init__(self, bot: BotData):
        self.bot = bot
        self.data_access = StatisticDataAccess()

    def increase_gif_count(self):
        self.data_access.increase_gif_count(self.bot.name)

    def increase_retweet_count(self, plus: int = 1):
        for _ in range(plus):
            self.data_access.increase_retweet_count(self.bot.name)

    def set_total_groups_count(self, total_groups_count: int):
        self.data_access.set_last_chats_count(self.bot.name, total_groups_count)

    def get(self) -> list[StatisticData] | None:
        # get statistic data by bot name
        bot_name = self.bot.name

        statistic = self.data_access.read()

        filter_statistic = list(filter(lambda stat: bool(self.get_by_name(bot_name)), statistic))

        return filter_statistic

    def get_today(self) -> StatisticData:
        today_date = datetime.now().date().strftime("%d.%m.%Y")

        statistic = next(
            filter(lambda stat: stat.date.strftime("%d.%m.%Y") == today_date and stat.bot_name == self.bot.name,
                   self.data_access.read()),
            StatisticData(
                bot_name=self.bot.name,
                date=datetime.now(),
                gif_count=0,
                retweet_count=0,
                chats_count=0,
            ))

        return statistic

    def get_by_name(self, bot_name):
        self.data_access.get_by_name(bot_name)
