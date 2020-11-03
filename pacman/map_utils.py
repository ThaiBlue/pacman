#!/usr/bin/env python3

import pathlib

BORDER_SYMBOL = ["═", "║", "╔", "╗", "╚", "╝", "*"]
BORDERS = ['═', '║', '╔', '╗', '╚', '╝']

def load_map(file_pathname):
    """Return a list of each line of the target map in the map file
    
    Arguments:
        file_pathname {str} -- path to the target map file
    
    Raises:
        ValueError: raise if 'file_pathname' is not a path to a exist file
    
    Returns:
        list -- list of each line of the target map
    """
    file = pathlib.PosixPath(file_pathname)
    if not file.is_file():
       raise ValueError("\'file_pathname\' must be a path to target file")

    #read the target map   
    f = file.open("r")
    _map = f.read()
    pacman_map = _map.split("\n")
    f.close()

    return pacman_map

def simplify_map(pacman_map):
    """Return a simplified map of the original pacman map
    
    Arguments:
        pacman_map {list} -- list of line of pacman map
    
    Raises:
        TypeError: raise if 'pacman_map' is not a list
        TypeError: raise if 'pacman_map' is not a list of line of original map
    
    Returns:
        simplified_pacman_map -- a list of line of simplified pacman map
    """
    if not isinstance(pacman_map, list):
        raise TypeError("\'pacman_map\' must be a list")

    simplified_pacman_map = []
    for line in pacman_map:
        if not isinstance(line, str):
            raise TypeError("\'pacman_map\' must be a list of strings")
        newline = ""
        for pos in range(len(line)):
            if line[pos] in ["═", "║", "╔", "╗", "╚", "╝"]:
                newline += "*"
            elif line[pos] == "·":
                newline += "."
            elif line[pos] == "•":
                newline += "o"
            else:
                newline += line[pos]
        simplified_pacman_map.append(newline)
    
    return simplified_pacman_map

