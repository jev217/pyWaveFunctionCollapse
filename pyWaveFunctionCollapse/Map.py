from chunk import Chunk, WFCError
from pattern import Pattern
from PIL import Image, ImageChops
import random
from collections import Counter

UP = (0, -1)
UP_RIGHT = (1, -1)
UP_LEFT = (-1, -1)
DOWN = (0, 1)
DOWN_RIGHT = (1, 1)
DOWN_LEFT = (-1, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
dirs = [UP, DOWN, LEFT, RIGHT, UP_RIGHT, UP_LEFT, DOWN_LEFT, DOWN_RIGHT]

BLANK_TILE = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

def addCoords(coord1, coord2):
    return (coord1[0] + coord2[0], coord1[1] + coord2[1])

def trim(im):
    bg = Image.new(im.mode, im.size, im.getpixel((0,0)))
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)

class MapError(Exception):
    pass

class BadPatternError(Exception):
    pass

class OutputShapeSize(Exception):
    pass

class Map(object):
    def __init__(self, pattern, outputImageName="output.png", tileSize:tuple=(16, 16), chunkSize:tuple=(16, 16), mapSize:tuple=(16, 16), outputShape:list=None):
        self.patternSTR = pattern
        self.pattern = Pattern(pattern, tileSize)
        self.tileSizeX, self.tileSizeY = tileSize
        self.chunkSizeX, self.chunkSizeY = chunkSize
        if outputShape == None:
            self.mapSizeX, self.mapSizeY = mapSize
        else:
            self.mapSizeX, self.mapSizeY = (len(outputShape[0]), len(outputShape))
        self.outputImageName = outputImageName
        self.map = {}
        if outputShape == None:
            for y in range(self.mapSizeY):
                for x in range(self.mapSizeX):
                    self.map[(x, y)] = 0
        else:
            for y in range(len(outputShape)):
                for x in range(len(outputShape[0])):
                    if outputShape[y][x] == 1:
                        self.map[(x, y)] = 0

    def addCoord(self, coord1, coord2):
        return (coord1[0]+coord2[0], coord1[1]+coord2[1])

    def is_generated(self):
        if any(self.map[coord] == 0 for coord in self.map.keys()):
            return False
        return True

    def getNeighbors(self, coord):
        neighbors = {}
        for dir in [UP, DOWN, LEFT, RIGHT]:
            neighborCoord = self.addCoord(coord, dir)
            if neighborCoord in self.map.keys():
                neighbors[neighborCoord] = dir
        return neighbors

    def generate_chunk(self, chunkNeighborTiles=None):
        generating = True
        retryCount = 0
        while generating:
            if retryCount > 125:
                raise MapError("Too many retries and can't solve next chunk.")
            try:
                if chunkNeighborTiles == None:
                    chunk = Chunk(self.pattern, tileSize=(self.tileSizeX, self.tileSizeY), chunkSize=(self.chunkSizeX, self.chunkSizeY))
                else:
                    chunk = Chunk(self.pattern, tileSize=(self.tileSizeX, self.tileSizeY), chunkSize=(self.chunkSizeX, self.chunkSizeY), chunkNeighbors=chunkNeighborTiles)
                chunk.collapse()
                generating = False
            except WFCError:
                retryCount += 1
                pass
        return chunk

    def generate_map_image(self):
        outputImage = Image.new("RGBA", ((self.chunkSizeX * self.tileSizeX) * self.mapSizeX, (self.chunkSizeY * self.tileSizeY) * self.mapSizeY))
        for coord, chunk in self.map.items():
            if self.map[coord] != 0:
                chunkImage = self.map[coord].get_chunk_image()
                outputImage.paste(chunkImage, ((self.chunkSizeX * self.tileSizeX) * coord[0], (self.chunkSizeY * self.tileSizeY) * coord[1]))
        return outputImage

    def showMap(self):
        outputImage = self.generate_map_image()
        outputImage.show()

    def saveMap(self):
        self.generate_crosshatching()

    def getMap(self):
        outputImage = self.generate_map_image()
        return outputImage

    def invertOffset(self, offset):
        return (-offset[0], -offset[1])

    def generate_crosshatching(self, mapImage=None):
        if mapImage == None:
            outputMap = Pattern(self.getMap(), tileSize=(self.tileSizeX, self.tileSizeY))
        else:
            outputMap = Pattern(mapImage, tileSize=(self.tileSizeX, self.tileSizeY))
        generatedMap = {}
        for y in range(outputMap.numTilesY):
            for x in range(outputMap.numTilesX):
                generatedMap[(x, y)] = outputMap.getTile((x, y))

        def getNeighbors(coord):
            neighbors = {}
            for dir in dirs:
                neighborCoord = self.addCoord(coord, dir)
                if neighborCoord in generatedMap.keys():
                    neighbors[neighborCoord] = dir
            return neighbors

        def random_pattern(patterns):
            occurances = {}
            for pattern in patterns:
                patternOccurance = self.pattern.patternOccurances[pattern]
                if patternOccurance not in occurances:
                    occurances[patternOccurance] = []
                occurances[patternOccurance].append(pattern)
            return random.choice(occurances[max(occurances.keys())])

        def save_generatedImage():
            generatedImage = Image.new("RGBA", (self.tileSizeX * outputMap.numTilesX, self.tileSizeY * outputMap.numTilesY))
            for coord, tile in generatedMap.items():
                tile = Image.frombytes("RGBA", (self.tileSizeX, self.tileSizeY), tile)
                generatedImage.paste(tile, (coord[0] * self.tileSizeX, coord[1] * self.tileSizeY))
            generatedImage = generatedImage.crop(generatedImage.getbbox())
            generatedImage.save(self.outputImageName)

        def show_generatedImage():
            generatedImage = Image.new("RGBA", (self.tileSizeX * outputMap.numTilesX, self.tileSizeY * outputMap.numTilesY))
            for coord, tile in generatedMap.items():
                tile = Image.frombytes("RGBA", (self.tileSizeX, self.tileSizeY), tile)
                generatedImage.paste(tile, (coord[0] * self.tileSizeX, coord[1] * self.tileSizeY))
            generatedImage.show()

        def find_most_common_intersects(arrays):
            all_values = [val for sublist in arrays for val in sublist]
            count = Counter(all_values)
            most_common = count.most_common()
            common_in_all = []

            for val, freq in most_common:
                if all(val in sublist for sublist in arrays):
                    common_in_all.append(val)

            if common_in_all:
                return common_in_all
            else:
                commonVals = []
                freq = list(set([freq for val, freq in most_common]))
                for val, valFreq in most_common:
                    if valFreq == max(freq):
                        commonVals.append(val)
                standOutArrays = []
                for array in arrays:
                    for commonVal in commonVals:
                        if commonVal not in array and array not in standOutArrays:
                            standOutArrays.append(array)
                return commonVals, standOutArrays

        emptyTiles = []
        for coord, tile in generatedMap.items():
            if tile == BLANK_TILE and any(generatedMap[neighborCoord] != BLANK_TILE for neighborCoord in getNeighbors(coord).keys()):
                emptyTiles.append(coord)
        noNeighbors = []
        for coord in emptyTiles:
            coordNeighbors = getNeighbors(coord)
            possiblePatterns = []
            if all(generatedMap[neighborCoord] == BLANK_TILE for neighborCoord in coordNeighbors.keys()):
                noNeighbors.append(coord)
                continue
            for neighborCoord, dir in coordNeighbors.items():
                if generatedMap[neighborCoord] != BLANK_TILE:
                    possiblePatterns.append(self.pattern.patternDB[generatedMap[neighborCoord]][self.invertOffset(dir)])
            possiblePatterns = set.intersection(*map(set, possiblePatterns))
            if possiblePatterns != set():
                generatedMap[coord] = random_pattern(possiblePatterns)
            else:
                noNeighbors.append(coord)
        show_generatedImage()
        for coord in noNeighbors:
            coordNeighbors = getNeighbors(coord)
            possiblePatterns = []
            for neighborCoord, dir in coordNeighbors.items():
                if generatedMap[neighborCoord] != BLANK_TILE:
                    possiblePatterns.append(self.pattern.patternDB[generatedMap[neighborCoord]][self.invertOffset(dir)])
            if set.intersection(*map(set, possiblePatterns)) != set():
                possiblePatterns = set.intersection(*map(set, possiblePatterns))
                generatedMap[coord] = random_pattern(possiblePatterns)
            else:
                possiblePatterns = find_most_common_intersects(possiblePatterns)
                generatedMap[coord] = random.choice(possiblePatterns[0])
        save_generatedImage()

    def generate_map(self):
        currentY = 0
        retryCount = 0
        while not self.is_generated():
            try:
                for x in range(self.mapSizeX):
                    coord = (x, currentY)
                    if coord in self.map.keys():
                        print("Generating chunk at {}".format(coord))
                        coordNeighbors = self.getNeighbors(coord)
                        chunkNeighborTiles = {}
                        for neighborCoord, dir in coordNeighbors.items():
                            if neighborCoord in self.map.keys() and self.map[neighborCoord] != 0:
                                for chunkCoord, chunkTile in self.map[neighborCoord].get_edge_tiles(self.invertOffset(dir)).items():
                                    chunkNeighborTiles[chunkCoord] = chunkTile
                        if chunkNeighborTiles == {}:
                            self.map[coord] = self.generate_chunk()
                            retryCount -= 1
                        else:
                            self.map[coord] = self.generate_chunk(chunkNeighborTiles=chunkNeighborTiles)
                        retryCount -= 1
                currentY += 1
            except MapError:
                if retryCount > 5:
                    raise BadPatternError("Pattern is too complex or large to generate map.")
                retryCount += 1
                if currentY > 0:
                    for x in range(self.mapSizeX):
                        coord = (x, currentY)
                        if coord in self.map.keys():
                            self.map[coord] = 0
                    currentY -= 1
                else:
                    for coord in self.map.keys():
                        self.map[coord] = 0
                    currentY = 0
        print("Map generated!")
