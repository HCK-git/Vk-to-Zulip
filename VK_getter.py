import socket
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType


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


def vk_getter():
    """функция vk_getter получает сообщение из бесед социальной сети Вконтакте,
       в которых состоит бот, возвращая строку вида
       "Пользователь <имя пользователя> написал:
       <сообщение пользователя>"
       Для работы функции не требуются входные данные"""
    for event in longpoll.listen():
        with open("Data/Settings.txt", "r") as f:
            f.readline()
            f.readline()
            f.readline()
            line4 = f.readline()
            arrline4 = line4.split()
            vk_id = arrline4[1]

        if event.type == VkBotEventType.MESSAGE_NEW and event.from_chat:
            id_chat = event.chat_id
            with open("Data/id_chat.txt", "w") as f:
                f.write(str(id_chat))
            user_id = event.message.get('from_id')
            message_vk = event.message.get('text')
            user = vk_session.method("users.get", {"user_ids": user_id})
            if message_vk[0] == '/':
                message_from_vk = "VK156324"+message_vk
                return message_from_vk
            print("vk_id: ", vk_id)
            if vk_id == 'False':
                message_from_vk = ("VK156324Пользователь {} {} написал:\n{}".format(user[0]['last_name'],
                                                                                    user[0]['first_name'], message_vk))
            else:
                message_from_vk = ("VK156324Пользователь {} {} (id: {}) написал:\n{}".format(user[0]['last_name'],
                                                                                             user[0]['first_name'],
                                                                                             user_id, message_vk))
            return message_from_vk

print("Started")
main_token, id_group, way_to_config = file_read()

vk_session = vk_api.VkApi(token=main_token)

longpoll = VkBotLongPoll(vk_session, id_group)

old_message_from_vk = None

while True:
    message_from_vk = vk_getter()
    if message_from_vk != old_message_from_vk:
        with socket.create_connection(("127.0.0.1", 10002)) as sock:
            sock.sendall(message_from_vk.encode("utf8"))
        old_message_from_vk = message_from_vk
