import os

# загрузка всх необходимых для работы программы библиотек
os.system("pip install tk")
os.system("pip install requests")
os.system("pip install vk_api")
os.system("pip install zulip")


import requests
from tkinter import *


def save_file(url, dir):
    """Функция скачивания файлов расширение .py. На вход подается ссылка на скачивание и директория."""
    r = requests.get(url, allow_redirects=True)
    file_name = url.split("/")[-1]
    dir = dir + '/' + file_name
    with open(dir, "wb") as f:
        f.write(r.content)


def make_file(name, text):
    """Функция создания текстовых файлов с информацией, необходимой для работы ботов. На вход подается имя файла и его
     содержимое."""
    dir = os.getcwd() + "/Data/" + name
    with open(dir, "w") as f:
        f.write(text)


def get_token():
    """Функция получения токена группы Вконтакте через поле ввода в окне."""
    global token
    token = entry.get()
    root.destroy()


def get_id_group():
    """Функция получения id группы Вконтакте через поле ввода в окне."""
    global id_group
    id_group = entry.get()
    root.destroy()


def get_way_to_file():
    """Функция получения токена пути к файлу zuliprc через поле ввода в окне."""
    global way_to_file
    way_to_file = entry.get()
    root.destroy()


def enter_data():
    """Функция ввода данных, полученных от пользователя в файл private_inform.txt."""
    global token, id_group, way_to_file
    with open(os.getcwd() + "/Data/private_inform.txt", "r") as f:
        line = f.readline()
        line1 = line[:len(line)-1]
        line = f.readline()
        line2 = line[:len(line)-1]
        line = f.readline()
        line3 = line[:len(line)]
    with open(os.getcwd()+"/Data/private_inform.txt", "w") as f:
        f.write(line1 + token + "\n" + line2 + id_group + "\n" + line3 + way_to_file)


# блок для проверки наличия папки Data, нужный для вывода ошибки о том, что бот уже установлен в этой папке
try:
    os.mkdir('Data')
except FileExistsError:
    root = Tk()
    root.title("WARNING")
    w = root.winfo_screenwidth()
    h = root.winfo_screenheight()
    w = w // 2 - 150
    h = h // 2 - 50
    root.geometry('300x100+{}+{}'.format(w, h))
    Label(text="Вы уже установили бота в эту папку", font=("Times New Roman", 12), width=50, height=3).pack()
    button = Button(text="OK", width=20)

    def button_exit(event):
        root.destroy()
        exit()
    button.bind("<Button-1>", button_exit)
    button.pack()
    root.mainloop()

# ссылки для скачивания файлов .py
link1 = "https://raw.githubusercontent.com/HCK-git/Vk-to-Zulip/main/MainBot.py"
link2 = "https://raw.githubusercontent.com/HCK-git/Vk-to-Zulip/main/VK_getter.py"
link3 = "https://raw.githubusercontent.com/HCK-git/Vk-to-Zulip/main/Zulip_getter.py"
directory = os.getcwd()
token = "None"
id_group = "None"
way_to_file = "None"

save_file(link1, directory)
save_file(link2, directory)
save_file(link3, directory)

# создание текстовых файлов в папке Data
make_file("Settings.txt", "user_email_bool: False\nsubject_bool: False\ndisplay_recipient_bool: False\n"
                          "id_vk_bool: False")
make_file("private_inform.txt", "token: \nid_group: \nway_to_config: ")
make_file("id_chat.txt", " ")

# создание окна для получение токена группы Вконтакте
root = Tk()
root.title("token")
w = root.winfo_screenwidth()
h = root.winfo_screenheight()
w = w // 2 - 150
h = h // 2 - 50
root.geometry('300x100+{}+{}'.format(w, h))
entry = Entry()
entry.pack(pady=10)
Button(text="Ввести", command=get_token).pack()

root.mainloop()

# создание окна для получение id группы Вконтакте
root = Tk()
root.title("id_group")
root.geometry('300x100+{}+{}'.format(w, h))
entry = Entry()
entry.pack(pady=10)
Button(text="Ввести", command=get_id_group).pack()

root.mainloop()

# создание окна для получение пути к файлу zuliprc
root = Tk()
root.title("way_to_file")
root.geometry('300x100+{}+{}'.format(w, h))
entry = Entry()
entry.pack(pady=10)
Button(text="Ввести", command=get_way_to_file).pack()

root.mainloop()

enter_data()
