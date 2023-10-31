import tkinter as tk
import random

# Create tkinter window
window = tk.Tk()
window.title("Tomato Throwing Game")

# Create target image on the right side (standard position)
target_image = tk.PhotoImage(file='target.png')  # Replace with the actual image filename
target_label = tk.Label(window, image=target_image)
target_label.place(x=500, y=200)

# Function to reposition Kernesti's image randomly
def reposition_kernesti():
    x = random.randint(50, 300)
    y = random.randint(50, 300)
    kernesti_label.place(x=x, y=y)

# Function to reposition Ernesti's image randomly
def reposition_ernesti():
    x = random.randint(700, 950)
    y = random.randint(50, 300)
    ernesti_label.place(x=x, y=y)

# Create Kernesti's image on the left side randomly
kernesti_image = tk.PhotoImage(file='kernesti.png')  # Replace with the actual image filename
kernesti_label = tk.Label(window, image=kernesti_image)
reposition_kernesti()  # Initial random positioning
kernesti_label.pack()

# Create a button to reposition Kernesti's image
reposition_kernesti_button = tk.Button(window, text="Reposition Kernesti", command=reposition_kernesti)
reposition_kernesti_button.pack()

# Create a button to reposition Ernesti's image
ernesti_image = tk.PhotoImage(file='ernesti.png')  # Replace with the actual image filename
ernesti_label = tk.Label(window, image=ernesti_image)
reposition_ernesti()  # Initial random positioning
ernesti_label.pack()

# Create a button to reposition Ernesti's image
reposition_ernesti_button = tk.Button(window, text="Reposition Ernesti", command=reposition_ernesti)
reposition_ernesti_button.pack()

def throw_tomato_kernesti():
    x = 0
    y = kernesti_label.winfo_y() + kernesti_image.height() // 2
    throw_tomato(x, y)

def throw_tomato(x, y):
    tomato = tk.Label(window, text="🍅", font=("Arial", 12))
    tomato.place(x=x, y=y)
    animate_tomato(tomato)

def animate_tomato(tomato):
    x, y = tomato.winfo_x(), tomato.winfo_y()
    if x < 500:
        tomato.place(x=x + 10, y=y+5)
        window.after(20, lambda: animate_tomato(tomato))
    else:
        tomato.destroy()

throw_tomato_kernesti_button = tk.Button(window, text="Throw Tomato (Kernesti)", command=throw_tomato_kernesti)
throw_tomato_kernesti_button.pack()


# Start the tkinter main loop
window.mainloop()