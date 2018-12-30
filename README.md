# Min.AI
This version of Minesweeper is based on the classic computer game. You can easily find out the details of the game from the web, for example: https:// en.wikipedia.org/wiki/Minesweeper_(video_game) However, there are a few differences designed to better evaluate your agent which will become apparent as you play with and familiarize yourself with the game. In Minesweeper, you are given a board that is set up as a 2D grid of tiles. Each tile covers either: (1) a hint number ( that tells how many mines are around that tile ) or (2) a mine. Ultimately, your agent’s goal is to uncover all tiles which do not contain a mine. A more concrete definition of the game is given by the following PEAS description.

**Performance Measure**
-  The performance measure of your agent will be a score calculated based on number of worlds your agent has completed. Points are awarded to your agent only if it successfully solves the entire world. Each difficulty has different weight. 
-  The game ends when your agent chooses to leave the game or if your agent uncovers a mine. In either of these cases you'll get a zero. 

**Environment**
- Each difficulty has a different dimension and number of mines: 
    * Beginner: 8 row x 8 column with 10 mines
    * Intermediate: 16x16 with 40 mines
    * Expert: 16x30 with 99 mines
- The board begins with 1 random tile already uncovered and presumably safe 
- Mines are randomly placed throughout the board.
- Your agent dies when it uncovers a mine.

**Actuators**
- Your agent has 4 moves:
 * (1) The action UNCOVER reveals a covered tile.
 * (2) The action FLAG places a flag on a tile.
 * (3) The action UNFLAG removes a flag from a tile if that tile has a flag. ○ (4) The action LEAVE ends the game immediately.
- The actions UNCOVER, FLAG, and UNFLAG are to be coupled with a pair of coordinates which allows the agent to act on a single tile. 

**Sensors**
- Your agent will receive only one percept:
   * Following an UNCOVER action, your argent will perceive the hint number associated with the previous UNCOVER action. This number represents how many mines are within that tile’s immediate neighbors. 
   * Following a FLAG or UNFLAG action, your agent will perceive -1. 
