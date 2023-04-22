import asyncio
import time

import keyboard
import telebot

builted = False

# настройка :
# bind f2 "exec scc"

# не менять
class SourceConsoleControl :
    def __init__(self) :
        if builted:
            with open("tg") as f:
                self.bot = telebot.TeleBot(f.read())
        self.bot = telebot.TeleBot("ТГ_БОТ_КЛЮЧ")
        self.menu = False
        self.pressed_menu = False  # зажатая клавиша (не менять)
        self.portal_path = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\Portal 2\\portal2"  # путь до игры

    def is_locked(self,command: str) -> int :
        if len(command) < 3 :
            return 2
        print(command)
        if command.split()[0] in "map".split(",") :
            return 1
        if command.split()[-1] in "".split(",") :
            return 1
        if command.lower() in "kill,crash,quit,exit,editor_toggle,fadeout,fadein".split(",") :
            return 1
        if command.find("test") :
            return
        return 0

    def exec_command(self,command: str) :
        try :
            with open(self.portal_path.replace("\\","/") + "/cfg/scc.cfg",'w') as f :
                f.write(command)
        except PermissionError :
            print("команда не записана")
        print(command)
        keyboard.press('f2')
        time.sleep(0.1)
        keyboard.release('f2')

    def main(self,command: str) :  # функция обраборки чата
        print(f"команда ({command}) введена")
        if self.menu :
            return
        if self.is_locked(command) :
            print(self.is_locked(command))
            if self.is_locked(command)==1 :
                print(f"команда ({command}) заблокирована")
            return
        self.exec_command(command)


scc = SourceConsoleControl()


@scc.bot.message_handler(commands = ['help','start'])
def send_welcome(message) :
    scc.bot.reply_to(message,"бот включен")


@scc.bot.message_handler(func = lambda message : True)
def message(message) :
    scc.main(message.text)


def menu_logger(x) :
    if not scc.pressed_menu :
        scc.menu = not scc.menu
        if scc.menu :
            print("меню открыто")
        else :
            print("меню закрыто")
        scc.pressed_menu = True


def menu_logger1(x) :
    scc.pressed_menu = False


if __name__=='__main__' :
    keyboard.on_press_key("esc",menu_logger)
    keyboard.on_release_key("esc",menu_logger1)
    asyncio.run(scc.bot.polling())
