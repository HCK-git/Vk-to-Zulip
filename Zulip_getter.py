import socket
import zulip
from typing import Any, Dict
import time

def file_read():
    """"Функция file_read получает информацию из файла private_inform"""

    with open('Data/private_inform.txt') as f:
        line1 = f.readline()
        arrline1 = line1.split()
        main_token_from_file = arrline1[1]
        line2 = f.readline()
        arrline2 = line2.split()
        id_group_from_file = int(arrline2[1])
        line3 = f.readline()
        arrline3 = line3.split()
        way_to_config_from_file = arrline3[1]
        return main_token_from_file, id_group_from_file, way_to_config_from_file


def zulip_getter():
    """функция zulip_getter получает сообщение из каналов приложения Zulip, возвращая строку вида
       "Пользователь <имя пользователя> написал:
       <сообщение пользователя>"
       Для работы функции не требуются входные данные"""

    with open("Data/Settings.txt", "r") as f:
        line1 = f.readline()
        arrline1 = line1.split()
        user_email_bool = arrline1[1]
        line2 = f.readline()
        arrline2 = line2.split()
        subject_bool = arrline2[1]
        line3 = f.readline()
        arrline3 = line3.split()
        display_recipient_bool = arrline3[1]

    request: Dict[str, Any] = {
        'anchor': 'newest',
        'num_before': 1,
        'num_after': 0
    }

    res = zulip_client.get_messages(request)
    message = res['messages'][0]['content']
    user_name = res['messages'][0]['sender_full_name']
    user_email = res['messages'][0]['sender_email']
    subject = res['messages'][0]['subject']
    display_recipient = res['messages'][0]['display_recipient']
    s = message.find('</span>')
    e = message.find('</p>')
    message = message[s + 8:e].replace('<br>', '')
    if message[0] == ' ':
        message = message[1:len(message)]
    if message[0] == '/':
        message_from_zulip ="ZULIP156324"+message
        return message_from_zulip
    message_from_zulip = ('ZULIP156324Пользователь {}'.format(user_name))
    if user_email_bool == 'True':
        message_from_zulip += f' (email: {user_email})'
    if subject_bool == 'True':
        message_from_zulip += f' в тему "{subject}"'
    if display_recipient_bool == 'True':
        message_from_zulip += f', канал "{display_recipient}",'
    message_from_zulip += f' написал:\n{message}'
    return message_from_zulip

print("Started")
main_token, id_group, way_to_config = file_read()

zulip_client = zulip.Client(config_file="{}".format(way_to_config))

old_message_from_zulip = zulip_getter()

while True:
    time.sleep(2)
    message_from_zulip = zulip_getter()
    if message_from_zulip != old_message_from_zulip:
        with socket.create_connection(("127.0.0.1", 10002)) as sock:
            sock.sendall(message_from_zulip.encode("utf8"))
        old_message_from_zulip = message_from_zulip
        print(old_message_from_zulip)
