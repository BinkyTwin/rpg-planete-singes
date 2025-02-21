import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Paramètres de l'animation
fig, ax = plt.subplots()
ax.set_xlim(-1.5, 1.5)
ax.set_ylim(-1.5, 1.5)
ax.set_aspect('equal')
ax.axis('off')

# Création de la boule
ball, = ax.plot([], [], 'bo', markersize=10)

# Fonction d'initialisation
def init():
    ball.set_data([], [])
    return ball,

# Fonction d'animation
def animate(i):
    t = i / 100.0
    x = np.cos(2 * np.pi * t)
    y = np.sin(2 * np.pi * t)
    ball.set_data([x], [y])
    return ball,

# Création de l'animation
ani = animation.FuncAnimation(fig, animate, init_func=init, frames=3000, interval=10, blit=True)

# Affichage de l'animation
plt.show()
