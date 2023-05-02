# pyWaveFunctionCollapse
My (arguably bad) implementation of WFC in Python to output images based off a few parameters and input images.  This might not align exactly with WFC but it's as best as I can understand it.  If you see how this can be improved please feel free to make the change as I've been attempting to make this as good as I can.

## Usage
The program can be used a few different ways, either generating a whole map or seperate chunks if needed.

This can generate in a few methods, if you'd like to generate a larger image based off a smaller images or called "chunks", you can use the following:
```python
from pyWaveFunctionCollapse.Map import Map

game_map = Map("path/to/image.png", outputImageName="path/to/output.png", tileSize=(16, 16), chunkSize=(16, 16), mapSize=(16, 16))
game_map.generate_map()
game_map.saveMap()
```
You can also generate a custom shape to be made out of the smaller "chunks" like the below code, please note that when giving a custom shape the "mapSize" parameter is ignored/overridden.
```python
from pyWaveFunctionCollapse.Map import Map

outputShape = [[0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
               [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
               [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
               [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
               [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
               [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
               [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
               [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
               [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
               [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0]]


gamemap = Map("D:\\Python Projects\\pyWaveFunctionCollapse\\texture\\mountTemplateStructure3.png", tileSize=(16, 16), chunkSize=(8, 8), outputShape=outputShape)
gamemap.generate_map()
gamemap.saveMap()
```

You can also generate seperate chunks without needing to do the whole map incase you want something smaller and more precise:
```python
from pyWaveFunctionCollapse.chunk import Chunk

chunk = Chunk("path/to/image.png", outputImageName="path/to/output.png", tileSize=(16, 16), chunkSize=(16, 16))
chunk.collapse()
chunk.save_chunk_image()
```