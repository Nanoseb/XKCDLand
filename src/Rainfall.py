import collections
import numpy as np
import numpy.random

Raindrop = collections.namedtuple('Raindrop', 'x y tail alpha')

class Rainfall(object):
    def __init__(self, max_x, max_y):
        self.max_x = max_x
        self.max_y = max_y

        self.falling_drops = 230

        self.fall_x = numpy.random.random(size=self.falling_drops) * self.max_x
        self.fall_y = -numpy.random.random(size=self.falling_drops) * self.max_y
        self.fall_velocities = numpy.random.normal(
            loc=self.max_y * 2,
            scale=self.max_y / 3,
            size=self.falling_drops,
        )
        self.fall_alphas = numpy.random.beta(4, 30, size=self.falling_drops)

        self.splashes = []

        self.current_time = 0.0

    def drops(self):
        for n in range(self.falling_drops):
            yield Raindrop(
                x=self.fall_x[n],
                y=self.fall_y[n],
                tail=self.max_y // 13,
                alpha=self.fall_alphas[n],
            )

        for (splash_x, splash_y, splash_time) in self.splashes:
            yield Raindrop(
                x=splash_x,
                y=splash_y,
                tail=self.max_y // 6,
                alpha=min(
                    1.0 * np.exp(-4.0 * (self.current_time - splash_time)),
                    1.0,
                ),
            )

    def update(self, dt):
        self.fall_y += self.fall_velocities * dt

        reset_mask = self.fall_y - self.max_y // 5 > self.max_y

        self.fall_y[reset_mask] = self.fall_y[reset_mask] - (1.3 * self.max_y)
        self.fall_x[reset_mask] = (
            numpy.random.random(size=self.falling_drops) * self.max_x
        )[reset_mask]

        for _ in range(numpy.random.poisson(1.4 * dt)):
            self.splashes.append((
                numpy.random.random() * self.max_x,
                numpy.random.random() * self.max_y,
                self.current_time,
            ))

        # Clear up old splashes
        self.splashes = [
            (x, y, time)
            for x, y, time in self.splashes
            if time > (self.current_time - 10.0)
        ]

        self.current_time += dt
