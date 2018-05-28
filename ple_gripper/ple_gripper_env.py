from ple.games import base
from pygame.constants import K_a, K_d, K_w, K_s, K_q, K_e


class Catcher(base.PyGameWrapper):

        def __init__(self, width=200, height=200):

                actions = {
                        "left": K_a,
                        "right": K_d,
                        "up": K_w,
                        "down": K_s,
                        "clockwise": K_e,
                        "counter_clockwise": K_q
                }

                base.PyGameWrapper.__init__(self, width, height, actions=actions)

                # game specific
                self.lives = 0

        def init(self):
            self.score = 0

            # game specific

        def getScore(self):
            return self.score

        def game_over(self):
            return self.lives == 0

        def step(self, dt):
            # move players
            # check hits
            # adjust scores
            # remove lives
