import asyncio
import os

import pandas as pd
from aiogram import Bot, Dispatcher, types
from aiogram.enums.parse_mode import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile
from dotenv import load_dotenv

from database.db import SessionLocal, VacancyHistory

# Load environment variables from .env
load_dotenv()

# Initialize bot and dispatcher

bot = Bot(token=os.getenv('BOT_TOKEN'))
dp = Dispatcher()


@dp.message(CommandStart())
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Hi! I'm a Bot counting vacancies on Robota.ua")


def generate_excel_report(data):
    # sort data by datatime first newest
    sorted_data = sorted(data, key=lambda x: x['datatime'], reverse=True)
    # Generate a pandas DataFrame
    df = pd.DataFrame(sorted_data, columns=['datatime', 'vacancy_count', 'change'])

    # Create Excel writer
    writer = pd.ExcelWriter('report.xlsx', engine='xlsxwriter')

    # Write DataFrame to Excel without the header
    df.to_excel(writer, index=False, startrow=1, header=False)

    # Get workbook and worksheet objects
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']

    # Define header format
    header_format = workbook.add_format({
        'bold': True,
        'text_wrap': True,
        'valign': 'top',
        'fg_color': '#FFFF00',  # Yellow color
        'border': 1
    })

    # Write the column headers with the defined format
    for col_num, value in enumerate(df.columns.values):
        worksheet.write(0, col_num, value, header_format)

    # Adjust column width
    for i, col in enumerate(df.columns):
        width = max(df[col].astype(str).map(len).max(), len(col))
        worksheet.set_column(i, i, width)

    # Save the file
    writer.close()


async def send_excel_file(chat_id):
    db = SessionLocal()
    query = db.query(VacancyHistory).order_by(VacancyHistory.query_time)

    data = []
    datetime_pattern = '%d.%m.%Y %H:%M'
    for history in query:
        data.append({
            "datatime": history.query_time.strftime(datetime_pattern),
            "vacancy_count": str(history.vacancy_count),
            "change": str(history.change)
        })


    generate_excel_report(data)

    document = FSInputFile(path='report.xlsx')
    await bot.send_document(chat_id=chat_id, document=document)


# Handler to respond to /send_report command
@dp.message(Command("get_today_statistic"))
async def get_today_statistic(message: types.Message):
    chat_id = message.from_user.id
    await send_excel_file(chat_id)


async def run_bot():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(run_bot())