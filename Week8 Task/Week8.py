import numpy as np
import tkinter as tk
import winsound
import time
import random
import math
import threading
import pygame
import os
from collections import defaultdict

pygame.mixer.init()

# kertoo koodille Apinojen sijainnit
current_dir = os.path.dirname(os.path.abspath(__file__))
monkey_wav = os.path.join(current_dir, "monkey.wav")
shark_wav = os.path.join(current_dir, "shark.wav")
dive_wav = os.path.join(current_dir, "dive.wav")
yahoo_wav = os.path.join(current_dir, "yahoo.wav")
monkeysound = pygame.mixer.Sound(monkey_wav)
sharksound = pygame.mixer.Sound(shark_wav)
divesound = pygame.mixer.Sound(dive_wav)
yahoosound = pygame.mixer.Sound(yahoo_wav)

# Meri simulaattori jossa on saaria josta lähtee apinoita kulkemaan kohti eri suuntia
class SeaSimulator:
    def __init__(self):
        self.ikkuna = tk.Tk()
        self.ikkuna.title("Exercise 8")
        self.ikkuna.geometry("800x800")
        self.ikkuna.configure(bg='blue')
        self.island_positions = []
        self.apinoja_saarilla = defaultdict(int)
        self.island_numbers = {}
        self.laituri_positions = []
        self.ResetSignal = threading.Event()
        self.monkey_threads = []
        self.random_swimmer_threads = []
        self.s1_island_coordinates = None
        self.arrived_islands = []

        self.create_widgets()
        self.update_islands_thread = threading.Thread(target=self.update_islands)
        self.update_islands_thread.start()

# rakentaa vasemman alanurkan napit
    def create_widgets(self):
        self.create_point_buttons()
        new_island_button = tk.Button(self.ikkuna, text="NEW ISLAND", command=self.create_new_island)
        new_island_button.place(x=10, y=750)
        reset_sea_button = tk.Button(self.ikkuna, text="RESET SEA", command=self.reset_sea)
        reset_sea_button.place(x=120, y=750)
        send_apina_button = tk.Button(self.ikkuna, text="Send Apina from S1", command=self.send_apina_from_s1)
        send_apina_button.place(x=220, y=750)

# lähettää apinan S1 saarelta nappi
    def send_apina_from_s1(self):
        coordinates = SeaSimulator.s1_island_coordinates
        if coordinates!= None:
            monkey_num = self.apinoja_saarilla.get(coordinates, 0)
            if monkey_num >= 1:
                self.send_apina_from_island("east", coordinates)

# rakentaa piste napit
    def create_point_buttons(self):
        self.point_buttons = []
        for i in range(5):
            button_temp = tk.Button(self.ikkuna, text="Points: " + str(5 * i), padx=40, bg="green")
            button_temp.grid(row=0, column=i + 1)
            button_temp.bind("<Button-1>", self.change_button_color)
            self.point_buttons.append(button_temp)

# vaihtaa napin väriä
    def change_button_color(self, event):
        button = event.widget
        button_color = button.cget("background")
        if button_color=="grey":
            button.config(bg="green")
        else:
            button.config(bg="grey")

# rakentaa uuden saaren merelle
    def create_new_island(self):
        if len(self.island_positions) < 10:
            new_position = self.generate_unique_island_position()
            self.add_island(new_position)
            self.apinoja_saarilla[new_position] = 10

            self.schedule_monkey_sounds(new_position)

            if len(self.island_positions) == 1:
                self.create_laiturit(new_position)
                self.schedule_random_apinas(new_position)
                SeaSimulator.s1_island_coordinates = new_position
        else:
            print("Too many islands, can't create more without crashing...")

# laskee hyvän paikan saarelle
    def generate_unique_island_position(self):
        while True:
            x = random.randint(50, 650)
            y = random.randint(50, 600)
            new_position = (x, y)
            overlap = any(self.calculate_distance(new_position, pos) < 170 for pos in self.island_positions)
            if not overlap:
                return new_position

