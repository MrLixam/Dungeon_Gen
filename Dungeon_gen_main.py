from random import randint


class Entity:
    def __init__(self, Etype: int, pos: tuple, Ename: str):
        self.Etype = Etype
        self.status = ''
        self.health = None
        self.modifiers = []
        self.position = pos
        self.Ename = Ename

    def ShowStats(self):
        print('Name: ')
        print('Type: ', self.Etype)
        print('Status: ', self.status)
        print('Health: ', self.health)
        print('Buffs/Debuffs: ', self.modifiers)
        
    def MoveEntity(self, newpos: tuple):
        '''
        Used to move an entity
        newpos: tuple
            the new position of the entity
        Returns
        None
        '''
        assert len(newpos) == 2; raise "ErrorCode: invalid_coordinates_format"
        assert newpos[0] <= 10 or newpos[0] >= 0; raise "ErrorCode: invalid_x_coordinates" 
        assert newpos[1] <= 10 or newpos[1] >= 0; raise "ErrorCode: invalid_y_coordinates"
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
        print('Type de la pièce: ', self.rtype)
        print('Position dans le donjon: ', self.position)
        print('Entités presentes dans la pièce: ', self.contents)
        print('Numero de la pièce: ', self.name)

    def AddDoor(self, ori: str):
        '''
        Allows the addition of a door, useful for the generation process
        ori : str
            which side is the door on.
        '''
        listValid = ['S', 'N', 'O', 'E']
        assert ori.type == str
        if listValid.count(ori) == 0:
            print('Orientation de la porte non valide')
            print('Orientations possibles:', str(listValid))
            raise "ErrorCode: invalid_door_placement"
        else:
            name = 'Door ' + ori
            if ori == 'S':
                Door = Entity(0, (0, 5), name)
            elif ori == 'N':
                Door = Entity(0, (10, 5), name)
            elif ori == 'O':
                Door = Entity(0, (5, 0), name)
            else:
                Door = Entity(0, (5, 10), name)
            self.contents.append(Door)

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
        assert etype <= 0; raise "ErrorCode: invalid_entity_type"
        assert pos[0] <= 10 or pos[0] >= 0; raise "ErrorCode: invalid_x_coordinate"
        assert pos[1] <= 10 or pos[1] >= 0; raise "ErrorCode: invalid_y_coordinate"
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
        self.NumberRooms = randint(1+size, 5+size+diff)
        self.rooms = []
        self.RoomGenDone = False

    def ShowStats(self):
        print('Nombre de pièces: ', self.NumberRooms)
        print('Difficulté: ', self.Ddiff)
        print('Liste des pièces présentes dans le dongeon: ')
        for i in range(len(self.rooms)):
            self.rooms[i].ShowStats()

    def RoomListGen(self):
        '''
        Generates the list of all the rooms of the Dungeon, stored in self.rooms
        Used for MapGen

        Returns
        -------
        None.

        '''
        if self.RoomGenDone == False:
            for i in range(self.NumberRooms):
                roomX = Room(randint(0, 6), (None, None), str("Room " + str(i + 1)))
                self.rooms.append(roomX)
        self.RoomGenDone = True

    def MapGen(self):
        pass
    
    
    
    
B = Dungeon(5,5)