def prettify_map(pacman_map):

    if not isinstance(pacman_map, list):
        raise TypeError("\'pacman_map\' must be a list")
    
    #dictionary of border line
    border_line = {
        "topleft" : "╝",
        "topright" : "╚",
        "bottomleft" : "╗",
        "bottomright" : "╔",
        "leftright" : "═",
        "topbottom" : "║"
    }

    #generate the fist stage of prettifying the simplified map
    _1st_stage_map = []
    for line in range(len(pacman_map)):
        if not isinstance(pacman_map[line], str):
            raise TypeError("\'pacman_map\' must be a list of string line of pacman map")

        newline = ""
        for pos in range(len(pacman_map[line])):
            if pacman_map[line][pos] == ".":
                newline += "·"
            elif pacman_map[line][pos] == "o":
                newline += "•"
            elif pacman_map[line][pos] == "*":
                border_type = ""
                #look up the top of the border point
                try:
                    pacman_map[line-1][pos]
                    if line - 1 < 0:
                        raise Exception
                except:
                    pass
                else:
                    if pacman_map[line-1][pos] in ["*"]:
                        border_type += "top"

                #look up the bottom of the border point
                try:
                    pacman_map[line+1][pos]
                except:
                    pass
                else:
                    if pacman_map[line+1][pos] in ["*"]:
                        border_type += "bottom"

                #look up the left of the border point
                try:
                    pacman_map[line][pos-1]
                    if pos - 1 < 0:
                        raise Exception
                except:
                    pass
                else:
                    if pacman_map[line][pos-1] in ["*"]:
                        border_type += "left"

                #look up the right of the border point
                try:
                    pacman_map[line][pos+1]
                except:
                    pass
                else:
                    if pacman_map[line][pos+1] in ["*"]:
                        border_type += "right"

                if border_type in border_line:
                    newline += border_line[border_type]
                else:
                    newline += pacman_map[line][pos]
            else:
                newline += pacman_map[line][pos]

        if newline != "":
            _1st_stage_map.append(newline)

    #generate the second stage of prettifying the simplified map
    _2nd_stage_map = []
    for line in range(len(_1st_stage_map)):
        newline = ""
        for pos in range(len(_1st_stage_map[line])):
            if _1st_stage_map[line][pos] != "*":
                newline += _1st_stage_map[line][pos]
            else:
                #assign a variable which will represent border symbol found as '12345678'
                # as top-left, top, top-right, right, ...etc, left. 
                vision = ""

                #look up top-left 
                try:
                    _1st_stage_map[line-1][pos-1]
                    if line - 1 < 0 or pos - 1 < 0:
                        raise Exception
                except:
                    pass
                else:
                    if _1st_stage_map[line-1][pos-1] in BORDER_SYMBOL:
                        vision += "1"

                #look up top
                try:
                    _1st_stage_map[line-1][pos]
                    if line - 1 < 0:
                        raise Exception
                except:
                    pass
                else:
                    if _1st_stage_map[line-1][pos] in BORDER_SYMBOL:
                        vision += "2"

                #look up top-right 
                try:
                    _1st_stage_map[line-1][pos+1]
                    if line - 1 < 0:
                        raise Exception
                except:
                    pass
                else:
                    if _1st_stage_map[line-1][pos+1] in BORDER_SYMBOL:
                        vision += "3"

                #look up right 
                try:
                    _1st_stage_map[line][pos+1]
                except:
                    pass
                else:
                    if _1st_stage_map[line][pos+1] in BORDER_SYMBOL:
                        vision += "4"

                #look up bottom-right 
                try:
                    _1st_stage_map[line+1][pos+1]
                except:
                    pass
                else:
                    if _1st_stage_map[line+1][pos+1] in BORDER_SYMBOL:
                        vision += "5"

                #look up bottom
                try:
                    _1st_stage_map[line+1][pos]
                except:
                    pass
                else:
                    if _1st_stage_map[line+1][pos] in BORDER_SYMBOL:
                        vision += "6"
                        
                #look up bottom-left 
                try:
                    _1st_stage_map[line+1][pos-1]
                    if pos - 1 < 0:
                        raise Exception
                except:
                    pass
                else:
                    if _1st_stage_map[line+1][pos-1] in BORDER_SYMBOL:
                        vision += "7"

                #look up left 
                try:
                    _1st_stage_map[line][pos-1]
                    if pos - 1 < 0:
                        raise Exception
                except:
                    pass
                else:
                    if _1st_stage_map[line][pos-1] in BORDER_SYMBOL:
                        vision += "8"

                if vision in ["4", "8", "12348", "45678", "123458", "123478", "345678", "145678"]:
                    newline += "═"
                elif vision in ["123456", "123678", "23456", "12678", "125678", "234567", "6"]:
                    newline += "║"
                elif vision in ["4678", "1234678", "2346"]:
                    newline += "╔"
                elif vision in ["4568", "1234568", "1268"]:
                    newline += "╗"
                elif vision in ["1245678", "2456", "1248"]:
                    newline += "╚"
                elif vision in ["2345678", "2678", "2348"]:
                    newline += "╝"
                else:
                    print(line, pos, vision)   
                
        if newline != "":
            _2nd_stage_map.append(newline)
                
    #generate the third stage of the map
    _3rd_stage_map = []
    for line in range(len(_2nd_stage_map)):
        newline = ""
        for pos in range(len(_2nd_stage_map[line])):
            if (pos == 0 or pos == len(_2nd_stage_map[line])-1) and\
                 _2nd_stage_map[line][pos] in ["╗", "╔"]:
                
                #store symbol that seen
                vision = ""

                #look up the top postition
                try:
                    _2nd_stage_map[line-1][pos]
                    if line - 1 < 0:
                        raise Exception
                except:
                    pass
                else:
                    if _2nd_stage_map[line-1][pos] in BORDER_SYMBOL:
                        vision += _2nd_stage_map[line-1][pos]

                #look up the bottom of the border point
                try:
                    _2nd_stage_map[line+1][pos]
                except:
                    pass
                else:
                    if _2nd_stage_map[line+1][pos] in BORDER_SYMBOL:
                        vision += _2nd_stage_map[line+1][pos]

                #look up the left of the border point
                try:
                    _2nd_stage_map[line][pos-1]
                    if pos - 1 < 0:
                        raise Exception
                except:
                    pass
                else:
                    if _2nd_stage_map[line][pos-1] in BORDER_SYMBOL:
                        vision += _2nd_stage_map[line][pos-1]

                #look up the right of the border point
                try:
                    _2nd_stage_map[line][pos+1]
                except:
                    pass
                else:
                    if _2nd_stage_map[line][pos+1] in BORDER_SYMBOL:
                        vision += _2nd_stage_map[line][pos-1]

                if vision in ["╔╗", "╗═"]:
                    newline += "═"
                elif vision in ["╔║╗", "╚║╗", "║╗", "╚╗"]:
                    newline += "╔"
                elif vision in ["╗║═", "╝║═", "║═", "╝═"]:
                    newline += "╗"

            else:
                newline += _2nd_stage_map[line][pos]

        if newline != "":
            _3rd_stage_map.append(newline)

    #generate the fourth stage of the map 
    #generate the third stage of the map
    _4th_stage_map = []
    for line in range(len(_3rd_stage_map)):
        newline = ""
        for pos in range(len(_3rd_stage_map[line])):
            if (pos == 0 or pos == len(_3rd_stage_map[line])-1) and\
                 _3rd_stage_map[line][pos] in ["╝", "╚"]:
                
                #store symbol that seen
                vision = ""

                #look up the top postition
                try:
                    _3rd_stage_map[line-1][pos]
                    if line - 1 < 0:
                        raise Exception
                except:
                    pass
                else:
                    if _3rd_stage_map[line-1][pos] in BORDER_SYMBOL:
                        vision += _3rd_stage_map[line-1][pos]

                #look up the bottom of the border point
                try:
                    _3rd_stage_map[line+1][pos]
                except:
                    pass
                else:
                    if _3rd_stage_map[line+1][pos] in BORDER_SYMBOL:
                        vision += _3rd_stage_map[line+1][pos]

                #look up the left of the border point
                try:
                    _3rd_stage_map[line][pos-1]
                    if pos - 1 < 0:
                        raise Exception
                except:
                    pass
                else:
                    if _3rd_stage_map[line][pos-1] in BORDER_SYMBOL:
                        vision += _3rd_stage_map[line][pos-1]

                #look up the right of the border point
                try:
                    _3rd_stage_map[line][pos+1]
                except:
                    pass
                else:
                    if _3rd_stage_map[line][pos+1] in BORDER_SYMBOL:
                        vision += _3rd_stage_map[line][pos-1]

                if vision in ["╚╝", "╝═"]:
                    newline += "═"
                elif vision in ["║╚╝", "║╔╝", "║╝", "╔╝"]:
                    newline += "╚"
                elif vision in ["║╝═", "║╗═", "║═", "╗═"]:
                    newline += "╝"

            else:
                newline += _3rd_stage_map[line][pos]

        if newline != "":
            _4th_stage_map.append(newline)

    return _4th_stage_map

