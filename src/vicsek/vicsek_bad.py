import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import click


class VicsekModel:

    def __init__(self, d=0.01, v=0.01, dt=1, eta=0.1):
        self.counter = 0
        self.d = d
        self.v = v
        self.dt = dt
        self.eta = eta

    def init_model(self, count):
        """
        Initialize the Vicsek model particle system and corresponding quiver plot.

        Parameters
        ----------
        count : int
            Number of particles in the simulation.

        Attributes
        ----------
        n : int
            Number of particles.

        r : numpy.ndarray of shape (n, 2)
            Random initial positions of particles in the unit square [0, 1] × [0, 1].

        theta : numpy.ndarray of shape (n,)
            Random initial orientations of particles in normalized angular space [0, 1].

        x : numpy.ndarray of shape (n,)
            x-coordinates of particle positions.

        y : numpy.ndarray of shape (n,)
            y-coordinates of particle positions.

        u : numpy.ndarray of shape (n,)
            x-components of velocity vectors computed as cos(2πθ).

        vv : numpy.ndarray of shape (n,)
            y-components of velocity vectors computed as sin(2πθ).

        fig : matplotlib.figure.Figure
            Matplotlib figure object used for visualization.

        ax : matplotlib.axes.Axes
            Matplotlib axes object for plotting.

        q : matplotlib.quiver.Quiver
            Quiver plot object representing particle velocities as arrows.
        """
        self.n = count

        self.r = np.random.random((self.n, 2))
        self.theta = np.random.random(self.n)

        self.fig, self.ax = plt.subplots(figsize=(6, 6))

        self.x = self.r[:, 0]
        self.y = self.r[:, 1]
        self.u = np.cos(2 * np.pi * self.theta)
        self.vv = np.sin(2 * np.pi * self.theta)

        self.q = self.ax.quiver(self.x, self.y, self.u, self.vv, angles='xy')
        self.ax.set_xlim(0, 1)
        self.ax.set_ylim(0, 1)
        self.ax.set_title("Vicsek Model")

    @staticmethod
    def distance(p1, p2):
        return np.sqrt(((p1 - p2) ** 2).sum())

    def update_model(self):
        for i in range(self.n):
            sum_sin = 0
            sum_cos = 0
            neighbours = 0

            for j in range(self.n):
                if i != j:
                    if VicsekModel.distance(self.r[i], self.r[j]) < self.d:
                        theta_j = 2 * np.pi * self.theta[j]
                        sum_sin = sum_sin + np.sin(theta_j)
                        sum_cos = sum_cos + np.cos(theta_j)
                        neighbours = neighbours + 1

            if neighbours > 0:
                avg_theta = np.arctan2(sum_sin / neighbours, sum_cos / neighbours)
                self.theta[i] = (avg_theta / (2 * np.pi)) + self.eta * (np.random.rand() - 0.5)

            dx = self.v * self.dt * np.cos(2 * np.pi * self.theta[i])
            dy = self.v * self.dt * np.sin(2 * np.pi * self.theta[i])

            self.r[i, 0] = self.r[i, 0] + dx
            self.r[i, 1] = self.r[i, 1] + dy

            if self.r[i, 0] > 1:
                self.r[i, 0] = 0
            if self.r[i, 1] > 1:
                self.r[i, 1] = 0
            if self.r[i, 0] < 0:
                self.r[i, 0] = 1
            if self.r[i, 1] < 0:
                self.r[i, 1] = 1

            self.counter += 1

    def animate(self, frame):

        self.update_model()

        self.x = []
        self.y = []
        self.u = []
        self.vv = []

        for i in range(self.n):
            self.x.append(self.r[i, 0])
            self.y.append(self.r[i, 1])
            self.u.append(np.cos(2 * np.pi * self.theta[i]))
            self.vv.append(np.sin(2 * np.pi * self.theta[i]))

        self.q.set_offsets(np.c_[self.x, self.y])
        self.q.set_UVC(self.u, self.vv)

        print("frame", frame, "counter", self.counter)

        return self.q,

@click.command()
@click.option('-c', "--count", default=200, help='Number')
def main(count):
    vicsek_model = VicsekModel()
    vicsek_model.init_model(count)
    ani = FuncAnimation(vicsek_model.fig, vicsek_model.animate, frames=200, interval=50, blit=True)
    plt.show()

if __name__ == "__main__":
    main()
