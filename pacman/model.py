#!/usr/bin/env python3

import json
import pathlib
import curses
import math
import random
from map_utils import *

PACMAN = "pacman"
BLINKY = "blinky"
PINKY = "pinky"
INKY = "inky"
CLYDE = "clyde"
SYMBOL = "symbol"
CHERRY = "cherry"
POINTS = "points"
EYES = '👀'
STANDING_START_ANNOUNCEMENT = "standing_start_announcement"
COLOR_RGB_PACMAN = (255, 255, 0)
COLOR_RGB_BLINKY = (255, 0, 0)
COLOR_RGB_PINKY = (255, 184, 255)
COLOR_RGB_INKY = (0, 255, 255)
COLOR_RGB_CLYDE = (255, 184, 82)
COLOR_RGB_ORANGE = (128, 64, 0)
COLOR_RGB_WHITE = (255, 255, 255)
COLOR_RGB_BLUE = (0, 0, 128)
COLOR_RGB_BRIGHT_BLUE = (24, 24, 255)
BORDER_SYMBOL = ['═', '║', '╔', '╗', '╚', '╝']
NOT_WALKABLE = ['═', '║', '╔', '╗', '╚', '╝', '-', 'x']
PACMAN_SYMBOL = "ᗧ"
READY = "READY!"
EXPLODING = '💥'
SKULL = '💀'
X = "x"
Y = "y"


class Object:
    """Base class of pacman game class hierachy
    
    Arguments:
        x - x ordinate of the object on the map
        y - y ordinate of the object on the map
        symbol - symbol represents the object on the map
        color - color of the symbol

    Attributes:
        _x - x ordinate of the object on the map
        _y - y ordinate of the object on the map
        __symbol - symbol represents the object on the map
        __color - color of the symbol
    """

    def __init__(self, x, y, symbol, color):
        #validate input
        if not isinstance(x, int):
            raise TypeError("\'x\' must be an integer.")
        if not isinstance(y, int):
            raise TypeError("\'y\' must be an integer.")
        if x <= 0:
            raise ValueError("\'x\' must be an positive integer.")
        if y <= 0:
            raise ValueError("\'y\' must be an positive integer.")
        if not isinstance(color, tuple):
            raise TypeError("\'color\' must be a tuple.")
        if len(color) != 3:
            raise AssertionError("\'color\' must be a tuple of three elements.")
        if not all([isinstance(i, int) for i in color]):
            raise TypeError("\'color\' must be a tuple of three integers.")
        if not all([i <= 0 or i >= 255 for i in color]):
            raise ValueError("\'color\' must be a tuple of the integers between 0 and 255.")
        if not isinstance(symbol, str):
            raise TypeError("\'symbol\' must be a symbol character.")
        if len(symbol) != 1:
            raise ValueError("\'symbol\' must be a single symbol character.")

        self._x = x
        self._y = y
        self.__symbol = symbol
        self.__color = color

    @property
    def x(self):
        return self._x
    
    @property
    def y(self):
        return self._y

    @property
    def symbol(self):
        return self.__symbol

    @property
    def color(self):
        return self.__color

class AnimatedCharacter(Object):

    def __init__(self, x, y, symbol, color):
        super().__init__(x, y, symbol, color)

    def set_direction(self, dy, dx):
        """Function set new direction for the object
        
        Arguments:
            dx {int} -- the amount of step x ordinate move
            dy {int} -- the amount of step y ordinate move
        
        Raises:
            TypeError: raise if 'dx' is not an integer
            TypeError: raise if 'dy' is not an integer
            ValueError: raise if 'dx' and 'dy' is not an integer between -1 and 1
        """
        #validate input
        if not isinstance(dx, int):
            raise TypeError("\'dx\' must be an integer")
        if not isinstance(dy, int):
            raise TypeError("\'dy\' must be an integer")
        if dx < -1 or dx > 1 or dy < -1 or dy > 1:
            raise ValueError("\'dx\' and \'dy\' must be an integer between -1 and 1")
        
        #set direction
        if dx == -1:
            if self._y == 14 and self._x == 1:
                self._x = 27
            else:
                self._x -= 1
        if dx == 1:
            if self._y == 14 and self._x == 26:
                self._x = 0
            else:
                self._x += 1
        if dy == -1:
            self._y -= 1
        if dy == 1:
            self._y += 1

    def play(self, scene):
        """Function that control the direction of Pacman
        
        Arguments:
            scene {Scene} -- Scene object that render the graphic
            pmap {Map} -- a Map object that store current level map
        
        Raises:
            TypeError: raise if 'scene' is not a Scene object
        """
        #validate input
        if not isinstance(scene, Scene):
            raise TypeError("\'scene\' must be an Scene object")
        
        #display the graphic
        scene.render()

