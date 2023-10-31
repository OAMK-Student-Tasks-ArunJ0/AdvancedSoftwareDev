import numpy as np
import random
import matplotlib.pyplot as plt

Jungle = np.zeros((100, 100))

Ernesti = {
    "name": "Ernesti",
    "location_x": random.randint(0, 99),
    "location_y": random.randint(0, 99),
}

Kernesti = {
    "name": "Kernesti",
    "location_x": random.randint(0, 99),
    "location_y": random.randint(0, 99),
}

while Kernesti["location_x"] == Ernesti["location_x"] and Kernesti["location_y"] == Ernesti["location_y"]:
    Kernesti["location_x"] = random.randint(0, 99)
    Kernesti["location_y"] = random.randint(0, 99)

Jungle[Ernesti["location_x"], Ernesti["location_y"]] = 1
Jungle[Kernesti["location_x"], Kernesti["location_y"]] = 2

plt.imshow(Jungle, cmap='viridis', origin='lower')
plt.title("Jungle with Ernesti and Kernesti")
plt.show()

# En päässyt kovin pitkälle sain plotterin tehtyä ja sen junglen mutta en kovin tiedä miten se liikkuminen tulisi