# lisää saaren asemalleen
    def add_island(self, new_position):
        island_count = len(self.island_positions) + 1
        self.island_numbers[new_position] = island_count
        island_button = tk.Button(self.ikkuna, text="S{} \nApes 10".format(island_count), padx=40, pady=40, bg="yellow")
        island_button.place(x=new_position[0], y=new_position[1])
        self.island_positions.append(new_position)

# rakentaa laiturit saarelle
    def create_laiturit(self, island_position):
        x = island_position[0] - 20
        y = island_position[1] + 45
        self.create_laituri_button(x, y, "W")
        x = island_position[0] + 115
        y = island_position[1] + 45
        self.create_laituri_button(x, y, "E")
        x = island_position[0] + 50
        y = island_position[1] - 25
        self.create_laituri_button(x, y, "N")
        x = island_position[0] + 50
        y = island_position[1] + 110
        self.create_laituri_button(x, y, "S")

# rakentaa laiturin kohdassa
    def create_laituri_button(self, x, y, direction):
        button = tk.Button(self.ikkuna, text="===") if direction in {"W", "E"} else tk.Button(self.ikkuna, text="||", padx=5, pady=5)
        self.laituri_positions.append((x, y))
        button.place(x=x, y=y)

# aloittaa random apina uimisen
    def schedule_random_apinas(self, island_position):
        random_swimmer_thread = threading.Thread(target=self.random_apina_from_island, args=(island_position,))
        random_swimmer_thread.start()
        self.monkey_threads.append(random_swimmer_thread)

# random apinojen uinti threadi
    def random_apina_from_island(self, island_position):
        while True:
            for i in range(10):
                if self.ResetSignal.is_set():
                    break
                time.sleep(1)
            if self.ResetSignal.is_set():
                break
            monkey_num = self.apinoja_saarilla.get(island_position, 0)
            if monkey_num >= 1:
                print("Apina went swimming")
                directions = ["west", "east", "north", "south"]
                direction = random.choice(directions)
                divesound.play()
                self.send_apina_from_island(direction, island_position)

# lähettää apinan saarelta uimaan yhtä suuntaa kohti
    def send_apina_from_island(self, direction, island_position):
        directions = {
            "west": (-20, 45),
            "east": (115, 45),
            "north": (50, -25),
            "south": (50, 110)
        }
        if direction in directions:
            x, y = island_position
            dx, dy = directions[direction]
            x = x+dx
            y = y+dy
            apina = tk.Label(self.ikkuna, text='🐵')
            self.apinoja_saarilla[island_position] -= 1
            for i in range(1500):
                if(direction=="west"):
                    apina_x = x - (i * 2.5)
                    apina_y = y + random.randint(-5, 5)
                if(direction=="east"):
                    apina_x = x + (i * 2.5)
                    apina_y = y + random.randint(-5, 5)
                if(direction=="north"):
                    apina_x = x + random.randint(-5, 5)
                    apina_y = y - (i * 2.5)
                if(direction=="south"):
                    apina_x = x + random.randint(-5, 5)
                    apina_y = y + (i * 2.5)
                self.ikkuna.after(10 * i, self.update_apina_ui, apina, apina_x, apina_y)
                chance = random.randint(1, 100)
                if chance <= 1:
                    island_number = self.island_numbers.get(island_position, 0)
                    print("Monkey from S{} died to a shark".format(island_number))
                    self.ikkuna.after(10 * i, self.remove_apina_ui, apina)
                    sharksound.play()
                    break
                if self.ResetSignal.is_set():
                    self.ikkuna.after(10 * i, self.remove_apina_ui, apina)
                    break
                for other_position in self.island_positions:
                    if other_position != island_position:
                        if apina_x >= (other_position[0]-10) and apina_x<=(other_position[0]+115):
                            if apina_y >= (other_position[1]-10) and apina_y<=(other_position[1]+115):
                                yahoosound.play()
                                self.ikkuna.after(10 * i, self.remove_apina_ui, apina)
                                time.sleep(1)
                                self.apinas_arrived_on_island(other_position)
                                return
        else:
            print("Invalid direction")

