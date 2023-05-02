from pattern import Pattern
import random
import numpy as np
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

class WFCCollapseError(Exception):
    pass

class WFCError(Exception):
    pass

class Chunk(object):
    def __init__(self, image, tileSize:tuple=(16, 16), chunkSize:tuple=(16,16), chunkNeighbors=None):
        if type(image) == str:
            self.pattern = Pattern(image, tileSize)
        else:
            self.pattern = image
        self.patternDB = self.pattern.patternDB
        self.chunkOutputSizeX, self.chunkOutputSizeY = chunkSize
        self.chunkSizeX, self.chunkSizeY = self.addCoords(chunkSize, (1, 1))
        self.tileSizeX, self.tileSizeY = tileSize
        self.chunkEdges = {}
        self.chunk = {}
        for y in range(self.chunkSizeY):
            for x in range(self.chunkSizeX):
                self.chunk[(x, y)] = list(self.patternDB.keys())
        if chunkNeighbors is not None:
            for coord in chunkNeighbors.keys():
                self.chunk[coord] = [chunkNeighbors[coord]]

    def getNeighbors(self, coord):
        neighbors = {}
        for dir in dirs:
            neighborCoord = addCoords(coord, dir)
            if neighborCoord in self.chunk:
                neighbors[neighborCoord] = dir
        return neighbors

    def invertOffset(self, dir):
        return (-dir[0], -dir[1])

    def addCoords(self, coord1, coord2):
        return (coord1[0] + coord2[0], coord1[1] + coord2[1])

    def minusCoords(self, coord1, coord2):
        return (coord1[0] - coord2[0], coord1[1] - coord2[1])

    def propagate(self, coord):
        currentPattern = self.chunk[coord][0]
        currentNeighbors = self.getNeighbors(coord)
        for currentNeighborCoord, currentToNeighborOffset in currentNeighbors.items():
            currentNeighborPatterns = self.chunk[currentNeighborCoord]
            for currentNeighborPattern in currentNeighborPatterns:
                if currentNeighborPattern not in self.patternDB[currentPattern][currentToNeighborOffset]:
                    self.chunk[currentNeighborCoord].remove(currentNeighborPattern)
                    if len(self.chunk[currentNeighborCoord]) == 0:
                        raise WFCError
        for coord, coordPatterns in self.chunk.items():
            coordPatternsDB = {}
            for coordPattern in coordPatterns:
                coordPatternOffsets = self.patternDB[coordPattern]
                for coordPatternOffset in coordPatternOffsets.keys():
                    if coordPatternOffset not in coordPatternsDB.keys():
                        coordPatternsDB[coordPatternOffset] = []
                    for pattern in coordPatternOffsets[coordPatternOffset]:
                        coordPatternsDB[coordPatternOffset].append(pattern)
            coordNeighbors = self.getNeighbors(coord)
            for neighborCoord, coordToNeighborOffset in coordNeighbors.items():
                if len(self.chunk[neighborCoord]) == 1:
                    continue
                neighborPatterns = self.chunk[neighborCoord]
                for neighborPattern in neighborPatterns:
                    try:
                        if neighborPattern not in coordPatternsDB[coordToNeighborOffset]:
                            self.chunk[neighborCoord].remove(neighborPattern)
                            if len(self.chunk[neighborCoord]) == 0:
                                raise WFCError
                    except KeyError:
                        pass

    def getIncorrectPatterns(self):
        incorrectCoords = []
        for coord in self.chunk.keys():
            coordNeighbors = self.getNeighbors(coord)
            coordPattern = self.chunk[coord][0]
            for coordNeighborCoord, coordToNeighborOffset in coordNeighbors.items():
                coordNeighborPatterns = self.chunk[coordNeighborCoord][0]
                if coordNeighborPatterns not in self.patternDB[coordPattern][coordToNeighborOffset] and coord not in incorrectCoords:
                    incorrectCoords.append(coord)
        return incorrectCoords

    def isCollapsed(self):
        if any(len(self.chunk[coord]) > 1 for coord in self.chunk.keys()):
            return False
        return True

    def collapseRemaining(self):
        count = 0
        for coord in self.chunk.keys():
            if len(self.chunk[coord]) > 1:
                count += 1
        return count

    def amountCollapsed(self):
        count = 0
        for coord in self.chunk.keys():
            if len(self.chunk[coord]) == 1:
                count += 1
        return count

    def getLowestEntropy(self):
        entropies = {}
        for coord in self.chunk.keys():
            if len(self.chunk[coord]) > 1:
                if len(self.chunk[coord]) not in entropies:
                    entropies[len(self.chunk[coord])] = []
                entropies[len(self.chunk[coord])].append(coord)
        return random.choice(entropies[min(entropies.keys())])

    def random_pattern(self, coord):
        patterns = self.chunk[coord]
        occurances = {}
        for pattern in patterns:
            patternOccurance = self.pattern.patternOccurances[pattern]
            if patternOccurance not in occurances:
                occurances[patternOccurance] = []
            occurances[patternOccurance].append(pattern)
        return [random.choice(occurances[max(occurances.keys())])]

    def collapse(self):
        startCoord = random.choice(list(self.chunk.keys()))
        self.chunk[startCoord] = [random.choice(self.chunk[startCoord])]
        self.propagate(startCoord)
        while not self.isCollapsed():
            #print(self.collapseRemaining(), self.amountCollapsed())
            nextCoord = self.getLowestEntropy()
            self.chunk[nextCoord] = self.random_pattern(nextCoord)
            self.propagate(startCoord)
        incorrectTiles = self.getIncorrectPatterns()
        incorrectCounts = []
        while len(incorrectTiles) > 0:
            incorrectCounts.append(len(incorrectTiles))
            #print("Incorrect tiles: {}".format(len(incorrectTiles)))
            if incorrectCounts.count(len(incorrectTiles)) > 5:
                raise WFCError("Chunk has no solution")
            for coord in incorrectTiles:
                neighbors = self.getNeighbors(coord)
                potentialPatterns = []
                for neighborCoord in neighbors.keys():
                    neighborPattern = self.chunk[neighborCoord][0]
                    potentialPatterns.append(self.patternDB[neighborPattern][self.invertOffset(neighbors[neighborCoord])])
                potentialPatterns = set.intersection(*map(set, potentialPatterns))
                potentialPatternOccurances = {}
                for potentialPattern in potentialPatterns:
                    potentialPatternOccurances[self.pattern.patternOccurances[potentialPattern]] = potentialPattern
                try:
                    self.chunk[coord] = [potentialPatternOccurances[max(potentialPatternOccurances.keys())]]
                except ValueError:
                    pass
            incorrectTiles = self.getIncorrectPatterns()

        edgeOutputs = {}
        for dir in [UP, DOWN, LEFT, RIGHT]:
            edgeOutputs[dir] = {}
        chunkOutputs = {}
        for coord in self.chunk.keys():
            chunkPattern = self.chunk[coord][0]
            if coord[0] > 0 and coord[0] < self.chunkOutputSizeX and coord[1] > 0 and coord[1] < self.chunkOutputSizeY:
                chunkOutputs[self.minusCoords(coord, (1,1))] = chunkPattern
            elif coord not in [(0, 0), (1, 0), (0,1), (0, self.chunkSizeY-1), (1, self.chunkSizeY-1), (0, self.chunkSizeY-2), (self.chunkSizeX-1, 0), (self.chunkSizeX-1, 1), (self.chunkSizeX-2, 0), (self.chunkSizeX-1, self.chunkSizeY-1), (self.chunkSizeX-2, self.chunkSizeY-1), (self.chunkSizeX-1, self.chunkSizeY-2)]:
                coord = list(coord)
                if coord[0] == 0:
                    edgeDir = LEFT
                    coord[0] = self.chunkOutputSizeX-1
                elif coord[0] == self.chunkSizeX-1:
                    edgeDir = RIGHT
                    coord[0] = 0
                elif coord[1] == 0:
                    edgeDir = UP
                    coord[1] = self.chunkOutputSizeY-1
                elif coord[1] == self.chunkSizeY-1:
                    edgeDir = DOWN
                    coord[1] = 0
                coord = tuple(coord)
                if coord not in edgeOutputs[edgeDir]:
                    edgeOutputs[edgeDir][coord] = chunkPattern

        self.chunk = chunkOutputs
        self.chunkEdges = edgeOutputs

    def get_edge_tiles(self, dir):
        return self.chunkEdges[dir]

    def get_chunk_image(self):
        chunkImage = Image.new("RGBA", (self.chunkOutputSizeX*self.tileSizeX, self.chunkOutputSizeY*self.tileSizeY))
        for coord in self.chunk.keys():
            chunkImage.paste(Image.frombytes("RGBA", (self.tileSizeX, self.tileSizeY), self.chunk[coord]), (coord[0]*self.tileSizeX, coord[1]*self.tileSizeY))
        return chunkImage

    def showChunk(self):
        chunkImage = Image.new("RGBA", (self.chunkOutputSizeX*self.tileSizeX, self.chunkOutputSizeY*self.tileSizeY))
        for coord in self.chunk.keys():
            try:
                chunkImage.paste(Image.frombytes("RGBA", (self.tileSizeX, self.tileSizeY), self.chunk[coord]), (coord[0]*self.tileSizeX, coord[1]*self.tileSizeY))
            except TypeError:
                chunkImage.paste(Image.frombytes("RGBA", (self.tileSizeX, self.tileSizeY), self.chunk[coord][0]), (coord[0]*self.tileSizeX, coord[1]*self.tileSizeY))
        chunkImage.show()