class Pacman(AnimatedCharacter):
    def __init__(self, x, y, symbol, color):
        super().__init__(x, y, symbol, color)

class Bonus(Object):

    def __init__(self, x, y, symbol, points):
        super().__init__(x, y, symbol, (0, 0, 0))
        #validate points argument
        if not isinstance(points, int):
            raise TypeError("\'points\' must be an integer.")
        if points%100 != 0:
            raise ValueError("\'points\' must be an integer which is multiple of 100")
        self.points = points

class Ghost(AnimatedCharacter):
    
    def __init__(self, x, y, color):
        super().__init__(x, y, 'ᗣ', color)
        self.last_y = 0
        self.last_x = 0

    def play(self, scene, level):
        """Ghosts move randomly
        """
        #validate input
        if not isinstance(scene, Scene):
            raise TypeError("\'scene\' must be a Scene object")
        if not isinstance(level, Level):
            raise TypeError("\'level\' must be a Level object")
        
        #loop counter
        loop = 0

        while True:

            #loop counter
            loop += 1

            #radom direction
            direction_y = random.randint(-1, 1)
            if direction_y == 0:
                direction_x = random.randrange(-5, 5, 2)
                if direction_x < 0:
                    direction_x = -1
                else:
                    direction_x = 1
            else:
                if direction_y < 0:
                    direction_y = -1
                else:
                    direction_y = 1
                direction_x = 0
            
            #check if direction is different from last pos and other ghosts
            if (self._x + direction_x != self.last_x or self._y + direction_y != self.last_y) and \
                (self._x + direction_x != level.ghosts[0].x or self._y + direction_y != level.ghosts[0].y) and \
                (self._x + direction_x != level.ghosts[1].x or self._y + direction_y != level.ghosts[1].y) and \
                (self._x + direction_x != level.ghosts[2].x or self._y + direction_y != level.ghosts[2].y) and \
                (self._x + direction_x != level.ghosts[3].x or self._y + direction_y != level.ghosts[3].y):               
                #try the new position
                try:
                    if self._y+direction_y < 0:
                        raise Exception
                    if self._x+direction_x < 0:
                        raise Exception
                    level.pmap.grid[self._y+direction_y][self._x+direction_x]
                except:
                    pass
                else:
                    #check if new direction hit wall or not 
                    if level.pmap.grid[self._y+direction_y][self._x+direction_x] not in NOT_WALKABLE:
                        self.last_y = self._y
                        self.last_x = self._x
                        self._x += direction_x
                        self._y += direction_y
                        break
                        
            #prevent infinite loop
            if loop == 10:
                self._x = self.last_x
                self._y = self.last_y
                break

        scene.render()
    
class Blinky(Ghost):
    def __init__(self, x, y):
        super().__init__(x, y, (0, 0, 0))

class Pinky(Ghost):
    def __init__(self, x, y):
        super().__init__(x, y, (0, 0, 0))

class Inky(Ghost):
    def __init__(self, x, y):
        super().__init__(x, y, (0, 0, 0))

class Clyde(Ghost):
    def __init__(self, x, y):
        super().__init__(x, y, (0, 0, 0))

class StandingStartAnnouncement:
    def __init__(self, x, y):
        if not isinstance(x, int):
            raise TypeError("\'x\' must be an integer.")
        if not isinstance(y, int):
            raise TypeError("\'y\' must be an integer.")
        if x < 0:
            raise ValueError("\'x\' must be an positive integer.")
        if y < 0:
            raise ValueError("\'y\' must be an positive integer.")

        self.x = x
        self.y = y

