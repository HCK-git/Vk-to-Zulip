import socket
import vk_api
import zulip
from vk_api.bot_longpoll import VkBotLongPoll

def file_read():
    """Функция file_read получает информацию из файла private_inform"""

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


def zulip_sender(message):
    """Функция zulip_sender осуществляет отправку сообщений в чат Zulip.
       Для работы функции ей необходимо передать само сообщение."""

    request = {
        "type": "stream",
        "to": "general",
        "topic": "Castle",
        "content": message,
    }
    return zulip_client.send_message(request)


def vk_sender(id_chat, message):
    """Функция vk_sender осуществляет отправку сообщений в беседу ВК.
       Для работы функции ей необходимо передать id беседы и само сообщение."""

    vk_session.method('messages.send', {'chat_id': id_chat, 'message': message, 'random_id': 0})

from subprocess import Popen
Popen('python Zulip_getter.py')
Popen('python VK_getter.py')



main_token, id_group, way_to_config = file_read()

zulip_client = zulip.Client(config_file="{}".format(way_to_config))
vk_session = vk_api.VkApi(token=main_token)
longpoll = VkBotLongPoll(vk_session, id_group)

user_email_bool = False
subject_bool = False
display_recipient_bool = False
stop = True
start = False
old_text_zulip = None
old_text_vk = None
help_message = "/start - запускает бота\n" \
               "/stop - выключает бота\n" \
               "/include email true(false) - добавление в сообщение email пользователя," \
               " отправившего сообщение из Zulip\n" \
               "/include display_recipient true(false) - добавление в сообщение название канала Zulip," \
               " из которого пришло сообшение\n" \
               "/include subject true(false) - добавление в сообщение темы канала Zulip, из которого пришло сообщение\n"

with open("Data/id_chat.txt", "r") as f:
    id_chat = f.readline()

with open("Data/Settings.txt", "w") as f:
    f.write("user_email_bool: False\n")
    f.write("subject_bool: False\n")
    f.write("display_recipient_bool: False\n")


