
# template
#from PIL import Image, ImageTk
import tkinter as tk
import winsound
import time
import threading
import numpy as np
import random

ikkuna=tk.Tk()
ikkuna.title("Exercise 5 apina island continent")
ikkuna.geometry("700x700")

koristetta=tk.Label(ikkuna,text="").grid(row=0,column=0)
point_button=[]

for i in range(5):
    button_temp=tk.Button(ikkuna,text="Points: "+str(i+1),padx=40)
    button_temp.grid(row=0,column=i+1)
    point_button.append(button_temp)
def i_suppose_i_have_earned_so_much_points(amount_of_points):
    for i in range(5):
        point_button[i].configure(bg='gray')
    time.sleep(1)    
    for i in range(amount_of_points):
        point_button[i].configure(bg='green')
        winsound.Beep(440+i*100,500)

hatasanat="Ernesti ja Kernesti tässä terve! Olemme autiolla saarella, ja voisitteko tulla sieltä sivistyksestä joku hakemaan meidät pois! Kiitos!"
hata_sanat=hatasanat.split()
perilla_sanat = []

saari=tk.Button(ikkuna,text="Saari",width=10,height=30,bg='yellow')
saari.place(x=50,y=100)

def update_apina_ui(apina, apina_x, apina_y):
    apina.place(x=apina_x, y=apina_y)

def apina_uimaan(y_taso, unique_sana):
    apina=tk.Label(ikkuna,text='🐵')
    apinan_aani=np.random.randint(300,3000)

    i_suppose_i_have_earned_so_much_points(1)

    liikuttu = 0

    for i in range(175):
        print('....APINA...UI.....'+unique_sana+'....')
        apina_x=160+(i*2.5)
        apina_y=y_taso + np.random.randint(-10,10)
        ikkuna.after(10*i, update_apina_ui, apina, apina_x, apina_y)

        liikuttu+=2.5
        if liikuttu >= 100:
            mahdollisuus = random.randint(1,100)
            if mahdollisuus <= 7:
                print(unique_sana+" Apina got eaten!!!")
                winsound.Beep(1000,1111)
                i_suppose_i_have_earned_so_much_points(3)
                return
            winsound.Beep(1000,500)
            liikuttu = 0
        
        winsound.Beep(apinan_aani,100)
        time.sleep(0.0001)
    if apina_x >= 585:
        print(unique_sana+" pääsi perille")
        winsound.Beep(1500,1000)
        perilla_sanat.append(unique_sana)
        print(perilla_sanat)
        if len(perilla_sanat) > 10:
            print("yli 10 sanaa viestistä perillä")
        i_suppose_i_have_earned_so_much_points(2)

def saie_apinalle_lahetys(y_taso):
    unique_sana = hata_sanat.pop(0)

    t=threading.Thread(target=apina_uimaan, args=(y_taso, unique_sana))
    t.start()

def monta_apinaa_ui():
    for i in range(10):
        saie_apinalle_lahetys(120)

e_laituri=tk.Button(ikkuna, text='=====', command=lambda: saie_apinalle_lahetys(120))
e_laituri.place(x=120,y=120)

e2_laituri=tk.Button(ikkuna, text='monta', command=lambda: monta_apinaa_ui())
e2_laituri.place(x=80,y=120)

k_laituri=tk.Button(ikkuna, text='=====', command=lambda: saie_apinalle_lahetys(500))
k_laituri.place(x=120,y=500)

mantere=tk.Button(ikkuna,text="mantere",width=10,height=30,bg='green')
mantere.place(x=600,y=100)

#########################

ikkuna.mainloop()