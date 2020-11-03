#!/usr/bin/env python3

import pathlib
import curses
from model import *

BORDER_SYMBOL = ["═", "║", "╔", "╗", "╚", "╝", "*", 'x' '-']
BORDERS = ['═', '║', '╔', '╗', '╚', '╝', 'x' '-']

class PacmanGameEngine:
    """The class handles game flow
    """
    def __init__(self):
        pass

    @staticmethod
    def __set_up(level_number):
        """Function to generate required object
        
        Arguments:
            level_number {int} -- level of the game
        
        Raises:
            TypeError: raise if level_number is not an integer
            ValueError: raise if level_number is not a positive integer
        
        Returns:
            object -- a set of generated object
        """
        #validate input
        if not isinstance(level_number, int):
            raise TypeError("\'level_number\' must be an integer")
        if level_number < 0:
            raise ValueError("\'level_number\' must be an positive integer")
        
        #setting up objects
        window = curses.initscr()
        level = Level.load(level_number)
        
        #setting up cursor
        curses.curs_set(0)
        window.nodelay(1)
        curses.cbreak(1)
        window.keypad(1)

        return window, level, Scene(window, level)

    @staticmethod
    def _tear_down(window):
        """Functino to clean up the terminal
        
        Arguments:
            window {object} -- window object generated from curses library
        
        Raises:
            TypeError: raise if window is not an object
        """     
        if not isinstance(window, object):
            raise TypeError("\'window\' must be a window object")

        #restore normal terminal
        window.clear()
        window.refresh()

    @staticmethod
    def __run(window, level, scene):
        """Function to handle game loop
        
        Arguments:
            window {object} -- window object of curses library
            level {Level} -- a Level instance
            scene {Scene} -- a Scene instance
        
        Raises:
            TypeError: raise if window is not an object
            TypeError: raise if Level is not an Level instance
            TypeError: raise if Scene it not an Scene instance
        """
        #validate input
        if not isinstance(window, object):
            raise TypeError("\'window\' must be an object")
        if not isinstance(level, Level):
            raise TypeError("\'level\' must be a Level object")
        if not isinstance(scene, Scene):
            raise TypeError("\'scene\' must be a Scene object")

        #initialize object
        pacman = level.pacman
        pmap = level.pmap
        ghosts = level.ghosts
        bonuses = level.bonuses 
        point = 0 # point gains by player
        std_x = pacman.x #default pacman x ordinate
        std_y = pacman.y #default pacman y ordinate
        main_loop = 0 # count number of main loop gone
        last_loop = 0 # store last point that an event trigger
        eaten_ghost = 0 #number of ghosts pacman has eaten after eating powercapsule
        up = False # pacman move up direction
        down = False # pacman move down direction
        left = False # pacman move left direction
        right = False # pacman move right direction

        #display standing start anouncement
        loop = 0 #loop counter
        scene.standing_start_announcement = True
        
        while True:
            #display the scene
            scene.render()

            #loop controller
            if loop == 5:
                scene.standing_start_announcement = False
                break

            loop += 1 # standing start announcement loop counter

        #game loop
        while True:
            
            #loop counter 
            main_loop += 1
            
            #implement the player direction
            button = 0
            button = window.getch()
            
            #implement quit button
            if button == ord('q'):
                break
            
            #implement move button
            if button == ord('w') or button == curses.KEY_UP:
                try:
                    if pacman.y - 1 < 0:
                        raise Exception
                    if pmap.grid[pacman.y-1][pacman.x] in BORDERS:
                        raise Exception
                except:
                    pass
                else:
                    up = True
                    down = False
                    left = False
                    right = False

            if button == ord('s') or button == curses.KEY_DOWN:
                try:
                    if pmap.grid[pacman.y+1][pacman.x] in BORDERS:
                        raise Exception
                except:
                    pass
                else:
                    up = False
                    down = True
                    left = False
                    right = False

            if button == ord('d') or button == curses.KEY_RIGHT:
                try:
                    if pmap.grid[pacman.y][pacman.x+1] in BORDERS:
                        raise Exception
                except:
                    pass
                else:
                    up = False
                    down = False
                    left = True
                    right = False

            if button == ord('a') or button == curses.KEY_LEFT:
                try:
                    if pacman.x - 1 < 0:
                        raise Exception
                    if pmap.grid[pacman.y][pacman.x-1] in BORDERS:
                        raise Exception
                except:
                    pass
                else:
                    up = False
                    down = False
                    left = False
                    right = True

            #auto move
            if up == True:
                pacman.set_direction(-1, 0)
            if down == True:
                pacman.set_direction(1, 0)
            if left == True:
                pacman.set_direction(0, 1)
            if right == True:
                pacman.set_direction(0, -1)

            #stop if hit wall
            if up == True and pmap.grid[pacman.y-1][pacman.x] in BORDERS:
                up = False
            if down == True and pmap.grid[pacman.y+1][pacman.x] in BORDERS:
                down = False
            if left == True and pmap.grid[pacman.y][pacman.x+1] in BORDERS:
                left = False
            if right == True and pmap.grid[pacman.y][pacman.x-1] in BORDERS:
                right = False
            
            #implement point gains
            #gain 10 points per dot
            if pmap.grid[pacman.y][pacman.x] == '·':
                pmap.grid[pacman.y][pacman.x] = ' '
                point += 10

            #gain 20 points per power capsule
            if pmap.grid[pacman.y][pacman.x] == '•':
                pmap.grid[pacman.y][pacman.x] = ' '
                point += 20
                scene.power_capsule = True

            # pacman eats bonus event
            if pacman.x == bonuses.x and pacman.y == bonuses.y:
                point += bonuses.points
                bonuses.points = 0

            #update points
            scene.points = point

            #check if game is end
            present_capsule = False
            for y in range(pmap.height):
                for x in range(pmap.width):
                    if pmap.grid[y][x] == '·': #if there are some dot
                        present_capsule = True
                    if pmap.grid[y][x] == '•': #if there are some power capsule
                        present_capsule = True

            if not present_capsule and bonuses.points == 0: #end game if no points left
                break
            
            #implememt pacman ate power capsule event
            if not scene.power_capsule: # if not eat power capsule yet
                #pacman death
                if pacman.x == ghosts[0].x and pacman.y == ghosts[0].y:
                    scene.death = True
                if pacman.x == ghosts[1].x and pacman.y == ghosts[1].y:
                    scene.death = True
                if pacman.x == ghosts[2].x and pacman.y == ghosts[2].y:
                    scene.death = True
                if pacman.x == ghosts[3].x and pacman.y == ghosts[3].y:
                    scene.death = True

            else: #if eat power capsule
                #pacman eats ghosts
                if pacman.x == ghosts[0].x and pacman.y == ghosts[0].y and not scene.blinky_ate:
                    eaten_ghost += 1 
                    scene.blinky_ate = True 

                if pacman.x == ghosts[1].x and pacman.y == ghosts[1].y and not scene.pinky_ate:
                    eaten_ghost += 1 
                    scene.pinky_ate = True   

                if pacman.x == ghosts[2].x and pacman.y == ghosts[2].y and not scene.inky_ate:
                    eaten_ghost += 1
                    scene.inky_ate = True 

                if pacman.x == ghosts[3].x and pacman.y == ghosts[3].y and not scene.clyde_ate:
                    eaten_ghost += 1
                    scene.clyde_ate = True


                #gain points
                if eaten_ghost > 0:
                    #if ate ghost, gain points
                    scene.points += eaten_ghost*200 

                    #if eaten all ghosts 
                    if eaten_ghost == 4:
                        eaten_ghost = 0
                        last_loop = main_loop
                        scene.power_capsule = False
                        scene.flash = False
                        scene.blinky_ate = False
                        scene.pinky_ate = False
                        scene.inky_ate = False
                        scene.clyde_ate = False

            #break death scene
            if scene.death == True:
                loop = 0 #loop counter
                while True:

                    scene.render()
                    loop += 1 # loop counter
                    
                    # if 20 loops have gone, break
                    if loop == 20:
                        break
                
                #return pacman to standard position
                scene.death = False
                scene.life -= 1 # lost 1 life
                pacman._x = std_x # back to default position
                pacman._y = std_y # back to default position

            #if drain out of life, end game
            if scene.life == 0:
                break

            #play ##############################
            pacman.play(scene)

            
            #start AI ############################

            #handle pacman eat power capsule event
            if scene.power_capsule:
                if last_loop == 0:
                    last_loop = main_loop
                
                # change to ghosts flashing scene
                if main_loop - last_loop > 40:
                    scene.flash = True
                    last_loop = 0

            #ghosts flashing scene
            if scene.power_capsule and scene.flash:
                if last_loop == 0:
                    last_loop = main_loop

                #stop pacman ate capsule event
                if main_loop - last_loop > 7:
                    last_loop = 0
                    #reset event status
                    scene.power_capsule = False
                    scene.flash = False
                    scene.blinky_ate = False
                    scene.pinky_ate = False
                    scene.inky_ate = False
                    scene.clyde_ate = False

            #implement ghosts are eaten envent
            if main_loop > 5:
                ghosts[0].play(scene, level)
                ghosts[1].play(scene, level)
                ghosts[2].play(scene, level)
                ghosts[3].play(scene, level)
            
            else:# start ghost
                #ghost move out the cage
                if main_loop == 1:
                    ghosts[0].set_direction(0, -1)
                    ghosts[1].set_direction(0, 1)
                    ghosts[2].set_direction(0, 1)
                    ghosts[3].set_direction(0, -1)
                if main_loop == 2:
                    ghosts[0].set_direction(-1, 0)
                    ghosts[1].set_direction(-1, 0)
                    ghosts[2].set_direction(-1, 0)
                    ghosts[3].set_direction(-1, 0)
                if main_loop == 3:
                    ghosts[0].set_direction(-1, 0)
                    ghosts[1].set_direction(-1, 0)
                    ghosts[2].set_direction(-1, 0)
                    ghosts[3].set_direction(-1, 0)
                if main_loop == 4:
                    ghosts[0].set_direction(-1, 0)
                    ghosts[1].set_direction(-1, 0)
                    ghosts[2].set_direction(0, -1)
                    ghosts[3].set_direction(0, 1)
                if main_loop == 5:
                    ghosts[0].set_direction(0, 1)
                    ghosts[1].set_direction(0, -1)
                    ghosts[2].set_direction(0, -1)
                    ghosts[3].set_direction(0, 1)

            #clean up scene
            curses.napms(200)
            window.clear()
            window.refresh()

    def start(self, level_number):
        """Function to beginning the game
        
        Arguments:
            level_number {int} -- level of the game
        """
        #setting up curses library
        window, level, scene = self.__set_up(level_number)

        #start the game
        self.__run(window, level, scene)

        #end game
        self._tear_down(window)


def main():
    game = PacmanGameEngine()
    game.start(1)

if __name__ == '__main__':
    main()