with socket.socket() as sock:
    sock.bind(("127.0.0.1", 10002))
    sock.listen()

    while stop:
        conn, addr = sock.accept()
        with conn:
            data = conn.recv(1024)
            data = data.decode("utf8")

            length = len(data)
            position = data.find('\n')
            if not('\n' in data):
                position = data.find('4')
            text = data[position+1:length]

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


            if "ZULIP156324" in data and (old_text_zulip == None or not(text in old_text_zulip)):
                l = len(data)
                message_from_zulip = data[11:l]
                l2 = len(message_from_zulip)
                pos = message_from_zulip.find("\n")
                old_text_zulip = message_from_zulip[pos+1:l2]
                message_from_zulip = data[11:l]
                if start is True and message_from_zulip[0] != '/':
                    vk_sender(id_chat, message_from_zulip)
                elif start is False:
                    zulip_sender(
                        'Бот не запущен. Напишите "/start" в беседу Вконтакте, в которой есть этот бот')
                elif start is True and ('/help' in message_from_zulip):
                    zulip_sender(help_message)
                elif start is True and ('/stop' in message_from_zulip):
                    stop = False
                    vk_sender(id_chat, 'Бот прекратил свою работу')
                    zulip_sender('Бот прекратил свою работу')
                elif start is True and ('/include email true' in message_from_zulip) \
                        and user_email_bool == 'False':
                    include_email = True
                    zulip_sender('Теперь в сообщении будет указываться email пользователя')
                    with open("Data/Settings.txt", "r") as f:
                        all = f.read()
                    with open("Data/Settings.txt", "w") as f:
                        all = all.replace("user_email_bool: False", "user_email_bool: True")
                        f.write(all)
                elif start is True and ('/include subject true' in message_from_zulip) \
                        and subject_bool == 'False':
                    include_subject = True
                    zulip_sender('Теперь в сообщении будет указываться тема, из которой получено сообщение')
                    with open("Data/Settings.txt", "r") as f:
                        all = f.read()
                    with open("Data/Settings.txt", "w") as f:
                        all = all.replace("subject_bool: False", "subject_bool: True")
                        f.write(all)
                elif start is True and ('/include display_recipient true' in message_from_zulip) \
                        and display_recipient_bool == 'False':
                    include_display_recipient = True
                    zulip_sender(
                        'Теперь в сообщении будет указываться название канала, из которого получено сообщение')
                    with open("Data/Settings.txt", "r") as f:
                        all = f.read()
                    with open("Data/Settings.txt", "w") as f:
                        all = all.replace("display_recipient_bool: False", "display_recipient_bool: True")
                        f.write(all)
                elif start is True and ('/include email false' in message_from_zulip) \
                        and user_email_bool == 'True':
                    include_email = False
                    zulip_sender('Теперь в сообщении не будет указываться email пользователя')
                    with open("Data/Settings.txt", "r") as f:
                        all = f.read()
                    with open("Data/Settings.txt", "w") as f:
                        all = all.replace("user_email_bool: True", "user_email_bool: False")
                        f.write(all)
                elif start is True and ('/include subject false' in message_from_zulip) \
                        and subject_bool == 'True':
                    include_subject = False
                    zulip_sender('Теперь в сообщении не будет указываться тема, из которой получено сообщение')
                    with open("Data/Settings.txt", "r") as f:
                        all = f.read()
                    with open("Data/Settings.txt", "w") as f:
                        all = all.replace("subject_bool: True", "subject_bool: False")
                        f.write(all)
                elif start is True and ('/include display_recipient false' in message_from_zulip) \
                        and display_recipient_bool == 'True':
                    include_display_recipient = False
                    zulip_sender(
                        'Теперь в сообщении не будет указываться название канала, из которого получено сообщение')
                    with open("Data/Settings.txt", "r") as f:
                        all = f.read()
                    with open("Data/Settings.txt", "w") as f:
                        all = all.replace("display_recipient_bool: True", "display_recipient_bool: False")
                        f.write(all)


            if "VK156324" in data and (old_text_vk == None or not(text in old_text_vk)):
                l = len(data)
                message_from_vk = data[8:l]
                l2 = len(message_from_vk)
                pos = message_from_vk.find("\n")
                old_text_vk = message_from_vk[pos+1:l2]
                if '/start' in message_from_vk and start is False:
                    vk_sender(id_chat, 'Бот успешно запущен')
                    vk_sender(id_chat, "Чтобы узнать весь список команд бота напишите /help")
                    zulip_sender('Бот успешно запущен')
                    zulip_sender("Чтобы узнать весь список команд бота напишите /help")
                    start = True
                elif start is True and ('/stop' in message_from_vk):
                    stop = False
                    vk_sender(id_chat, 'Бот прекратил свою работу')
                    zulip_sender('Бот прекратил свою работу')
                elif start is True and '/' != message_from_vk[0]:
                    zulip_sender(message_from_vk)
                elif start is False:
                    vk_sender(id_chat, 'Бот не запущен. Напишите "/start" в эту беседу')
                elif start is True and ('/help' in message_from_vk):
                    vk_sender(id_chat, help_message)
                elif start is True and ('/include email true' in message_from_vk) \
                        and user_email_bool == 'False':
                    include_email = True
                    vk_sender(id_chat, 'Теперь в сообщении будет указываться email пользователя')
                    with open("Data/Settings.txt", "r") as f:
                        all = f.read()
                    with open("Data/Settings.txt", "w") as f:
                        all = all.replace("user_email_bool: False", "user_email_bool: True")
                        f.write(all)
                elif start is True and ('/include subject true' in message_from_vk) \
                        and subject_bool == 'False':
                    include_subject = True
                    vk_sender(id_chat,
                              'Теперь в сообщении будет указываться тема, из которой получено сообщение')
                    with open("Data/Settings.txt", "r") as f:
                        all = f.read()
                    with open("Data/Settings.txt", "w") as f:
                        all = all.replace("subject_bool: False", "subject_bool: True")
                        f.write(all)
                elif start is True and ('/include display_recipient true' in message_from_vk) \
                        and display_recipient_bool == 'False':
                    include_display_recipient = True
                    vk_sender(id_chat,
                              'Теперь в сообщении будет указываться название канала, из которого получено сообщение')
                    with open("Data/Settings.txt", "r") as f:
                        all = f.read()
                    with open("Data/Settings.txt", "w") as f:
                        all = all.replace("display_recipient_bool: False", "display_recipient_bool: True")
                        f.write(all)
                elif start is True and ('/include email false' in message_from_vk) \
                        and user_email_bool == 'True':
                    include_email = False
                    vk_sender(id_chat, 'Теперь в сообщении не будет указываться email пользователя')
                    with open("Data/Settings.txt", "r") as f:
                        all = f.read()
                    with open("Data/Settings.txt", "w") as f:
                        all = all.replace("user_email_bool: True", "user_email_bool: False")
                        f.write(all)
                elif start is True and ('/include subject false' in message_from_vk) \
                        and subject_bool == 'True':
                    include_subject = False
                    vk_sender(id_chat,
                              'Теперь в сообщении не будет указываться тема, из которой получено сообщение')
                    with open("Data/Settings.txt", "r") as f:
                        all = f.read()
                    with open("Data/Settings.txt", "w") as f:
                        all = all.replace("subject_bool: True", "subject_bool: False")
                        f.write(all)
                elif start is True and ('/include display_recipient false' in message_from_vk) \
                        and display_recipient_bool == 'True':
                    include_display_recipient = False
                    vk_sender(id_chat,
                              'Теперь в сообщении не будет указываться название канала, из которого получено сообщение')
                    with open("Data/Settings.txt", "r") as f:
                        all = f.read()
                    with open("Data/Settings.txt", "w") as f:
                        all = all.replace("display_recipient_bool: True", "display_recipient_bool: False")
                        f.write(all)