class Map:
    """class Map of pacman game map
    
    Arguments:
        data - argument that take data of pacman map

    Attributes:
        __data - store a pacman map
        __height - height of the pacman map grid
        __width - width of the pacman map grid
        __grid - pacman map grid
    """

    def __init__(self, data):
        self.__data = data
        self.__height = len(data)

        #compute map width
        width = 0
        for line in data:
            if width == 0:
                width = len(line)
            if width < len(line):
                width = len(line)
        self.__width = width

        #generate grid
        grid = []
        for x in range(len(data)):
            grid_line = []
            for y in range(width):
                try:
                    data[x][y]
                except:
                    grid_line.append(" ")
                else:
                    grid_line.append(data[x][y])
            grid.append(grid_line)
        self.__grid = grid
        self.__cell_graph = []
        self.__node_graph = []

    @property
    def height(self):
        return self.__height
    
    @property
    def width(self):
        return self.__width

    @property
    def grid(self):
        return self.__grid
    
    @staticmethod
    def load_map(file_pathname):
        return Map(prettify_map(uncompress_map_with_rle(load_map(file_pathname))))

    def build_graph(self, x, y):
        """Return a list of walkable Cells
        
        Arguments:
            x {int} -- x ordinate of the first Cell
            y {[type]} -- y ordinate of the first Cell
        
        Raises:
            TypeError: raise if x is not an integer
            TypeError: raise if y is not an integer
            ValueError: raise if x or y is not a positive integer
        
        Returns:
            list -- list of walkable
        """
        #validate input 
        if not isinstance(x, int):
            raise TypeError("\'x\' must be an integer")
        if not isinstance(y, int):
            raise TypeError("\'y\' must be an integer")
        if x < 0 or y < 0:
            raise ValueError("\'x\' and \'y\' must be zero or a positive integer")
        if self.__grid[y][x] in BORDER_SYMBOL:
            raise AssertionError("\'x\' and \'y\' must be the coordinate of a walkable Cell")
        
        #list of Cell
        cells = {}
        walkable_cell = [(y, x)] #store walkable cell that not walk through yet
        grid = self.__grid.copy()

        while True:
            cell = walkable_cell.pop(0) #get a walkable cell
            _y, _x = cell[0], cell[1] # x and y ordinate of the cell
            
            #compute Cell id
            _id = _y*self.__width + _x

            #generate walkable Cell
            if grid[_y][_x] not in NOT_WALKABLE:
                cells[_id] = Cell(_id, _x, _y)
            
            #look up the top cell
            try:
                if _y - 1 < 0:
                    raise Exception
                if grid[_y-1][_x] in NOT_WALKABLE:
                    raise Exception
            except:
                pass
            else:
                walkable_cell.append((_y-1, _x))

            #look up the bottom cell
            try:
                if grid[_y+1][_x] in NOT_WALKABLE:
                    raise Exception
            except:
                pass
            else:
                walkable_cell.append((_y+1, _x))

            #look up the right cell
            try:
                if grid[_y][_x+1] in NOT_WALKABLE:
                    raise Exception
            except:
                pass
            else:
                walkable_cell.append((_y, _x+1))

            #look up the left cell
            try:
                if _x - 1 < 0:
                    raise Exception
                if grid[_y][_x -1] in NOT_WALKABLE:
                    raise Exception
            except:
                pass
            else:
                walkable_cell.append((_y, _x-1))

            grid[_y][_x] = NOT_WALKABLE[0] #remove generated Cell from the clone grid

            if walkable_cell == []:#break if there is no walkable Cell left
                break
        
        #sort the results ascending by id
        ids = sorted(cells) #sorted id
        cell_list = []
        
        for id_ in ids:
            cell_list.append(cells[id_])
        
        #add neighbor for cells
        for cell in cell_list:
            for other in cell_list:
                if cell.id == other.id: #skip if the Cell meet itself
                    continue
                if math.sqrt(math.pow(other.x-cell.x, 2) + math.pow(other.y-cell.y, 2)) == 1:
                    cell.add_neighbor_cell(other)

        #save cell graph
        self.__cell_graph = cell_list

        return cell_list

    def build_weighted_graph(self, x, y):
        """Return a list of Node that represents a Node graph
        
        Arguments:
            x {int} -- x ordinate of the fist walkable Cell
            y {int} -- y ordinate of the first walkable Cell
        
        Returns:
            list -- a list of Node instance
        """
        #build a graph
        cells = self.build_graph(x, y)
        node_dict = {}

        #generate a node dictionary
        for cell in cells: # for each cell in cells
            #if cell is intersection, cell is a Node
            if cell.is_intersection():
                node_dict[cell] = Node(cell)

        #find neighbor node
        for cell in node_dict:
            for neighbor in cell.neighbor_cell: # for each neighbor of the Cell
                last_cell = cell #last cell = root Cell
                cell_  = neighbor #current Cell
                loop = True # loop handler
                while loop:
                    if len(cell_.neighbor_cell) == 1:
                        break
                    for cell__ in cell_.neighbor_cell:
                        if cell__ is last_cell: #if cell is last cell
                            continue
                        elif cell__.is_intersection() and cell__ is not cell: #if cell is interection
                            #add neighbor node for the current node
                            node_dict[cell].add_neighbor_node(node_dict[cell__],\
                                int(math.sqrt(math.pow(cell.x - cell__.x, 2)+math.pow(cell.y - cell__.y, 2)))) 
                            loop = False # end while loop
                            break
                        else: # if cell is not an intersectionq
                            last_cell = cell_
                            cell_ = cell__ 
                            break
        
        #save node graph
        self.__node_graph = list(node_dict.values())

        return self.__node_graph

    def find_shortest_path(self, source_node, destination_node):
        
        #validate input
        if not isinstance(source_node, Node):
            raise TypeError("\'source_node\' must be an Node instance")
        if not isinstance(destination_node, Node):
            raise TypeError("\'destination_node\' must be an Node instance")

        #preprocessing assignment
        distance = {} # store the distance between the node and the source node
        prev_node = {} # store the current node and its previous node
        for node in self.__node_graph:
            if node is source_node:
                distance[node] = 0 # source node == 0
            else:
                distance[node] = 1000 # disance node == infinite

        unvisited_node = self.__node_graph #store unvisited node store from minimum distance to max distance
        i = 0

        while unvisited_node != []:
            current_node = unvisited_node[i] # assign the current node

            for node in current_node.neighbor_nodes: # for each neighbor node of current node
                distance_ = node[0] + distance[node[1]] #compute the distance between
                
                if distance_ < distance[current_node]: # if computed distance less than known distance
                    distance[current_node] = distance_
                    prev_node[current_node] = node[1]
                    if unvisited_node != []:
                        unvisited_node.pop(i) 
            
            i += 1
            if i >= len(unvisited_node):
                i = 0               
                    

        #back track the path from destination node to source node
        path = []
        current_node = destination_node
        
        while True:
            path.insert(0, current_node)
            current_node = prev_node[current_node]

            if current_node is source_node:
                path.insert(0, current_node)
                break

        return path
        
  
