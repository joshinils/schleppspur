#!/usr/bin/env python3

import pygame
import pygame.draw
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
    max_fps: int = 2400

    def drawLine(self: 'pge', a: Tuple[float, float], b: Tuple[float, float], color: Tuple[int, int, int] = (0, 0, 0)):
        pygame.draw.line(self.screen, color, a, b)

    def __init__(self: 'pge'):
        pygame.font.init()
        #font = pygame.font.SysFont(None, 48)
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

    def drawCircle(self : 'pge', center: Tuple[int, int], radius: int, color: Tuple[int, int, int] = (255, 255, 255)) -> None:
        pygame.draw.circle(self.screen, color, center, radius)

    def drawString(self : 'pge', pos: Tuple[int, int], text: str, color: Tuple[int, int, int] = (255, 255, 255)) -> None:
        try:
            text=str(text)
            font = pygame.font.SysFont(None, 24)
            img = font.render(text, True, color)
            self.screen.blit(img, pos)
        except Exception as e:
            print('Font Error, saw it coming')
            self.drawCircle(pos, 3, color)
            raise e

    def drawPolygon(self: 'pge', points: List[Tuple[int, int]], color: Tuple[int, int, int] = (255, 255, 255)) -> None:
        pygame.draw.polygon(self.screen, color, points)


class nodePair:
    draggerPos: Tuple[float, float]
    stonePos: Tuple[float, float]
    time: float
    deleteWeight: float = None

    def __init__(self: 'nodePair', draggerPos: Tuple[float, float], stonePos: Tuple[float, float], time: float):
        self.draggerPos = draggerPos
        self.stonePos = stonePos
        self.time = time
        pass

    def __repr__(self: 'nodePair') -> str:
        return ("nodePair(dragger:" + str(self.draggerPos) + ", stonePos:" + str(self.stonePos) + " delW:" + str(self.deleteWeight) + ")")

class game(pge):
    track: List[nodePair] = []
    lastPos = np.array([0, 0])
    timeAcc: float = 0

    def OnUserCreate(self: 'game'):
        # print("game::OnUserCreate")
        self.t = time.time() # time seconds since 1970

    def OnUserUpdate(self: 'game', delta_t: float) -> bool:
        # print("game::OnUserUpdate")

        self.timeAcc += delta_t

        self.fps = 1/delta_t
        self.screen.fill((delta_t, self.fps % 255, 255))


        mousePos = pygame.mouse.get_pos()
        #print(mousePos)

        self.drawCircle(self.lastPos, 6, (200, 0, 0))
        self.drawCircle(mousePos, 8, (250, 250, 250))
        # pygame.draw.circle(self.screen, (200, 0, 0), self.lastPos, 6)
        # pygame.draw.circle(self.screen, (250, 250, 250), mousePos, 8)

        dir = self.lastPos - mousePos
        norm = np.linalg.norm(dir)

        if norm != 0:
            dir = dir / norm

        #self.drawLine(mousePos, self.lastPos)
        self.lastPos = self.lastPos - dir * (norm -200)

        self.track.append(nodePair(self.lastPos, mousePos, self.timeAcc))
        self.drawTrack()

        title = "fps: " + str(int(self.fps*100)/100).ljust(6) + " delta_t: " + str(delta_t)
        pygame.display.set_caption(title.ljust(1000))
        return True

    def pruneTrack(self: 'game') -> None:
        maxLen = 300
        print(len(self.track), self.fps)

        to_remove = 0

        if len(self.track) > maxLen :
            to_remove += 1
        if self.fps < 120:
            to_remove += 2

        for i in range(to_remove):
            # search closest to remove
            prev = None
            next = None
            curr = None

            minWeight = 1080*1920
            deleteIdx = None

            for i in range(len(self.track)):
                prev = curr
                curr = next
                next = self.track[i]

                #print(prev, curr, next)
                if prev == None:
                    continue

                curr.deleteWeight = ( - np.linalg.norm(prev.draggerPos - next.draggerPos)
                                      + np.linalg.norm(prev.draggerPos - curr.draggerPos)
                                      + np.linalg.norm(next.draggerPos - curr.draggerPos))
                curr.deleteWeight *= i * i
                # print(np.linalg.norm(prev.draggerPos - next.draggerPos),
                #       np.linalg.norm(prev.draggerPos - curr.draggerPos),
                #       np.linalg.norm(next.draggerPos - curr.draggerPos),
                #       " deleteweight ",
                #       curr.deleteWeight)
                if minWeight > curr.deleteWeight:
                    minWeight = curr.deleteWeight
                    deleteIdx = i-1
                # print("minW:", minWeight, "delIdX:", deleteIdx)

            # for p in self.track:
            #     print(p.deleteWeight)
            #
            # print("del:", self.track[deleteIdx])
            del self.track[deleteIdx]

    def drawTrack(self: 'game') -> None:
        last_p = None
        for p in self.track:
            random.seed(p.deleteWeight)
            col = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            self.drawLine(p.stonePos, p.draggerPos, col)
            if last_p != None:
                self.drawLine(last_p.draggerPos, p.draggerPos)
                #self.drawString((p.draggerPos + p.stonePos)*.5, p.deleteWeight, col)
                self.drawLine(last_p.stonePos, p.stonePos)

                self.drawPolygon([last_p.stonePos,
                                  last_p.draggerPos,
                                  p.draggerPos,
                                  p.stonePos],
                                 col)
                self.drawCircle(p.draggerPos, 2, col)
                self.drawCircle(p.stonePos, 2, col)
            last_p = p

        self.pruneTrack()

def main():

    g = game()
    if g.Construct(1920, 1080):
        g.Start()

if __name__ == "__main__":
    main()