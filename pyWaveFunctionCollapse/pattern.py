from PIL import Image

UP = (0, -1)
UP_RIGHT = (1, -1)
UP_LEFT = (-1, -1)
DOWN = (0, 1)
DOWN_RIGHT = (1, 1)
DOWN_LEFT = (-1, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
dirs = [UP, DOWN, LEFT, RIGHT, UP_RIGHT, UP_LEFT, DOWN_LEFT, DOWN_RIGHT]

def addCoords(coord1, coord2):
    return (coord1[0] + coord2[0], coord1[1] + coord2[1])

class Pattern(object):
    def __init__(self, image, tileSize=(16, 16)):
        if type(image) == str:
            self.image = Image.open(image).convert("RGBA")
        else:
            self.image = image.convert("RGBA")
        self.tileSizeX, self.tileSizeY = tileSize
        self.width, self.height = self.image.size
        self.numTilesX = self.width // self.tileSizeX
        self.numTilesY = self.height // self.tileSizeY
        self.patternCount = 0
        self.patternOccurances = {}
        self.patternDB = {}
        for y in range(self.numTilesY):
            for x in range(self.numTilesX):
                tile = self.getTile((x, y))
                if tile not in self.patternDB:
                    self.patternDB[tile] = {}
                    self.patternCount += 1
                if tile not in self.patternOccurances:
                    self.patternOccurances[tile] = 0
                self.patternOccurances[tile] += 1
                neighbors = self.getNeighborTiles((x, y))
                for dir in dirs:
                    if dir not in self.patternDB[tile]:
                        self.patternDB[tile][dir] = []
                    for neighbor in neighbors[dir]:
                        if neighbor not in self.patternDB[tile][dir]:
                            self.patternDB[tile][dir].append(neighbor)
        for pattern in self.patternOccurances.keys():
            self.patternOccurances[pattern] /= self.patternCount

    def getTile(self, coord):
        x, y = coord
        return self.image.crop((self.tileSizeX*x, self.tileSizeY*y, self.tileSizeX+(self.tileSizeX*x), self.tileSizeY+(self.tileSizeY*y))).tobytes()

    def showTile(self, coord):
        self.getTile(coord).show()

    def getNeighborTiles(self, coord):
        neighbors = {}
        for dir in dirs:
            neighbors[dir] = []
            neighborCoord = addCoords(coord, dir)
            if neighborCoord[0] >= 0 and neighborCoord[0] < self.numTilesX and neighborCoord[1] >= 0 and neighborCoord[1] < self.numTilesY:
                neighoborTile = self.getTile(neighborCoord)
                if neighoborTile not in neighbors[dir]:
                    neighbors[dir].append(self.getTile(neighborCoord))
        return neighbors