def compress_map_with_rle(pacman_map):
    """Return a RLE map of the simplified map
    
    Arguments:
        pacman_map {list} -- list of string line of the map
    
    Raises:
        TypeError: raise if 'pacman_map' is not a list
        TypeError: raise if 'pacman_map' is not a list of string line
    
    Returns:
        list -- list of string line of RLE map
    """
    if not isinstance(pacman_map, list):
        raise TypeError("\'pacman_map\' must be a list")

    rle_map = []
    for line in pacman_map:

        if not isinstance(line, str):
            raise TypeError("\'pacman_map\' must be a list of string line of the map")

        newline = ""
        current_symbol = ""
        same_sym_amount = 0
        saved = False

        for pos in line:
            if current_symbol == pos:
                same_sym_amount += 1
            elif current_symbol == "":
                current_symbol = pos
                same_sym_amount += 1
            elif current_symbol != pos:
                newline += str(same_sym_amount) + current_symbol
                current_symbol = pos
                same_sym_amount = 1
                saved = True

        if not saved and same_sym_amount != 0:
            newline += str(same_sym_amount) + current_symbol

        rle_map.append(newline)
    
    return rle_map

def save_map(pacman_map, file_pathname):
    """Write the map into a new map file that specified by 'file_pathnam' argument
    
    Arguments:
        pacman_map {list} -- list of string line of a pacman map
        file_pathname {str} -- pathname of the new map file
    
    Raises:
        TypeError: raise if 'pacman_map' argument is not a list
        ValueError: raise if 'file_pathname' exists already
        TypeError: raise if 'pacman_map' is not a list of string line of a pacman map
    """
    if not isinstance(pacman_map, list):
        raise TypeError("\'pacman_map\' must be a list")

    path = pathlib.PosixPath(file_pathname)
    if path.is_file():
        raise ValueError("file_pathname already exists, please choose another file_pathname.")
    
    file_map = path.open("w+")
    for line in pacman_map:
        if not isinstance(line, str):
            raise TypeError("\'pacman_map\' must be a list of string line of the map")
        
        file_map.write(line+'\n')

    file_map.close()

def uncompress_map_with_rle(compress_map):
    """Return an uncompress map of the RLE version of the map
    
    Arguments:
        compress_map {list} -- list of string line of the RLE compress map
    
    Raises:
        TypeError: raise if 'compress_map' is not a list 
        TypeError: raise if 'compress_mao' is not a list of string line
      
    Returns:
        list -- simplified version of the pacman map
    """
    if not isinstance(compress_map, list):
        raise TypeError("\'compress_map\' must be a list")
    
    uncompress_map = []
    for line in compress_map:
        if not isinstance(line, str):
            raise TypeError("\'compress_map\' must be a list of string line of the map")
        
        newline = ""
        last_sym_pos = -1

        for pos in range(len(line)):
            if line[pos] not in "0123456789":
                newline += int(line[last_sym_pos+1:pos])*line[pos]
                last_sym_pos = pos

        uncompress_map.append(newline)
    
    return uncompress_map