class Level:

    def __init__(self, number, pmap, objects):
        if self.__class__.__name__ == Level.__name__:
            raise Exception("The class Level MUST be instantiated with its factory methods")
        if number < 0:
            raise ValueError("\'number\' parameter must be a positive integer")
        
        self.number = number
        self.pmap = pmap
        self.objects = objects
        self.pacman = objects[0]
        self.ghosts = objects[1:5]
        self.bonuses = objects[5]

    @staticmethod
    def __build_instance(number, pmap, objects):    
        class LevelImpl(Level):
            def __init__(self, number, pmap, objects):
                super().__init__(number, pmap, objects)
        return LevelImpl(number, pmap, objects)

    @classmethod
    def load(cls, number, root_path_name="./"):
        path = pathlib.PosixPath(root_path_name)
        if root_path_name != "./":
            if  not path.is_dir():
                raise ValueError("\'root_path_name\' must point to an exist directory.")
            if not path.is_absolute():
                raise ValueError("\'root_path_name\' must be an absolute path.")
        
        #path to map dir
        map_level = root_path_name+"/map/level"+str(number)

        #load data from level?.json file
        data = json.load(open(map_level+".json"))

        #generate objects
        objects = [
            Pacman(data[PACMAN][X],data[PACMAN][Y], PACMAN_SYMBOL, (255,255,0)),
            Pinky(data[PINKY][X], data[PINKY][Y]),
            Inky(data[INKY][X], data[INKY][Y]),
            Blinky(data[BLINKY][X], data[BLINKY][Y]),
            Clyde(data[CLYDE][X], data[CLYDE][Y]),
            Bonus(data[CHERRY][0][X], data[CHERRY][0][Y], data[CHERRY][0][SYMBOL], data[CHERRY][0][POINTS]),
            StandingStartAnnouncement(data[STANDING_START_ANNOUNCEMENT][X],\
                 data[STANDING_START_ANNOUNCEMENT][Y])
        ]
        
        return cls.__build_instance(number, Map.load_map(map_level+".rle"), objects)

