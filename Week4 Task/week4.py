# Tehdään tkinteriä ja säikeistystä ...
 
print("...")
 
import tkinter as tk
import time
import winsound
import threading
import numpy as np
import psutil
 
ikkuna=tk.Tk()
ikkuna.title("Käyttöliittymä, jossa on säikeistystoiminnallisuutta...")
ikkuna.geometry("650x300")
 
koriste={}
for i in range(10):
    koriste[i]=tk.Label(ikkuna,text="")
    koriste[i].grid(row=i,column=i)
 
ernestin_muuttuja_naytolla=tk.StringVar()
ernestin_muuttuja_naytolla.set("---------")
 
kernestin_muuttuja_naytolla=tk.StringVar()
kernestin_muuttuja_naytolla.set("---------")
 
cpu_muuttuja_naytolle=tk.StringVar()
 
# diipa daipaa koodinpätkää...
 
def ernesti_heita_tomaatti():
    for i in range(8):
        print("o-",i)
        temp=np.random.randint(0,100)
        ernestin_muuttuja_naytolla.set(f"{temp}+{temp*'-'}->")
        # lisataan jokin raskas suoritusasia...
        A=np.ones((1000,1000))
        B=np.matmul(A,A)
        # ...raskas osio loppuu
        time.sleep(0.1)
        winsound.Beep(489,100)
    print("...heit...heit...")
    print(slider.get())
    winsound.Beep(300,500)
 
# tehdään funktio, joka luo tomaatinheittosäikeen Ernestiä varten ja myös ajaa sen...
def luo_ja_aja_saie_tomaatinheittoa_varten_ernestille():
    #luonti
    t=threading.Thread(target=ernesti_heita_tomaatti)
    #käynnistys
    t.start()
 
ernesti_painike=tk.Button(ikkuna,text="Ernesti",command=luo_ja_aja_saie_tomaatinheittoa_varten_ernestille)
ernesti_painike.grid(row=1,column=1)
 
ernesti_teksti=tk.Label(ikkuna,textvariable=ernestin_muuttuja_naytolla,bg='green',width=80,anchor='w',fg='red')
ernesti_teksti.grid(row=1,column=2)
 
# ***************************************************
# ***************************************************
 
def kernesti_heita_tomaatti():
    for i in range(8):
        print("o-",i)
        temp=np.random.randint(0,100)
        kernestin_muuttuja_naytolla.set(f"{temp}+{temp*'-'}->")
        time.sleep(0.1)
        winsound.Beep(689,100)
    print("...heit...heit...")
    winsound.Beep(200,500)
 
# tehdään funktio, joka luo tomaatinheittosäikeen Kernestiä varten ja myös ajaa sen...
def luo_ja_aja_saie_tomaatinheittoa_varten_kernestille():
    #luonti
    t=threading.Thread(target=kernesti_heita_tomaatti)
    #käynnistys
    t.start()
 
kernesti_painike=tk.Button(ikkuna,text="Kernesti",command=luo_ja_aja_saie_tomaatinheittoa_varten_kernestille)
kernesti_painike.grid(row=3,column=1)
 
kernesti_teksti=tk.Label(ikkuna,textvariable=kernestin_muuttuja_naytolla,bg='green',width=80,anchor='w')
kernesti_teksti.grid(row=3,column=2)
 
#Muuta...
def monitor_cpu_load():
    #global cpu_muuttuja_naytolle
    while True:
        #cpu_muuttuja=psutil.cpu_percent()
        pid=psutil.Process().pid
        cpu_muuttuja=psutil.Process(pid).num_threads()
        maara_skaalattu=cpu_muuttuja/1
        cpu_muuttuja_naytolle.set(f"{cpu_muuttuja} {int(maara_skaalattu)*'#'}")
        time.sleep(0.1)
 
t_cpu=threading.Thread(target=monitor_cpu_load)
t_cpu.start()
 
cpu_tekstiotsikko=tk.Label(ikkuna,text="Threads:")
cpu_tekstiotsikko.grid(row=10,column=1)
cpu_tekstijuttu=tk.Label(ikkuna,textvariable=cpu_muuttuja_naytolle,width=80,bg='red',anchor='w')
cpu_tekstijuttu.grid(row=10,column=2)
 
slider = tk.Scale(ikkuna, from_=0, to=100, orient=tk.HORIZONTAL)
slider.grid(row=11, column=2)
 
ikkuna.mainloop()