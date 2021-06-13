#!/usr/bin/env python3

import pygame
import time
from typing import *
import random
import numpy as np

from pygame import mouse

class pge:
    screen: 'pygame.Surface'
    time_of_last_frame: float
    ScreenWidth: int
    ScreenHeight: int
    max_fps: int = 240

    def drawLine(self: 'pge', a: Tuple[float, float], b: Tuple[float, float], color: Tuple[int, int, int] = (0, 0, 0)):
        pygame.draw.line(self.screen, color, a, b)

    def __init__(self: 'pge'):
        pass

    def Construct(self: 'pge', width: int = 300, height: int = 200) -> bool:
        try:
            self.ScreenWidth, self.ScreenHeight = width, height
            self.screen = pygame.display.set_mode((self.ScreenWidth, self.ScreenHeight))
        except:
            return False
        return True

    def Start(self: 'pge'):
        self.OnUserCreate()
        self.delta_t=1

        is_running = True
        while is_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_running = False
                    break

            now = time.time()
            self.delta_t = now - self.t
            if self.max_fps > 0 and self.delta_t < 1/self.max_fps:
                # print(self.delta_t)
                # print(1/self.max_fps-self.delta_t)

                time.sleep(1/self.max_fps - self.delta_t)
                now = time.time()
                self.delta_t = now - self.t

            self.OnUserUpdate(self.delta_t)

            self.t = now
            pygame.display.flip()


    def OnUserCreate(self: 'pge'):
        # print("pge::OnUserCreate")
        pass

    def OnUserUpdate(self: 'pge', delta_t: float) -> bool:
        # print("pge::OnUserUpdate")
        return True

class game(pge):
    def OnUserCreate(self: 'game'):
        # print("game::OnUserCreate")
        self.t = time.time() # time seconds since 1970

    lastPos = np.array([0, 0])

    def OnUserUpdate(self: 'game', delta_t: float) -> bool:
        # print("game::OnUserUpdate")

        fps = 1/delta_t
        self.screen.fill((delta_t, fps % 255, 255))


        mousePos = pygame.mouse.get_pos()
        print(mousePos)

        pygame.draw.circle(self.screen, (200, 0, 0), self.lastPos, 6)
        pygame.draw.circle(self.screen, (250, 250, 250), mousePos, 8)

        dir = self.lastPos - mousePos
        norm = np.linalg.norm(dir)

        if norm != 0:
            dir = dir / norm

        #self.drawLine(mousePos, self.lastPos)
        self.lastPos = self.lastPos - dir * (norm -200)

        self.drawLine(mousePos, self.lastPos)

        title = "fps: " + str(int(fps*100)/100).ljust(6) + " delta_t: " + str(delta_t)
        pygame.display.set_caption(title.ljust(1000))
        return True

def main():

    g=game()
    if g.Construct(1920, 1080):
        g.Start()

if __name__ == "__main__":
    main()