class Palette:
    """
    Return a Palette instance to manipulate curses color library
    """

    def __init__(self):
        #store pair color in this list meaning: pair_number = indice + 2 
        self.__color_number = []

    def get_composite_color(self, foreground_color, background_color=(0, 0, 0)):
        """Return pair_number of curses pair_color
        
        Arguments:
            foreground_color {tuple} -- foreground color of the symbol
        
        Keyword Arguments:
            background_color {tuple} -- background color of the symbol (default: {(0, 0, 0})
        
        Raises:
            TypeError: raise if foreground_color is not a tuple
            AssertionError: raise if foreground_color must be a tuple of three paramenter
            TypeError: raise if foreground_color must be a tuple of three integer
            ValueError: raise if foreground_color must be a tuple of three integer between 0 and 255
        
        Returns:
            int -- an integer represents pair_number of a pair_color
        """
        #validate foreground_color argument
        if not isinstance(foreground_color, tuple):
            raise TypeError("foreground_color must be a tuple")
        if len(foreground_color) != 3:
            raise AssertionError("foreground_color must be a tuple of three paramenter")
        if not all([isinstance(i, int) for i in foreground_color]):
            raise TypeError("foreground_color must be a tuple of three integer")
        if (foreground_color[0] < 0 or foreground_color[0] > 255) and \
            (foreground_color[1] < 0 or foreground_color[1] > 255) and \
                (foreground_color[2] < 0 or foreground_color[2] > 255):
            raise ValueError("foreground_color must be a tuple of three integer between 0 and 255")
        
        #validate background_color argument
        if background_color != (0, 0, 0):
            if not isinstance(background_color, tuple):
                raise TypeError("background_color must be a tuple")
            if len(background_color) != 3:
                raise AssertionError("background_color must be a tuple of three paramenter")
            if not all([isinstance(i, int) for i in background_color]):
                raise TypeError("background_color must be a tuple of three integer")
            if (background_color[0] < 0 or background_color[0] > 255) and \
                (background_color[1] < 0 or background_color[1] > 255) and \
                    (background_color[2] < 0 or background_color[2] > 255):
                raise ValueError("background_color must be a tuple of three integer between 0 and 255")

        #create pair_color values
        pair_color = (foreground_color, background_color)

        #if color has registered
        if pair_color in self.__color_number:
            return self.__color_number.index(pair_color) + 2

        #if color has not registered yet
        else:
            pair_number = len(self.__color_number) + 1
            curses.init_color(pair_number*2, int(foreground_color[0]/256*1000), int(foreground_color[1]/256*1000), int(foreground_color[2]/256*1000))
            curses.init_color(pair_number*2+1, int(background_color[0]/256*1000), int(background_color[1]/256*1000), int(background_color[2]/256*1000))
            curses.init_pair(pair_number*2, pair_number*2, pair_number*2+1)
            self.__color_number.append(pair_color)

            return pair_number