# kun apinat pääsee perille saarelle ja kertoo turismista
    def apinas_arrived_on_island(self, position_of_island):
        print("Monkey reached an island at S{}".format(self.island_numbers.get(position_of_island, 0)))
        self.apinoja_saarilla[position_of_island] += 1
        if position_of_island in self.arrived_islands:
            return
        else:
            print("Monkeys at the island S{} discovered tourism!!!".format(self.island_numbers.get(position_of_island, 0)))
            self.create_laiturit(position_of_island)
            self.schedule_random_apinas(position_of_island)
            self.arrived_islands.append(position_of_island)

# poistaa apinan kun se kuolee tai pääsee perille
    def remove_apina_ui(self, apina):
        apina.place_forget()

# päivittää apinojen uidessa niiden kohtaa
    def update_apina_ui(self, apina, apina_x, apina_y):
        apina.place(x=apina_x, y=apina_y)

# laskee kuinka kaukana saaret ovat ettei ne mene toisten päälle
    def calculate_distance(self, point1, point2):
        x1, y1 = point1
        x2, y2 = point2
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

# aloittaa apina ääni threadin
    def schedule_monkey_sounds(self, island_position):
        monkey_thread = threading.Thread(target=self.apina_sound_thread, args=(island_position,))
        monkey_thread.start()
        self.monkey_threads.append(monkey_thread)

# ilmoittaa apinojen elämästä saarella kun ne siellä on
    def apina_sound_thread(self, island_pos):
        while True:
            monkey_num = self.apinoja_saarilla.get(island_pos, 0)
            for i in range(monkey_num):
                soundfreq = random.randint(200, 1000)
                winsound.Beep(soundfreq, 100)
                chance = random.randint(1, 100)
                if chance <= 1:
                    print("Monkey on S{} died of laughter".format(self.island_numbers.get(island_pos, 0)))
                    monkeysound.play()
                    self.apinoja_saarilla[island_pos] -= 1
            for i in range(10):
                if self.ResetSignal.is_set():
                    break
                time.sleep(1)
            if self.ResetSignal.is_set():
                break

# saarien tietojen päivittäjä
    def update_islands(self):
        while not self.ResetSignal.is_set():
            for island_position in self.island_positions:
                apinas = self.apinoja_saarilla.get(island_position, 0)
                island_number = self.island_numbers.get(island_position, 0)
                for widget in self.ikkuna.winfo_children():
                    if isinstance(widget, tk.Button) and widget.winfo_exists():
                        x, y = island_position
                        if widget.winfo_x() == x and widget.winfo_y() == y:
                            widget.config(text="S{} \nApes {}".format(island_number, apinas))
            time.sleep(1)

# Reset napin toiminnot
    def reset_sea(self):
        self.ResetSignal.set()
        for laituri_position in self.laituri_positions:
            self.destroy_buttons_at_position(laituri_position)
        self.laituri_positions = []

        for island_position in self.island_positions:
            self.destroy_buttons_at_position(island_position)
        self.island_positions = []

        for thread in self.monkey_threads:
            thread.join()
        self.monkey_threads = []

        for thread in self.random_swimmer_threads:
            thread.join()
        self.random_swimmer_threads = []

        if self.update_islands_thread.is_alive():
            self.update_islands_thread.join()

        self.ResetSignal.clear()
        if not self.update_islands_thread.is_alive():
            self.update_islands_thread = threading.Thread(target=self.update_islands)
            self.update_islands_thread.start()

# tuhoaa saaret resetissä
    def destroy_buttons_at_position(self, position):
        x, y = position
        for widget in self.ikkuna.winfo_children():
            if isinstance(widget, tk.Button) and widget.winfo_x() == x and widget.winfo_y() == y:
                widget.destroy()

    def run(self):
        self.ikkuna.mainloop()

if __name__ == "__main__":
    sea_simulator = SeaSimulator()
    sea_simulator.run()