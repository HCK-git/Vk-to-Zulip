from tkinter import *
import os
import requests


def save_file(url, dir):
    r = requests.get(url, allow_redirects=True)
    file_name = url.split("/")[-1]
    dir = dir + '/' + file_name
    with open(dir, "wb") as f:
        f.write(r.content)


def make_file(name, text):
    dir = os.getcwd() + "/Data/" + name
    with open(dir, "w") as f:
        f.write(text)


def get_token():
    global token
    token = entry.get()
    root.destroy()


def get_id_group():
    global id_group
    id_group = entry.get()
    root.destroy()


def get_way_to_file():
    global way_to_file
    way_to_file = entry.get()
    root.destroy()


def enter_data():
    global token, id_group, way_to_file
    print(token)
    print(id_group)
    print(way_to_file)
    print(type(token))
    with open(os.getcwd() + "/Data/privat_inform.txt", "r") as f:
        line = f.readline()
        line1 = line[:len(line)-1]
        line = f.readline()
        line2 = line[:len(line)-1]
        line = f.readline()
        line3 = line[:len(line)]
    with open(os.getcwd()+"/Data/privat_inform.txt", "w") as f:
        f.write(line1 + token + "\n" + line2 + id_group + "\n" + line3 + way_to_file)

        
os.system("pip install tk")
os.system("pip install requests")
os.system("pip install vk_api")
os.system("pip install zulip")

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
os.mkdir('Data')
make_file("Settings.txt", "user_email_bool: False\nsubject_bool: False\ndisplay_recipient_bool: False")
make_file("privat_inform.txt", "token: \nid_group: \nway_to_config: ")
make_file("id_chat.txt", " ")

root = Tk()
root.title("token")
w = root.winfo_screenwidth()
h = root.winfo_screenheight()
w = w // 2 - 200
h = h // 2 - 200
root.geometry('400x400+{}+{}'.format(w, h))
entry = Entry()
entry.pack(pady=10)
Button(text="Ввести", command=get_token).pack()

root.mainloop()


root = Tk()
root.title("id_group")
w = root.winfo_screenwidth()
h = root.winfo_screenheight()
w = w // 2 - 200
h = h // 2 - 200
root.geometry('400x400+{}+{}'.format(w, h))
entry = Entry()
entry.pack(pady=10)
Button(text="Ввести", command=get_id_group).pack()

root.mainloop()


root = Tk()
root.title("way_to_file")
w = root.winfo_screenwidth()
h = root.winfo_screenheight()
w = w // 2 - 200
h = h // 2 - 200
root.geometry('400x400+{}+{}'.format(w, h))
entry = Entry()
entry.pack(pady=10)
Button(text="Ввести", command=get_way_to_file).pack()

root.mainloop()

enter_data()
