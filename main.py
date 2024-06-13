import asyncio
import schedule
from parser.parser import fetch_and_store_vacancies
from bot.bot import run_bot


async def run_parser_job():
    print("run_parser_job started")
    await fetch_and_store_vacancies()


async def run_bot_job():
    print("run_bot_job started")
    await run_bot()


async def main():
    schedule.every().hour.do(lambda: asyncio.ensure_future(run_parser_job()))

    bot_task = asyncio.create_task(run_bot_job())

    while True:
        schedule.run_pending()
        await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(main())
