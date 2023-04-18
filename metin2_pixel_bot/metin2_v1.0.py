from tkinter import *
import time
from pynput import keyboard
bindkey = keyboard
import keyboard
import pyautogui
from PIL import Image
from python_imagesearch import imagesearch
import random
import win32gui





#Global Elements
mod_state = False
finded_state = False
finded_time = 0
direction_character = False
afk_state = False
walk_state = False
window_title = "" #Write window name
window = win32gui.FindWindow(None, window_title)


list_metin = ["metins/mtn_1.png","metins/mtn_2.png","metins/mtn_3.png"]

list_afk_control = {
    1:{
        "name": "code_imgs/tamam.png",
        "x":45,
        "y":13,
    },
    2:{
        "name": "code_imgs/nick.png",
        "x":45,
        "y":13,
    },
    3:{
        "name": "code_imgs/baglan.png",
        "x":45,
        "y":13,
    },
    4:{
        "name": "code_imgs/basla.png",
        "x":50,
        "y":13,
    },
    5:{
        "name": "code_imgs/dog.png",
        "x":45,
        "y":10,
    },
    6:{
        "name": "code_imgs/bot.png",
        "x":100,
        "y":0,
    },
}



# Start mod
def start_mod():
    global mod_state
    mod_state = True
    mod_control()


def mod_control(): #text search loop only when mod state is true
    while mod_state:
        search_metin()
        if keyboard.is_pressed('F1'):
            break


def search_metin():
    state_metin = False
    metin = []
    for text in list_metin:
        metin =  imagesearch.imagesearch(text)
        if metin[0] != -1:
            state_metin = True
            break
    if state_metin:
        print("metin buldum")
        find_metin(metin)
    else:
        walk_character()
        rotate_camera()
        login()





def walk_character(): #not find metin, move character
    if walk_state:
        number = random.randint(1,10)
        keyboard.press("W")
        time.sleep(number*0.1)  
        keyboard.release("W")



def rotate_camera(): # not find metin, rotate camera
    keyboard.press("q")
    time.sleep(0.1)  
    keyboard.release("q")


def search_metin_health(w,h):
    target =  imagesearch.imagesearch("code_imgs/mtnhlth.png")
    if target != -1:
        if target[0] <= w*0.25  or target[0] >= w-w*0.25 or target[1] >= h-h*0.65:
            return False
        else:
            return True
    else:
        return False

def control_metin_state(w,h):
    target =  imagesearch.imagesearch("code_imgs/mtng.png")
    if target != -1:
        if target[0] <= w*0.1  or target[0] >= w-w*0.25 or target[1] >= h-h*0.65:
            return False
        else:
            return True
    else:
        return False



def login_action():
    img = []
    for index in list_afk_control:
        path = list_afk_control[index]["name"]
        x = list_afk_control[index]["x"]
        y = list_afk_control[index]["y"]
        img = imagesearch.imagesearch(path)
        if img[0] != -1:
            pyautogui.moveTo(img[0]+x, img[1]+y)
            pyautogui.click(img[0]+x, img[1]+y)   




def login():#afk control exited from char, script logged in char
    time.sleep(0.2)
    if afk_state:
        login_action()
    return False




def find_metin(metin): #finded metinqq
    global finded_time 
    finded_time = time.time()
    global window 
    leftx, topy, rightx, bottomy = win32gui.GetWindowRect(window)
    width = rightx - leftx
    height = bottomy - topy
    pyautogui.moveTo(metin[0]+(width*0.015), metin[1]+(height*0.052)+((metin[1]*0.04)))
    pyautogui.click(metin[0]+(width*0.015), metin[1]+(width*0.052)+((metin[1]*0.04)))
    global finded_state 
    finded_state = True
    time.sleep(0.15)
    state_metin_name = control_metin_state(width,height)
    if state_metin_name:
        while finded_state: 
            state_metin_name = control_metin_state(width,height)
            if type(finded_time) != "float":
                elapsed_time  = time.time()-finded_time
                if elapsed_time > 30: 
                        pyautogui.moveTo((width*0.5)+leftx, (height*0.5)+topy)
                        pyautogui.click(width*0.5, height*0.5)
                elif elapsed_time > 6: 
                    state = search_metin_health(width,height)
                    if state:
                        finded_time = False
                        finded_state = False
                        keyboard.press('q')
                        time.sleep(0.2)  
                        keyboard.release('q')
                        time.sleep(0.2)  
                        walk_character()
                        rotate_camera()
                        break

            if not state_metin_name:
                finded_state = False
                break





def walk_mode(): #on off walk_mode
    global walk_state 
    walk_state = not walk_state


def afk_mode(): #on off walk_mode
    global afk_state 
    afk_state = not afk_state



#Gui Key pannel

main_window = Tk()
main_window.title("Meta Scripts Game Bot")
main_window.configure(background="#232323")
main_window.geometry("240x300")
photo = PhotoImage(file = "metalogo.png")
main_window.iconphoto(False, photo)
delay = 10

delay_label = Label(main_window,font=("Helvetica", 12), fg="white", bg="#232323", text="Kesme Suresi Girip Kaydete Bas:")
delay_label.place(x=1, y=95, anchor="w")

delay_entry = Entry(main_window)
delay_entry.insert(0, str(delay))
delay_entry.place(x=50, y=125, anchor="w")

save_button = Button(main_window, text="KAYDET",font=("Helvetica", 14), activebackground="green", fg="white", bg="#4c4c4c",command=login)
save_button.place(x=65, y=160, anchor="w")

start_button = Button(main_window, text="Baslat", font=("Helvetica", 17), fg="white", bg="#4c4c4c", activebackground="#005b0f",command=start_mod)
start_button.place(x=20, y=30, anchor="w")

stop_button = Button(main_window, text="Durdur", font=("Helvetica", 17), fg="white", bg="#4c4c4c", activebackground="#bc0909",command=search_metin_health)
stop_button.place(x=140, y=30, anchor="w")

start_label = Label(main_window,fg="#005b0f",bg="#232323",foreground="orange",font=("Helvetica", 10), text="")
start_label.place(x=72, y=70, anchor="w")

stop_label = Label(main_window,fg="#bc0909",bg="#232323",foreground="orange",font=("Helvetica", 10), text="")
stop_label.place(x=70, y=70, anchor="w")

# gmkontrol

gmkontrol_check = Checkbutton(main_window, text="!GM KONTROL!",fg="white", bg="#4c4c4c", foreground="orange" )
gmkontrol_check.pack()
gmkontrol_check.place(x=1, y=205, anchor="w")

# yenidendirilme

afk_check = Checkbutton(main_window, text="Afk Mode",fg="white", bg="#4c4c4c", foreground="yellow",command = afk_mode)
afk_check.pack()
afk_check.place(x=1, y=225, anchor="w")



delay_spinbox = Entry(main_window, width=0, fg="white", bg="#4c4c4c")
delay_spinbox.pack()
delay_spinbox.place(x=0, y=280, anchor="w")

delay_scale = Scale(main_window, from_=1, to=500, length=232, width=15,bg="#232323",fg="white",troughcolor="#4c4c4c", orient='horizontal')
delay_scale.pack()
delay_scale.place(x=1, y=280, anchor="w")


#walk 

oto_skill_check = Checkbutton(main_window, text="Yürüme", fg="white", bg="#4c4c4c", foreground="red",command=walk_mode)
oto_skill_check.pack()
oto_skill_check.place(x=1, y=245, anchor="w")



main_window.mainloop()
