import asyncio
import re
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
from database.db import SessionLocal, VacancyHistory


async def fetch_and_store_vacancies():
    print("fetch_and_store_vacancies started")
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    driver.get("https://robota.ua/zapros/junior/ukraine")
    await asyncio.sleep(5)

    vacancy_count = driver.find_element(By.XPATH, "//div[contains(text(), ' вакан')]").text
    vacancy_count = vacancy_count.replace(" ", "")
    regex = r"\d+"
    vacancy_count = int(re.findall(regex, str(vacancy_count))[0])
    driver.close()

    db = SessionLocal()
    last_record = db.query(VacancyHistory).order_by(VacancyHistory.query_time.desc()).first()
    if last_record:
        change = vacancy_count - last_record.vacancy_count
    else:
        change = vacancy_count
    datetime_with_hours = datetime(datetime.now().year, datetime.now().month, datetime.now().day, datetime.now().hour, datetime.now().minute)
    db.add(VacancyHistory(query_time=datetime_with_hours, vacancy_count=vacancy_count, change=change))
    db.commit()
    db.close()


if __name__ == '__main__':
    fetched_jobs_amount = fetch_and_store_vacancies()
