import numpy as np
import tkinter as tk
import winsound
import time
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading

ikkuna=tk.Tk()
ikkuna.title("Exercise 6 Deserted Island")
ikkuna.geometry("1000x800")

# add five buttons to the top line of the window
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


colors = [(1, 1, 0), (0, 0, 1)]  # Yellow to Blue
cmap = LinearSegmentedColormap.from_list("YellowToBlue", colors, N=256)

num_rows = 100
num_columns = 100

# Aloituspiste hahmoille

saari = np.zeros((num_rows, num_columns))


pool_x1, pool_y1, pool_x2, pool_y2 = 60, 20, 80, 80

oja_e_x1, oja_e_y1, oja_e_x2, oja_e_y2 = 0, 30, 60, 31

oja_k_x1, oja_k_y1, oja_k_x2, oja_k_y2 = 0, 70, 60, 71

saari[pool_x1:pool_x2, pool_y1:pool_y2] = 0.2
saari[oja_e_x1:oja_e_x2, oja_e_y1:oja_e_y2] = 0.1
saari[oja_k_x1:oja_k_x2, oja_k_y1:oja_k_y2] = 0.1



fig, ax = plt.subplots()
fig.set_facecolor("blue")

cax = ax.matshow(saari, cmap=cmap, vmin=0, vmax=1)
ax.axis("off")

saari_kanvaasi=FigureCanvasTkAgg(fig,master=ikkuna)
saari_kanvaasi.get_tk_widget().place(x=100,y=120)

saari_kanvaasi.draw()

## SAIETYS
i_suppose_i_have_earned_so_much_points(1)

def update_apina_ui(apina, apina_x, apina_y):
    apina.place(x=apina_x, y=apina_y)

def apina_kaivaa_e():
    apina=tk.Label(ikkuna,text='🐵')
    apinan_aani=np.random.randint(300,3000)
    apina_dig_time=1
    apina_x=290
    apina_y=220
    for k in range(61):
        ikkuna.after(10*k, update_apina_ui, apina, apina_x, apina_y)
        if apina_y!=400:
            apina_y=220+k*3
        if apina_x!=338:
            apina_x=290+k
        winsound.Beep(apinan_aani,100)
    for i in range(61):
        apina_y=400-i*4
        apina_x=338
        ikkuna.after(10*i, update_apina_ui, apina, apina_x, apina_y)
        winsound.Beep(apinan_aani,100)
        if saari[oja_e_x2 - i, oja_e_y1]!=1:
            saari[oja_e_x2-i,oja_e_y1]=1
            cax.set_data(saari)
            saari_kanvaasi.draw()
            time.sleep(apina_dig_time)
            apina_dig_time=apina_dig_time*2
        if apina_y==160:
            break
    i_suppose_i_have_earned_so_much_points(2)
    apina.destroy()


def saie_apinalle_lahetys_e():
    t=threading.Thread(target=apina_kaivaa_e)
    t.start()


e_forest=tk.Button(ikkuna, text='E Forest',bg="green", command=lambda: saie_apinalle_lahetys_e())
e_forest.place(x=260,y=200)


ikkuna.mainloop()

