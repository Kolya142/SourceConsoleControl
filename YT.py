import asyncio
import os
import sys
import time

# pip install pytchat
import pytchat
import keyboard

# настройка :
# bind f2 "exec scc"

# не менять
class SourceConsoleControl :
    def __init__(self) :
        self.chat = pytchat.create(video_id="oezd4d-ApMk")
        self.menu = False
        self.autostart = (True, "portal2.exe", "-dev +developer 2") # запускать при старте
        self.ok = "esc"
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


def menu_logger(x) :
    if not scc.pressed_menu :
        scc.menu = not scc.menu
        if scc.menu :
            print("меню открыто")
        else :
            print("меню закрыто")
        scc.pressed_menu = True
        scc.ok = "esc"

def menu_logger0(x) :
    if not scc.pressed_menu :
        if not scc.ok == "esc":
            scc.menu = not scc.menu
            if scc.menu :
                print("меню открыто")
            else :
                print("меню закрыто")
            scc.pressed_menu = True
        scc.ok = '~'


def menu_logger1(x) :
    scc.pressed_menu = False



if __name__=='__main__' :
    if scc.autostart[0]:
        gt = '"' + '/'.join(scc.portal_path.replace("\\", "/").split('/')[:-1]) + '/' + scc.autostart[1] + '"' + ' ' + scc.autostart[2]
        print(gt)
        sss = ""
        if os.name != "nt":
            sss = "c.sh"
        else:
            sss = "c.bat"
        with open(sss, 'w') as f:
            f.write(gt)
        if os.name != "nt":
            os.system("xterm -e c.sh &")
        else:
            os.system("start c.bat")
    keyboard.on_press_key("esc",menu_logger)
    keyboard.on_release_key("esc",menu_logger1)
    keyboard.on_press_key("`",menu_logger0)
    keyboard.on_release_key("`",menu_logger1)
    while True:
        while scc.chat.is_alive() :
            for c in scc.chat.get().sync_items() :
                scc.main(c.message)