class Scene:
    """The class control the output graphic of the game
    
    Raises:
        TypeError: raise if 'window' is not an object
        TypeError: raise if 'level' is not an Level object

    Arguments:
        window {object} - a window object of curses library
        level {Level} - a Level object

    Attributes:
        __window - store a window object
        __level - store a Level object    
        points - store points gained by player
        life - store the amount of life left
        death - store live condition of Pacman
        power_capsule - strigger Pacman eat capsule event
        flash - strigger flash stage of ghosts after pacman eat power capsule
        standing_start_announcement - strigger game is starting event
        blinky_ate, pinky_ate, inky_ate, clyde_ate - strigger ghosts have been eaten event
    """
    
    def __init__(self, window, level):
        if not isinstance(window, object):
            raise TypeError("\'window\' must be a window object.")
        if not isinstance(level, Level):
            raise TypeError("\'level\' must be a Level object.")
        self.__window = window
        self.__level = level
        self.points = 0
        self.life = 4
        self.death = False
        self.power_capsule = False
        self.flash = False
        self.standing_start_announcement = False
        self.blinky_ate = False
        self.pinky_ate = False
        self.inky_ate = False
        self.clyde_ate = False

    #instance methos that control resizing
    def __is_fully_visible(self):
        """Check if the window is large enough
        
        Returns:
            bool -- window is large enough or not
        """
        window_size = self.__window.getmaxyx()
        if window_size[1] < 38 or window_size[0] < 38:
            return True
        return False
    
    #centering text
    def __centering_text(self, y, x, text, color):
        self.__window.addstr(y,x-int(len(text)/2), text, color)

    def __display_header_and_footer(self, resize_x, resize_y):
        """Display header and footer of the game scene"""
        self.__window.addstr(2+resize_y, 6+resize_x, "1UP    HIGH SCORE    2UP", curses.color_pair(16))
        self.__centering_text(3+resize_y, 7+resize_x, str(self.points), curses.color_pair(16))
        self.__centering_text(3+resize_y, 17+resize_x, str(self.points), curses.color_pair(16))
        self.__centering_text(3+resize_y, 28+resize_x, "0", curses.color_pair(16))
        self.__window.addstr(34+resize_y, 6+resize_x, PACMAN_SYMBOL*self.life, curses.color_pair(2))

    def __display_the_map(self, resize_x, resize_y):
        """Display pacman map"""
        grid = self.__level.pmap.grid
        for y in range(self.__level.pmap.height):
            for x in range(self.__level.pmap.width):
                if grid[y][x] in BORDER_SYMBOL:
                    self.__window.addch(y+4+resize_y, x+4+resize_x, grid[y][x], curses.color_pair(12))
                elif grid[y][x] in ['·', '•']:
                    self.__window.addch(y+4+resize_y, x+4+resize_x, grid[y][x], curses.color_pair(14))
                elif grid[y][x] in ['x', '-']:
                    self.__window.addch(y+4+resize_y, x+4+resize_x, ' ', curses.color_pair(12))
                else:
                    self.__window.addch(y+4+resize_y, x+4+resize_x, grid[y][x], curses.color_pair(12))

    def __display_bonuses(self, resize_x, resize_y):
        """Display bonuses"""
        if self.__level.bonuses.points != 0 and  \
        (self.__level.ghosts[0].x != self.__level.bonuses.x and self.__level.ghosts[0].y != self.__level.bonuses.y) and \
            (self.__level.ghosts[1].x != self.__level.bonuses.x and self.__level.ghosts[1].y != self.__level.bonuses.y) and  \
                (self.__level.ghosts[2].x != self.__level.bonuses.x and self.__level.ghosts[2].y != self.__level.bonuses.y) and \
                    (self.__level.ghosts[3].x != self.__level.bonuses.x and self.__level.ghosts[3].y != self.__level.bonuses.y) and \
                        (self.__level.pacman.x != self.__level.bonuses.x and self.__level.pacman.y != self.__level.bonuses.y):

            self.__window.addch(self.__level.bonuses.y+4+resize_y, self.__level.bonuses.x+4+resize_x, self.__level.bonuses.symbol, curses.color_pair(12))
            self.__window.addch(34+resize_y, 28+resize_x, self.__level.bonuses.symbol)

    def __display_animated_character(self, resize_x, resize_y):
        """Display pacman and ghosts"""

        if not self.power_capsule:
            self.__window.addch(self.__level.ghosts[0].y+4+resize_y, self.__level.ghosts[0].x+4+resize_x, self.__level.ghosts[0].symbol, curses.color_pair(4))
            self.__window.addch(self.__level.ghosts[1].y+4+resize_y, self.__level.ghosts[1].x+4+resize_x, self.__level.ghosts[1].symbol, curses.color_pair(6))
            self.__window.addch(self.__level.ghosts[2].y+4+resize_y, self.__level.ghosts[2].x+4+resize_x, self.__level.ghosts[2].symbol, curses.color_pair(8))
            self.__window.addch(self.__level.ghosts[3].y+4+resize_y, self.__level.ghosts[3].x+4+resize_x, self.__level.ghosts[3].symbol, curses.color_pair(10))

        #if pacman ate power capsule
        else:
            if not self.flash:
                #blue ghosts
                self.__window.addch(self.__level.ghosts[0].y+4+resize_y, self.__level.ghosts[0].x+4+resize_x, self.__level.ghosts[0].symbol, curses.color_pair(18))
                self.__window.addch(self.__level.ghosts[1].y+4+resize_y, self.__level.ghosts[1].x+4+resize_x, self.__level.ghosts[1].symbol, curses.color_pair(18))
                self.__window.addch(self.__level.ghosts[2].y+4+resize_y, self.__level.ghosts[2].x+4+resize_x, self.__level.ghosts[2].symbol, curses.color_pair(18))
                self.__window.addch(self.__level.ghosts[3].y+4+resize_y, self.__level.ghosts[3].x+4+resize_x, self.__level.ghosts[3].symbol, curses.color_pair(18))

            else:
                #blue ghosts
                self.__window.addch(self.__level.ghosts[0].y+4+resize_y, self.__level.ghosts[0].x+4+resize_x, self.__level.ghosts[0].symbol, curses.color_pair(16))
                self.__window.addch(self.__level.ghosts[1].y+4+resize_y, self.__level.ghosts[1].x+4+resize_x, self.__level.ghosts[1].symbol, curses.color_pair(16))
                self.__window.addch(self.__level.ghosts[2].y+4+resize_y, self.__level.ghosts[2].x+4+resize_x, self.__level.ghosts[2].symbol, curses.color_pair(16))
                self.__window.addch(self.__level.ghosts[3].y+4+resize_y, self.__level.ghosts[3].x+4+resize_x, self.__level.ghosts[3].symbol, curses.color_pair(16))
                
                self.__window.refresh()
                curses.napms(10)

                #white ghosts
                self.__window.addch(self.__level.ghosts[0].y+4+resize_y, self.__level.ghosts[0].x+4+resize_x, self.__level.ghosts[0].symbol, curses.color_pair(18))
                self.__window.addch(self.__level.ghosts[1].y+4+resize_y, self.__level.ghosts[1].x+4+resize_x, self.__level.ghosts[1].symbol, curses.color_pair(18))
                self.__window.addch(self.__level.ghosts[2].y+4+resize_y, self.__level.ghosts[2].x+4+resize_x, self.__level.ghosts[2].symbol, curses.color_pair(18))
                self.__window.addch(self.__level.ghosts[3].y+4+resize_y, self.__level.ghosts[3].x+4+resize_x, self.__level.ghosts[3].symbol, curses.color_pair(18))
            

    def __display_pacman_dead(self, resize_x, resize_y):
        """Display pacman dead scene"""

        #display pacman
        if not self.death:
            self.__window.addch(self.__level.pacman.y+4+resize_y, self.__level.pacman.x+4+resize_x, self.__level.pacman.symbol, curses.color_pair(2))
        else:
            #display death scene
            self.__window.addch(self.__level.pacman.y+4+resize_y, self.__level.pacman.x+4+resize_x, SKULL)
            curses.napms(100)
            self.__window.refresh()

            self.__window.addch(self.__level.pacman.y+4+resize_y, self.__level.pacman.x+4+resize_x, EXPLODING)
            curses.napms(100)
            self.__window.refresh()

    def __display_ghosts_eyes(self, resize_x, resize_y):
        """Display ghost eyes after ghost have been eaten"""
        if self.blinky_ate:
            self.__window.addch(self.__level.ghosts[0].y+4+resize_y, self.__level.ghosts[0].x+4+resize_x, EYES)
        if self.pinky_ate:
            self.__window.addch(self.__level.ghosts[1].y+4+resize_y, self.__level.ghosts[1].x+4+resize_x, EYES)
        if self.inky_ate:
            self.__window.addch(self.__level.ghosts[2].y+4+resize_y, self.__level.ghosts[2].x+4+resize_x, EYES)
        if self.clyde_ate:
            self.__window.addch(self.__level.ghosts[3].y+4+resize_y, self.__level.ghosts[3].x+4+resize_x, EYES)
         
    def __display_standing_start_annoucement(self, resize_x, resize_y):

        if self.standing_start_announcement:
            #display the map
            self.__window.refresh()
            curses.napms(200)

            #display the announcement
            self.__window.addstr(self.__level.objects[6].y+4+resize_y, self.__level.objects[6].x+1+resize_x, READY, curses.color_pair(2))
            self.__window.refresh()
            curses.napms(200)
    
    def __display_enlarge_annoucement(self, resize_x, resize_y):
        """Display enlarge screen annoucement"""
        
        self.__window.clear()
        self.__window.addstr("Enlarge your... terminal!", curses.color_pair(16))
        self.__window.refresh()

    #instance method that display the game
    def render(self):
        """Display the graphic
        
        Returns:
            int -- return an ascii value of pressed key
        """
        #start curses color library
        curses.start_color()

        # Create a palette and register the colors.
        palette = Palette()
        palette.get_composite_color(COLOR_RGB_PACMAN)
        palette.get_composite_color(COLOR_RGB_BLINKY)
        palette.get_composite_color(COLOR_RGB_PINKY)
        palette.get_composite_color(COLOR_RGB_INKY)
        palette.get_composite_color(COLOR_RGB_CLYDE)
        palette.get_composite_color(COLOR_RGB_BLUE)
        palette.get_composite_color(COLOR_RGB_ORANGE)
        palette.get_composite_color(COLOR_RGB_WHITE)
        palette.get_composite_color(COLOR_RGB_BRIGHT_BLUE)

        #control graphics and resizing window
        window_size = self.__window.getmaxyx()
        resize_y = int((window_size[0] - 36)/2)
        resize_x = int((window_size[1] - 36)/2)

        #check if map is fully visible
        visible = self.__is_fully_visible()
        if visible:
            self.__display_enlarge_annoucement(resize_x, resize_y)
        
        else:
            # display header and footer
            self.__display_header_and_footer(resize_x, resize_y)

            #display the map
            self.__display_the_map(resize_x, resize_y)
            
            #display bonuses
            self.__display_bonuses(resize_x, resize_y)
            
            #display animated character
            self.__display_animated_character(resize_x, resize_y)

            #ghost become eyes after being eaten
            self.__display_ghosts_eyes(resize_x, resize_y)

            self.__display_pacman_dead(resize_x, resize_y)

        #standing start announcement
        self.__display_standing_start_annoucement(resize_x, resize_y)

        #refresh grahics
        self.__window.refresh()

