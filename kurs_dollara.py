import requests
from bs4 import BeautifulSoup
import time
import smtplib


class Currency:
    # ссылка на страницу с которой будем парсить
    currency_url = 'https://www.google.com/search?sxsrf=ALeKk00z4iQbIPw7txjcpJasYv7dK_NZCA%3A1585477287016&ei=p3aAXtFL3YCTvg__57L4DQ&q=%D0%BA%D1%83%D1%80%D1%81+%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80%D0%B0&oq=%D0%BA%D1%83%D1%80%D1%81+%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80%D0%B0&gs_lcp=CgZwc3ktYWIQDDIECAAQRzIECAAQRzIECAAQRzIECAAQRzIECAAQRzIECAAQRzIECAAQRzIECAAQR1AAWABgrzdoAHAEeACAAQCIAQCSAQCYAQCqAQdnd3Mtd2l6&sclient=psy-ab&ved=0ahUKEwiRu_eTu7_oAhVdwMQBHf-zDN8Q4dUDCAs'
    # заголовки для передачи вместе с url
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}
    current_converted_price = 0
    # разница после которой будет отправлено сообщене на почту
    difference = 2

    def __init__(self):
        # установка курса валюты при создании обьекта
        self.current_converted_price = float(self.get_currency_price().replace(',', '.'))

    # метод получения значения курса
    def get_currency_price(self):
        # парсим всю страницу
        full_page = requests.get(self.currency_url, headers=self.headers)
        # разбираем страницу
        soup = BeautifulSoup(full_page.content, 'html.parser')
        # получаем нужное значение
        convert = soup.findAll("span", {"class": "DFlfde", "class": "SwHCTb", "data-precision": "2"})
        return convert[0].text

    # проверяем изменение курса
    def check_currency(self):
        currency = float(self.get_currency_price().replace(',', '.'))
        if currency >= self.current_converted_price + self.difference:
            print('Курс вырос, продавай баксы!')
            self.send_mail()
        elif currency <= self.current_converted_price - self.difference:
            print('Курс упал. Закупай баксы')
            self.send_mail()
        print('Сейчас курс 1 доллар =  ' + str(currency))
        time.sleep(3)
        self.check_currency()

    # отправляем email через SMTP
    def send_mail(self):
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()

        server.login('dmitriykostarev9987@gmail.com', 'skyiieifdmtzyfdo')
        subject = 'Currency'
        body = 'Currency has been changed'
        message = f'Subject: {subject}\n{body}'

        server.sendmail(
            'From',
            'To',
            message
        )
        server.quit()


# создаем обьект и вызываем метод
currency = Currency()
currency.check_currency()