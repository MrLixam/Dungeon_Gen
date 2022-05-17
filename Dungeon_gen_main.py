from random import randint
from time import sleep
import matplotlib.pyplot as plt
from math import sqrt
import numpy as np


class Entity:
    def __init__(self, Etype: int, pos: tuple, Ename: str, stats: dict):
        self.Etype = Etype
        self.status = []
        self.stats = stats
        self.modifiers = []
        self.position = pos
        self.Ename = Ename

    def ShowStats(self):
        print('Name: ', self.Ename)
        print('Type: ', self.Etype)
        print('Status: ', self.status)
        print('Stats: ', self.health)
        print('Buffs/Debuffs: ', self.modifiers)

    def MoveEntity(self, newpos: tuple):
        '''
        Used to move an entity
        newpos: tuple
            the new position of the entity
        Returns
        None
        '''
        assert newpos.type == tuple, "ErrorCode: invalid_var_type"
        assert len(newpos) == 2, "ErrorCode: invalid_coordinates_format"
        assert newpos[0] <= 10, "ErrorCode: invalid_x_coordinates"
        assert newpos[1] <= 10, "ErrorCode: invalid_y_coordinates"
        self.position = newpos

    def EntityUpdate(self):
        pass


class Room:
    def __init__(self, rtype: int, position: tuple, name: str):
        self.rtype = rtype
        self.position = position
        self.contents = []
        self.name = name

    def ShowStats(self):
        print("")
        print("~~~~~~")
        print('Type de la pièce: ', self.rtype)
        print('Position dans le donjon: ', self.position)
        print('Entités presentes dans la pièce: ')
        for i in range(len(self.contents)):
            self.contents[i].ShowStats()
            print('')
        print('Numero de la pièce: ', self.name)
        print("~~~~~~")

    def UpdatePos(self, newPos: tuple):
        assert newPos.type == tuple, 'ErrorCode: invalid_pos_type'
        self.position = newPos


    def AddEntity(self, name: str, pos: tuple, etype: int):
        '''
        Used to place an entity other than a door
        name : str
            Name of the entity.
        pos : tuple
            position of entity in the room.
        etype : int
            Entity type, only above 0 here, otherwise door.

        Returns
        None.

        '''

        assert 0 <= pos[0] <= 10, "ErrorCode: invalid_x_coordinate"

        assert 0 <= pos[1] <= 10, "ErrorCode: invalid_y_coordinate"
        new_entity = Entity(etype, pos, name)
        self.contents.append(new_entity)


class Dungeon:
    '''
    To get the Stats of a room in a dungeon,
    use command [name of dungeon].rooms[index of room (which is number of the room-1)].ShowStats()
    example:
        to get the stats of the room number 6 in dungeon "X":
            X.rooms[5].ShowStats()
    '''

    def __init__(self, size: int, diff: int):
        self.Dsize = size
        self.Ddiff = diff
        self.NumberRooms = randint(3 + size, 5 + size + diff)
        self.rooms = []
        self.RoomGenDone = False
        self.CoordsGenDone = False
        self.graphSize = size*50*(diff*0.5)
        self.list_coords = []
        self.relations = []

    def ShowStats(self):
        print('Nombre de pièces: ', self.NumberRooms)
        print('Difficulté: ', self.Ddiff)
        print('Liste des pièces présentes dans le dongeon: ')
        for i in range(len(self.rooms)):
            self.rooms[i].ShowStats()
        print(self.relations)

    def Room(self,i):
        '''
        info about room  in dungeon
        '''
        return self.rooms[i-1].ShowStats()

    def CoordsGen(self):
        print(self.NumberRooms)
        limit = 0.03*self.graphSize
        print(limit)
        coords_current = []
        while len(self.list_coords) <= self.NumberRooms:
            coordx = randint(0, self.graphSize)
            coordy = randint(0, self.graphSize)
            curr_tuple = (coordx, coordy)
            print("ok")
            coord_ok = True
            if len(coords_current) == 0:
                coords_current.append(curr_tuple)
                self.list_coords.append(curr_tuple)
            else:
                for i in range(len(coords_current)):
                    coord_checked_x = coords_current[i][0]
                    coord_checked_y = coords_current[i][1]
                    distance = sqrt((coord_checked_x - coordx)**2 + (coord_checked_y - coordy)**2)
                    print(distance)
                    if distance < limit:
                        coord_ok = False
                if coord_ok:
                    print("yes", curr_tuple)
                    coords_current.append(curr_tuple)
                    self.list_coords.append(curr_tuple)
                else:
                    print("no")

        self.CoordsGenDone = True

    def LinkGen(self):
        coords = self.list_coords.copy()
        curr_coord = None
        for i in range(len(coords)-1):
            dist = []
            curr_coord = coords[i]
            for k in range(len(coords)):
                if k==i :
                    continue
                else:
                    c_point = coords[k]
                    distance = (sqrt((c_point[0] - curr_coord[0])**2 + (c_point[1] - curr_coord[1])**2))
                    dist.append((distance,list(c_point)))
            dist.sort()
            closest = (list(curr_coord), dist[0][1], dist[1][1], dist[2][1])
            self.relations.append(closest)
        return


    def RoomListGen(self):
        '''
        Generates the list of all the rooms of the Dungeon, stored in self.rooms
        Used for the Map generation

        Returns
        -------
        None.

        '''
        assert self.CoordsGenDone, "ErrorCode: no coordinates generated"
        if not self.RoomGenDone:
            for i in range(self.NumberRooms):
                roomX = Room(randint(0, 6), (self.list_coords[i][0], self.list_coords[i][1]), str("Room " + str(i + 1)))
                self.rooms.append(roomX)
        self.RoomGenDone = True

    def Show_Dungeon(self):
        x = self.graphSize
        y = self.graphSize
        x_room = []
        y_room = []
        line_x = []
        line_y = []
        plt.plot(x, y)
        for i in range(len(self.list_coords)):
            x_room.append(self.list_coords[i][0])
            y_room.append(self.list_coords[i][1])
        plt.scatter(x_room, y_room, color = 'red')
        for i in range(len(x_room)):
            plt.annotate('Room' + str(i),(x_room[i], y_room[i]))
            for i in range(len(self.relations)):
                line_x = []
                line_y = []
                line_x.append(self.relations[i][0][0])
                line_y.append(self.relations[i][0][1])
                line_x.append(self.relations[i][0][0])
                line_y.append(self.relations[i][0][1])
                for k in range(1,4):
                    line_x.pop()
                    line_y.pop()
                    line_x.append(self.relations[i][k][0])
                    line_y.append(self.relations[i][k][1])
                    plt.plot(line_x,line_y,)
        plt.show()



B = Dungeon(randint(1,10),randint(1, 10))
B.CoordsGen()
B.RoomListGen()
B.LinkGen()
B.ShowStats()
B.Show_Dungeon()