class Cell:
    """Cell of a pacman map
    
    Raises:
        TypeError: raise if 'id_', 'x' and 'y' is not an integer 
        ValueError: raise if 'id_', 'x' and 'y' is not an positive integer
    
    Arguments:
        id_ {int} - number position of the Cell
        x {int} - x ordinate position of the Cell
        y {int} - y ordinate position of the Cell

    Attributes:
        __id - store number position of the Cell
        __x - store x ordinate of the Cell
        __y - store y ordinate of the Cell
        __neighbor_cell - store address its neighbor Cell
        __intersection - store number of Cell that the Cell itself is neighbor
    """
    def __init__(self, id_, x, y):
        #validate input
        if not isinstance(id_, int):
            raise TypeError("\'id_\' parameter must be an integer.")
        if not isinstance(x, int):
            raise TypeError("\'x\' parameter must be an integer.")
        if not isinstance(y, int):
            raise TypeError("\'y\' parameter must be an integer.")

        if id_ < 0 or x < 0 or y < 0:
            raise ValueError("\'id_\', \'x\' and \'y\' must be zero or an positive integer.")

        self.__id = id_
        self.__x = x
        self.__y = y
        self.__neighbor_cell = []
        self.intersection = 0

    @property
    def id(self):
        return self.__id

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    @property
    def neighbor_cell(self):
        return self.__neighbor_cell

    def add_neighbor_cell(self, other):
        """Add the other Cell as its neighbor Cell
        
        Arguments:
            other {obj} -- a Cell object that near the current Cell

        Returns:
            bool -- True if intersection >= 3 else False
        """
        #validate input 
        if not isinstance(other, Cell):
            raise TypeError("\'cell\' must be a Cell object")

        #find distance between two Cell
        if int(math.sqrt(math.pow(other.x-self.x, 2) + math.pow(other.y-self.y, 2))) != 1:
            raise AssertionError("other Cell must be a neighbor of the current Cell")
        
        #add neighbor Cell to the list
        self.__neighbor_cell.append(other)
        
        #note that the Cell has a neighbor
        self.intersection += 1

    def is_intersection(self):
        """Return True if the Cell has more than two neighbor
        """
        #handle the processing
        if self.intersection < 3:
            return False
        else:
            return True

