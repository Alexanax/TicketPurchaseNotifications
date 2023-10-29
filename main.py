import time
from bs4 import BeautifulSoup
import requests

date_of_match = '18 Ноября'

TOKEN = "6713595400:AAGmddBYjLskHWg8NX7VmPX9tKif1iNK9As"
chat_ids = ["435521817", "1292115978"]
message = f"Появилась возможность купить билет на матч который будет {date_of_match}"

trigger = True


def check_ticket():
    global trigger
    while trigger:
        try:
            html = requests.get('https://hctorpedo.ru/tickets/').text
            soup = BeautifulSoup(html, "html.parser")
            cards = soup.find_all('span', class_='sliderCard__content-center-bigDate')
            for card in cards:
                if card.text.__contains__(date_of_match):
                    if card.parent.parent.parent.find('a', class_='btn sliderCard__head-btn') is not None:
                        print('Найдено событие, отправляю уведомление в телеграмм')
                        send_notification()
                        trigger = False
                        break
                    else:
                        print('Не найдено событие, пробую еще раз через 10 минут')
                        time.sleep(600)
        except Exception as e:
            print(f"Произошла ошибка {e} при вызове https://hctorpedo.ru/tickets/, попробуем еще раз через 5 минут")
            time.sleep(600)


def send_notification():
    while True:
        try:
            for chat_id in chat_ids:
                url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
                requests.get(url)
                print('Отправил уведомление в телеграмм')
            break
        except Exception as e:
            print(f"Произошла ошибка {e} при вызове sendMessage, попробуем еще раз через 5 секунд")
            time.sleep(5)


if __name__ == '__main__':
    check_ticket()