class Node:
    """A Node cell of a pacman map
    
    Raises:
        TypeError: raise if cell is not an Cell

    Arguments:
        cell {cell} -- an Cell instance

    Attributes:
        __cell -- store an Cell instance
        __neighbor_node -- store neighbor node of the current Node
    """
    def __init__(self, cell):
        #validate input
        if not isinstance(cell, Cell):
            raise TypeError("\'cell\' must be an Cell instance")

        self.__cell = cell
        self.__neighbor_node = []

    @property
    def id(self):
        return self.__cell.id

    @property
    def x(self):
        return self.__cell.x

    @property
    def y(self):
        return self.__cell.y
    
    @property
    def neighbor_nodes(self):
        return self.__neighbor_node

    def add_neighbor_node(self, node, distance):
        """Add a neighbor node with proper distance of the current node
        
        Arguments:
            node {Node} -- a Node instance
            distance {int} -- distance between two node
        
        Raises:
            TypeError: raise if node is not an Node instance
            TypeError: raise if distance is not an integer
            ValueError: raise if distance is not an positive integer
        """

        #validate input
        if not isinstance(node, Node):
            raise TypeError("\'node\' must be an Node instance")        
        if not isinstance(distance, int):
            raise TypeError("\'distance\' must be an integer")
        if distance <= 0:
            raise ValueError("\'distance\' must be an positive integer")

        #add neighbor node
        self.__neighbor_node.append((distance, node))