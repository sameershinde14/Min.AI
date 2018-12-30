# ==============================CS-199==================================
# FILE:			MyAI.py
#
# AUTHOR: 		Justin Chung
#
# DESCRIPTION:	This file contains the MyAI class. You will implement your
#				agent in this file. You will write the 'getAction' function,
#				the constructor, and any additional helper functions.
#
# NOTES: 		- MyAI inherits from the abstract AI class in AI.py.
#
#				- DO NOT MAKE CHANGES TO THIS FILE.
# ==============================CS-199==================================

from AI import AI
from Action import Action
import random


class TileInfo:
    def __init__(self, numbr, _uncover):
        self.number = numbr
        self.uncover = _uncover
        self.voteNumber = 0


class MyAI(AI):

    def __init__(self, rowDimension, colDimension, totalMines, startX, startY):
        self.rows = colDimension
        self.cols = rowDimension
        self.totalMines = totalMines
        self.minesLeft = totalMines
        self.prev_x = startX
        self.prev_y = startY
        self.Tiles = [[TileInfo(-10, False) for j in range(self.cols)] for i in range(self.rows)]
        self.queue = []
        self.voteq = []
        self.debug = False
        self.uncoverCount = 0

    def getAction(self, number: int) -> "Action Object":
        newx, newy = self.prev_x, self.prev_y
        (self.Tiles[newx][newy]).number = number
        (self.Tiles[newx][newy]).uncover = True
        self.uncoverCount += 1

        top_left = (newx - 1, newy + 1)
        top_right = (newx + 1, newy + 1)
        top = (newx, newy + 1)
        left = (newx - 1, newy)
        right = (newx + 1, newy)
        bt_left = (newx - 1, newy - 1)
        bt = (newx, newy - 1)
        bt_right = (newx + 1, newy - 1)
        listof = [top, top_left, top_right, left, right, bt, bt_left, bt_right];

        if number == 0:
            for move in listof:
                if 0 <= move[0] < self.rows and 0 <= move[1] < self.cols:
                    self.Tiles[move[0]][move[1]].voteNumber = -1
        elif number > 0:
            for move in listof:
                if 0 <= move[0] < self.rows and 0 <= move[1] < self.cols and self.Tiles[move[0]][move[1]].voteNumber!=-1:
                    self.Tiles[move[0]][move[1]].voteNumber += 1

        if number == -1:
            self.minesLeft -= 1
            for move in listof:
                if 0 <= move[0] < self.rows and 0 <= move[1] < self.cols:
                    if self.Tiles[move[0]][move[1]].number > 0:
                        self.Tiles[move[0]][move[1]].number -= 1
        elif number > 0:
            for move in listof:
                if 0 <= move[0] < self.rows and 0 <= move[1] < self.cols:
                    if self.Tiles[move[0]][move[1]].number == -1:
                        self.Tiles[newx][newy].number -= 1

        queue2 = []
        if number == 0:
            for x1 in range(newx - 1, newx + 2):
                for y1 in range(newy - 1, newy + 2):
                    if 0 <= x1 < self.rows and 0 <= y1 < self.cols:
                        if x1 == newx and y1 == newy:
                            continue
                        queue2.append([x1, y1, AI.Action.UNCOVER])
        """
		if number == 1:
			for x in range(newx-2, newx+3):
				queue2.append([x, newy-2])
				queue2.append([x, newy + 2])
			queue2.extend([[newx-2, newy-1], [newx-2, newy], [newx-2, newy+1], [newx+2, newy-1],[newx+2, newy], [newx+2, newy+1]]);
		"""
        queue3 = []
        for c in queue2:
            if self.rows > c[0] >= 0 and self.cols > c[1] >= 0 and not (self.Tiles[c[0]][c[1]]).uncover:
                queue3.append(c);

        for a in queue3:
            found = False
            for item in self.queue:
                if (a[0] == item[0] and a[1] == item[1]):
                    found = True
                    break;
            if not found:
                self.queue.append(a);

        # print(" ; ".join(str(i) for i in self.queue))
        if self.debug:
            self.printBoard();
        action = -10
        inval = 0
        while action == -10 and inval < 10:
            action = self.getNextAct(action)
            inval += 1
        if (action == -10):
            cnt, ctb = 0, 0
            nx, ny, nnx, nny = -1, -1, -1, -1
            for x in range(self.rows):
                for y in range(self.cols):
                    if self.Tiles[x][y].number == -1:
                        ctb += 1
                        nnx, nny = x, y
                    if self.Tiles[x][y].number == -10:
                        cnt += 1
                        nx, ny = x, y
            if cnt == 1:
                self.prev_x = nx
                self.prev_y = ny
                action = AI.Action.UNCOVER if ctb == self.totalMines else AI.Action.FLAG
                if self.debug:
                    print(action, self.prev_x,self.prev_y,"\n")
                return Action(action, nx, ny);
            if cnt == 0:
                self.prev_x = nnx
                self.prev_y = nny
                action = AI.Action.UNCOVER
                if self.debug:
                    print(action, self.prev_x, self.prev_y, "\n")
                return Action(AI.Action.UNCOVER, nnx, nny)

        portion = 2/3
        if self.rows == 30:
            portion = 4/5
        if(action == -10 and self.uncoverCount > (portion * self.rows*self.cols)):
            if not self.Tiles[self.rows-1][self.cols-1].uncover:
                self.prev_x = self.rows-1
                self.prev_y = self.cols - 1
                action = AI.Action.UNCOVER
            elif not self.Tiles[self.rows-1][0].uncover:
                self.prev_x = self.rows-1
                self.prev_y = 0
                action = AI.Action.UNCOVER
            elif not self.Tiles[0][self.cols-1].uncover:
                self.prev_x = 0
                self.prev_y = self.cols - 1
                action = AI.Action.UNCOVER
            elif not self.Tiles[0][0].uncover:
                self.prev_x = 0
                self.prev_y = 0
                action = AI.Action.UNCOVER

        if (action == -10):
            # add voting mechanism
            self.recalculateVotes()
            a = random.choice(self.voteq)
            self.prev_x = a[0]
            self.prev_y = a[1]
            action = a[2]
        if self.debug:
            print(action, self.prev_x,self.prev_y,"\n")
        return Action(action, self.prev_x, self.prev_y);

    def recalculateVotes(self):
        self.voteq.clear()
        if self.debug:
            self.printVoteBoard()
        max = -100
        min = 100
        xmax, ymax = [], []
        xmin, ymin = [], []
        for a in range(self.rows):
            for b in range(self.cols):
                if self.Tiles[a][b].number != -10 or self.Tiles[a][b].uncover: continue
                if self.Tiles[a][b].voteNumber > max:
                    max = self.Tiles[a][b].voteNumber
                    xmax = [a]
                    ymax = [b]
                elif self.Tiles[a][b].voteNumber == max:
                    xmax.append(a)
                    ymax.append(b)
                if self.Tiles[a][b].voteNumber ==0:
                    continue
                if self.Tiles[a][b].voteNumber < min :
                    min = self.Tiles[a][b].voteNumber
                    xmin = [a]
                    ymin = [b]
                elif self.Tiles[a][b].voteNumber == min:
                    xmin.append(a)
                    ymin.append(b)
        for i in range(len(xmax)):
            self.voteq.append([xmax[i], ymax[i], AI.Action.FLAG])
            break;

    def printBoard(self):
        print("\n")
        for i in range(self.rows):
            print("\t".join([str(x.number) for x in self.Tiles[i]]))
        print("\n")

    def printVoteBoard(self):
        print("\n")
        for i in range(self.rows):
            vb = [str(x.voteNumber) for x in self.Tiles[i]]
            vb = [str(t) if self.Tiles[i][j].number == -10 else str(-1) for j, t in enumerate(vb)]
            print("\t".join(vb))
        print("\n")

    def getNextAct(self, action):
        if (len(self.queue) and action == -10):
            a = self.queue.pop(0)
            self.prev_x = a[0]
            self.prev_y = a[1]
            if self.Tiles[a[0]][a[1]].uncover:
                action = -10
            else:
                action = a[2]
        if action == -10 and len(self.queue) == 0:
            self.fillqueue()
            queue3 = []
            for c in self.queue:
                if self.rows > c[0] >= 0 and self.cols > c[1] >= 0 and not (self.Tiles[c[0]][c[1]]).uncover:
                    queue3.append(c)
            self.queue = queue3
            if (len(self.queue)):
                a = self.queue.pop(0);
                self.prev_x = a[0]
                self.prev_y = a[1]
                action = a[2]
        return action;

    def fillqueue(self):
        for y in range(1, self.cols - 1):
            if self.Tiles[self.rows - 2][y].number == -10 or self.Tiles[self.rows - 2][y].number == -1 or \
                    self.Tiles[self.rows - 2][y].number == 0: continue
            self.identifyPatterns(self.rows - 2, y)

        if not self.queue:
            for y in range(1, self.cols - 1):
                if self.Tiles[1][y].number == -10 or self.Tiles[1][y].number == 0 or self.Tiles[1][
                    y].number == -1: continue
                self.identifyPatterns2(1, y)

        if not self.queue:
            for x in range(1, self.rows - 1):
                if self.Tiles[x][1].number == -10 or self.Tiles[x][1].number == 0 or self.Tiles[x][1].number == -1:
                    continue
                self.identifyPatterns4(x, 1)

        if not self.queue:
            for x in range(1, self.rows - 1):
                if self.Tiles[x][self.cols - 2].number == -10 or self.Tiles[x][self.cols - 2].number == 0 or \
                        self.Tiles[x][self.cols - 2].number == -1: continue
                self.identifyPatterns5(x, self.cols - 2)

        if not self.queue:
            for x in range(1, self.rows - 1):
                for y in range(1, self.cols - 1):
                    if self.Tiles[x][y].number == -10 or self.Tiles[x][y].number == 0 or self.Tiles[x][
                        y].number == -1: continue
                    self.identifyPatterns3(x, y)
        if not self.queue:
            for y in range(1, self.cols - 1):
                if self.Tiles[0][y].number == -10 or self.Tiles[0][y].number == 0 or self.Tiles[0][
                    y].number == -1: continue
                # row 0
                if self.Tiles[0][y].number == 1 and [t.uncover for t in self.Tiles[1][y - 1:y + 2]] == [True, True,
                                                                                                        True] and \
                        self.Tiles[0][y - 1].uncover and not self.Tiles[0][y + 1].uncover:
                    self.queue.append([0, y + 1, AI.Action.FLAG])
                elif self.Tiles[0][y].number == 1 and [t.uncover for t in self.Tiles[1][y - 1:y + 2]] == [True, True,
                                                                                                          True] and \
                        self.Tiles[0][y + 1].uncover and not self.Tiles[0][y - 1].uncover:
                    self.queue.append([0, y - 1, AI.Action.FLAG])

            for y in range(1, self.cols - 1):
                g = self.rows - 1
                if self.Tiles[g][y].number == -10 or self.Tiles[g][y].number == 0 or self.Tiles[g][
                    y].number == -1: continue
                if self.Tiles[g][y].number == 1 and [t.uncover for t in self.Tiles[g - 1][y - 1:y + 2]] == [True, True,
                                                                                                            True] and \
                        self.Tiles[g][y - 1].uncover and not self.Tiles[g][y + 1].uncover:
                    self.queue.append([g, y + 1, AI.Action.FLAG])
                elif self.Tiles[g][y].number == 1 and [t.uncover for t in self.Tiles[g - 1][y - 1:y + 2]] == [True,
                                                                                                              True,
                                                                                                              True] and \
                        self.Tiles[g][y + 1].uncover and not self.Tiles[g][y - 1].uncover:
                    self.queue.append([g, y - 1, AI.Action.FLAG])

            for x in range(1, self.rows - 1):
                if self.Tiles[x][0].number == -10 or self.Tiles[0][y].number == 0 or self.Tiles[0][
                    y].number == -1: continue
                # print([t[0].uncover for t in self.Tiles[x - 1:x + 2]])
                # col-0
                if self.Tiles[x][0].number == 1 and [t[0].uncover for t in self.Tiles[x - 1:x + 2]] == [True, True,
                                                                                                        True] and \
                        self.Tiles[x + 1][1].uncover and self.Tiles[x][1].uncover and not self.Tiles[x - 1][1].uncover:
                    self.queue.append([x - 1, 1, AI.Action.FLAG])
                elif self.Tiles[x][0].number == 1 and [t[0].uncover for t in self.Tiles[x - 1:x + 2]] == [True, True,
                                                                                                          True] and \
                        self.Tiles[x - 1][1].uncover and self.Tiles[x][1].uncover and not self.Tiles[x + 1][1].uncover:
                    self.queue.append([x + 1, 1, AI.Action.FLAG])

            for x in range(1, self.rows - 1):
                g = self.cols - 1
                # col-last
                # print([t[g].uncover for t in self.Tiles[x - 1:x + 2]])
                if self.Tiles[x][g].number == 1 and [t[g].uncover for t in self.Tiles[x - 1:x + 2]] == [True, True,
                                                                                                        True] and \
                        self.Tiles[x + 1][g - 1].uncover and self.Tiles[x][g - 1].uncover and not self.Tiles[x - 1][
                    g - 1].uncover:
                    self.queue.append([x - 1, g - 1, AI.Action.FLAG])
                elif self.Tiles[x][g].number == 1 and [t[g].uncover for t in self.Tiles[x - 1:x + 2]] == [True, True,
                                                                                                          True] and \
                        self.Tiles[x - 1][g - 1].uncover and self.Tiles[x][g - 1].uncover and not self.Tiles[x + 1][
                    g - 1].uncover:
                    self.queue.append([x + 1, g - 1, AI.Action.FLAG])
        if not self.queue:
            self.fillqueue2()
        if not self.queue:
            corners = {"tl":[1,1], "tr":[1, self.cols-2], "bl":[self.rows-2, 1], "br":[self.rows-2, self.cols-2]}
            for c in corners.keys():
                self.identifyCornerPatters(c, corners[c][0], corners[c][1]);

    def fillqueue2(self):
        for x1 in range(self.rows):
            for y1 in range(self.cols):
                if self.Tiles[x1][y1].uncover and self.Tiles[x1][y1].number == 0:
                    top_left = (x1 - 1, y1 + 1)
                    top_right = (x1 + 1, y1 + 1)
                    top = (x1, y1 + 1)
                    left = (x1 - 1, y1)
                    right = (x1 + 1, y1)
                    bt_left = (x1 - 1, y1 - 1)
                    bt = (x1, y1 - 1)
                    bt_right = (x1 + 1, y1 - 1)
                    listof = [top, top_left, top_right, left, right, bt, bt_left, bt_right];

                    for move in listof:
                        if 0 <= move[0] < self.rows and 0 <= move[1] < self.cols and self.Tiles[move[0]][
                            move[1]].number == -10 and not self.Tiles[move[0]][move[1]].uncover \
                                and self.Tiles[move[0]][move[1]].number != -1:
                            self.queue.append([move[0], move[1], AI.Action.UNCOVER])

    def identifyCornerPatters(self, corner, x, y):
        if self.minesLeft> 2:
            return
        pat = [[0 for _ in range(3)] for _ in range(3)]
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                pat[i + 1][j + 1] = self.Tiles[x + i][y + j].number
        notuncvr = []
        pat2 = [[False for _ in range(3)] for _ in range(3)]
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                pat2[i + 1][j + 1] = self.Tiles[x + i][y + j].uncover
                if not self.Tiles[x + i][y + j].uncover:
                    notuncvr.append([x + i, y + j])

        if corner=="bl" and pat2==[[True,True,True], [False,False,True], [False,False,True]]:
            if (pat[1][2]==1 or pat[2][2]==1) and (pat[0][0]==1 or pat[0][1]==1) and self.minesLeft==2:
                self.queue.append([x, y-1, AI.Action.FLAG])
                self.queue.append([x+1, y, AI.Action.FLAG])
            else:
                self.queue.append([x, y, AI.Action.FLAG])

        elif corner=="tr" and pat2==[[True,False,False], [True,False,False], [True,True,True]]:
            if (pat[2][1]==1 or pat[2][2]==1) and (pat[0][0]==1 or pat[1][0]==1) and self.minesLeft==2:
                self.queue.append([x-1, y, AI.Action.FLAG])
                self.queue.append([x, y+1, AI.Action.FLAG])
            else:
                self.queue.append([x, y, AI.Action.FLAG])

        elif corner=="br" and pat2==[[True,True,True], [True,False,False], [True,False,False]]:
            if (pat[1][0]==1 or pat[2][0]==1) and (pat[0][1]==1 or pat[0][2]==1) and self.minesLeft==2:
                self.queue.append([x+1, y, AI.Action.FLAG])
                self.queue.append([x, y+1, AI.Action.FLAG])
            else:
                self.queue.append([x, y, AI.Action.FLAG])
        elif corner=="tl" and pat2==[[False,False,True], [False,False,True], [True,True,True]]:
            if (pat[1][2]==1 or pat[0][2]==1) and (pat[2][0]==1 or pat[2][1]==1) and self.minesLeft==2:
                self.queue.append([x+1, y, AI.Action.FLAG])
                self.queue.append([x, y-1, AI.Action.FLAG])
            else:
                self.queue.append([x, y, AI.Action.FLAG])

    def isValidTile(self, a, b):
        return 0<=a<self.rows and 0<=b<self.cols


    def identifyPatterns3(self, x, y):
        pat = [[0 for _ in range(3)] for _ in range(3)]
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                pat[i + 1][j + 1] = self.Tiles[x + i][y + j].number
        notuncvr = []
        pat2 = [[False for _ in range(3)] for _ in range(3)]
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                pat2[i + 1][j + 1] = self.Tiles[x + i][y + j].uncover
                if not self.Tiles[x + i][y + j].uncover:
                    notuncvr.append([x + i, y + j])

        # 1-2-1 pattern
        if pat[1] == [1, 2, 1] and pat2[2] == [True, True, True] and not pat2[0][0] and not pat2[0][2]:
            self.queue.append([x - 1, y - 1, AI.Action.FLAG])
            self.queue.append([x - 1, y + 1, AI.Action.FLAG])

        elif pat[1] == [1, 2, 1] and pat2[0] == [True, True, True] and not pat2[2][0] and not pat2[2][2]:
            self.queue.append([x + 1, y - 1, AI.Action.FLAG])
            self.queue.append([x + 1, y + 1, AI.Action.FLAG])

        elif [t[1] for t in pat] == [1, 2, 1] and [t[0] for t in pat2] == [True, True, True] and not pat2[0][
            2] and not pat2[2][2]:
            self.queue.append([x + 1, y + 1, AI.Action.FLAG])
            self.queue.append([x - 1, y + 1, AI.Action.FLAG])

        elif [t[1] for t in pat] == [1, 2, 1] and [t[2] for t in pat2] == [True, True, True] and not pat2[0][
            0] and not pat2[2][0]:
            self.queue.append([x + 1, y - 1, AI.Action.FLAG])
            self.queue.append([x - 1, y - 1, AI.Action.FLAG])

        #mirror done
        elif pat[1][1]==2 and pat[1][2]==1 and pat2[2] == [True, True, True] and pat2[1][0] and \
                pat2[0]==[False,False,False]:
            self.queue.append([x-1, y-1, AI.Action.FLAG])

        elif pat[1][1]==2 and pat[1][0]==1 and pat2[2] == [True, True, True] and pat2[1][2] and \
                pat2[0]==[False,False,False]:
            self.queue.append([x-1, y+1, AI.Action.FLAG])

        #mirror done
        elif pat[1][1]==2 and pat[2][1]==1 and [t[0] for t in pat2] == [True, True, True] and pat2[0][1] and \
                [t[2] for t in pat2]==[False,False,False]:
            self.queue.append([x-1, y+1, AI.Action.FLAG])

        elif pat[1][1]==2 and pat[0][1]==1 and [t[0] for t in pat2] == [True, True, True] and pat2[2][1] and \
                [t[2] for t in pat2]==[False,False,False]:
            self.queue.append([x+1, y+1, AI.Action.FLAG])

        #mirror done
        elif pat[1][1]==2 and pat[0][1]==1 and [t[2] for t in pat2] == [True, True, True] and pat2[2][1] and \
                [t[0] for t in pat2]==[False,False,False]:
            self.queue.append([x+1, y-1, AI.Action.FLAG])

        elif pat[1][1]==2 and pat[2][1]==1 and [t[2] for t in pat2] == [True, True, True] and pat2[0][1] and \
                [t[0] for t in pat2]==[False,False,False]:
            self.queue.append([x-1, y-1, AI.Action.FLAG])

        elif pat[1][1] == 2 and pat[1][2] == 1 and pat2[0] == [True, True, True] and pat2[1][0] and \
                pat2[2] == [False, False, False]:
            self.queue.append([x + 1, y - 1, AI.Action.FLAG])

        elif pat[1][1] == 2 and pat[1][0] == 1 and pat2[0] == [True, True, True] and pat2[1][2] and \
                pat2[2] == [False, False, False]:
            self.queue.append([x + 1, y + 1, AI.Action.FLAG])


        elif pat[1][1] == 1 and pat[1][2] == 1 and [t[0] for t in pat2]==[True, True, True] and  \
                pat2[2] == [True, True, True] and not pat2[0][1] and not pat2[0][2] and \
                self.isValidTile(x-1, y+2) and not self.Tiles[x-1][y+2].uncover:
            self.queue.append([x - 1, y + 2, AI.Action.UNCOVER])

        elif pat[1][1] == 1 and pat[1][2] == 1 and [t[0] for t in pat2]==[True, True, True] and  \
                pat2[0] == [True, True, True] and not pat2[2][1] and not pat2[2][2] and \
                self.isValidTile(x+1, y+2) and not self.Tiles[x+1][y+2].uncover:
            self.queue.append([x + 1, y + 2, AI.Action.UNCOVER])

        elif pat[1][1] == 1 and pat[2][1] == 1 and [t[0] for t in pat2]==[True, True, True] and  \
                pat2[0] == [True, True, True] and not pat2[1][2] and not pat2[2][2] and \
                self.isValidTile(x+2, y+1) and not self.Tiles[x+2][y+1].uncover:
            self.queue.append([x + 2, y + 1, AI.Action.UNCOVER])

        elif pat[1][1] == 1 and pat[2][1] == 1 and [t[2] for t in pat2]==[True, True, True] and  \
                pat2[0] == [True, True, True] and not pat2[1][0] and not pat2[2][0] and \
                self.isValidTile(x+2, y-1) and not self.Tiles[x+2][y-1].uncover:
            self.queue.append([x + 2, y - 1, AI.Action.UNCOVER])
        ##
        elif pat[1][1] == 1 and pat[1][0] == 1 and [t[2] for t in pat2]==[True, True, True] and  \
                pat2[0] == [True, True, True] and not pat2[2][0] and not pat2[2][1] and \
                self.isValidTile(x+1, y-2) and not self.Tiles[x+1][y-2].uncover:
            self.queue.append([x + 1, y - 2, AI.Action.UNCOVER])

        elif pat[1][1] == 1 and pat[1][0] == 1 and [t[2] for t in pat2] == [True, True, True] and \
                pat2[2] == [True, True, True] and not pat2[0][0] and not pat2[0][1] and \
                self.isValidTile(x - 1, y - 2) and not self.Tiles[x - 1][y - 2].uncover:
            self.queue.append([x - 1, y - 2, AI.Action.UNCOVER])

        elif pat[1][1] == 1 and pat[0][1] == 1 and [t[2] for t in pat2]==[True, True, True] and  \
                pat2[2] == [True, True, True] and not pat2[0][0] and not pat2[1][0] and \
                self.isValidTile(x-2, y-1) and not self.Tiles[x-2][y-1].uncover:
            self.queue.append([x - 2, y - 1, AI.Action.UNCOVER])

        elif pat[1][1] == 1 and pat[0][1] == 1 and [t[0] for t in pat2]==[True, True, True] and  \
                pat2[2] == [True, True, True] and not pat2[0][2] and not pat2[1][2] and \
                self.isValidTile(x-2, y+1) and not self.Tiles[x-2][y+1].uncover:
            self.queue.append([x - 2, y + 1, AI.Action.UNCOVER])

        elif (pat[1][1] == 2 and len(notuncvr) == 2):
            for nuc in notuncvr:
                self.queue.append([nuc[0], nuc[1], AI.Action.FLAG])

        elif (pat[1][1] == 1 and len(notuncvr) == 1):
            for nuc in notuncvr:
                self.queue.append([nuc[0], nuc[1], AI.Action.FLAG])

        elif (pat[1][1] == 3 and len(notuncvr) == 3):
            for nuc in notuncvr:
                self.queue.append([nuc[0], nuc[1], AI.Action.FLAG])

    def identifyPatterns(self, x, y):
        pat = [[0 for _ in range(3)] for _ in range(3)]

        # print("\nPattern printing:\n");
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                pat[i + 1][j + 1] = self.Tiles[x + i][y + j].number

        notuncvr = []
        pat2 = [[False for _ in range(3)] for _ in range(3)]
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                pat2[i + 1][j + 1] = self.Tiles[x + i][y + j].uncover
                if not self.Tiles[x + i][y + j].uncover:
                    notuncvr.append([x + i, y + j])

        if (pat[1][1] == 1 and len(notuncvr) == 1):
            for nuc in notuncvr:
                self.queue.append([nuc[0], nuc[1], AI.Action.FLAG])

        elif (pat[1][1] == 2 and len(notuncvr) == 2):
            for nuc in notuncvr:
                self.queue.append([nuc[0], nuc[1], AI.Action.FLAG])

        elif (pat[1][1] == 3 and len(notuncvr) == 3):
            for nuc in notuncvr:
                self.queue.append([nuc[0], nuc[1], AI.Action.FLAG])

        elif (pat[1][1] == 1 and pat[1][0] == -10 and pat[2][1] == 1 and pat[2][0] == -10):
            if not self.Tiles[x - 1][y - 1].uncover:
                self.queue.append([x - 1, y - 1, AI.Action.UNCOVER])

        elif (pat[1][1] == 1 and pat[1][2] == -10 and pat[2][1] == 1 and pat[2][2] == -10):
            if not self.Tiles[x - 1][y + 1].uncover:
                self.queue.append([x - 1, y + 1, AI.Action.UNCOVER])

        elif (pat[1] == [1, 2, 1] and pat2[2] == [False, False, False]):
            self.queue.append([x + 1, y + 1, AI.Action.FLAG])
            self.queue.append([x + 1, y - 1, AI.Action.FLAG])

        elif (pat[1][1] == 2 and pat[1][2] == -10 and pat[2][1] == 2 and pat[2][2] == -10):
            if not self.Tiles[x + 1][y + 1].uncover:
                self.queue.append([x + 1, y + 1, AI.Action.FLAG])
            if not self.Tiles[x - 1][y - 1].uncover:
                self.queue.append([x - 1, y - 1, AI.Action.FLAG])

        elif (pat[1][1] == 2 and pat[1][0] == -10 and pat[2][1] == 2 and pat[2][0] == -10):
            if not self.Tiles[x + 1][y - 1].uncover:
                self.queue.append([x + 1, y - 1, AI.Action.FLAG])
            if not self.Tiles[x][y - 1].uncover:
                self.queue.append([x, y - 1, AI.Action.FLAG])

        elif pat[1] == [1,2,1] and pat2[0] == [False, False, False] and pat2[2] == [True, True, True]:
            self.queue.append([x-1, y-1, AI.Action.FLAG])
            self.queue.append([x - 1, y + 1, AI.Action.FLAG])

        elif (pat[0][1] == 2 and pat[1][1] == 2 and pat[1][2] == -10 and pat[2][1] == 1 and pat[2][2] == -10 and pat[0][
            2] == -10):
            if not self.Tiles[x - 1][y + 1].uncover:
                self.queue.append([x - 1, y + 1, AI.Action.FLAG])

        elif (pat[1][0] == 2 and pat[1][1] == 2 and pat[1][2] == 1 and pat[2][0] == -10 and pat[2][1] == -10 and pat[2][
            2] == 1):
            if not self.Tiles[x + 1][y - 1].uncover:
                self.queue.append([x + 1, y - 1, AI.Action.FLAG])
            if not self.Tiles[x + 1][y].uncover:
                self.queue.append([x + 1, y, AI.Action.FLAG])

        elif (pat[1][1] == 2 and len(notuncvr) == 2):
            for nuc in notuncvr:
                self.queue.append([nuc[0], nuc[1], AI.Action.FLAG])

        elif (pat[1][1] == 1 and len(notuncvr) == 1):
            for nuc in notuncvr:
                self.queue.append([nuc[0], nuc[1], AI.Action.FLAG])

        elif (pat[1][1] == 3 and len(notuncvr) == 3):
            for nuc in notuncvr:
                self.queue.append([nuc[0], nuc[1], AI.Action.FLAG])

        elif (pat[1][0] == 1 and pat[1][1] == 2 and pat[1][2] == 2 and pat[2][0] == 1 and pat[2][1] == -10 and pat[2][
            2] == -10):
            if not self.Tiles[x + 1][y + 1].uncover:
                self.queue.append([x + 1, y + 1, AI.Action.FLAG])
            if not self.Tiles[x + 1][y].uncover:
                self.queue.append([x + 1, y, AI.Action.FLAG])

        elif (pat[1][1] == 2 and pat[1][0] == 1 and pat[2][1] == 1 and pat2[0] == [False, False, False] and not pat2[1][
            2] and not pat2[2][2]):
            self.queue.append([x - 1, y + 1, AI.Action.UNCOVER])

    def identifyPatterns2(self, x, y):

        pat = [[0 for _ in range(3)] for _ in range(3)]
        # print("\nPattern printing:\n");
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if 0 <= x + i < self.rows and 0 <= y + j < self.cols:
                    pat[i + 1][j + 1] = self.Tiles[x + i][y + j].number
        notuncvr = []
        pat2 = [[False for _ in range(3)] for _ in range(3)]
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                pat2[i + 1][j + 1] = self.Tiles[x + i][y + j].uncover
                if not self.Tiles[x + i][y + j].uncover:
                    notuncvr.append([x + i, y + j])

        if [t[0] for t in pat2]==[False,False,False] and [t[2] for t in pat2]==[True, True, True] and [t[1] for t in pat] == [1,2,1]:
            self.queue.append([x-1,y-1,AI.Action.FLAG])
            self.queue.append([x + 1, y - 1, AI.Action.FLAG])

        elif (pat[1][1] == 1 and pat[1][0] == -10 and pat[0][1] == 1 and pat[0][0] == -10):
            if self.Tiles[x + i][y + j].number < -99:
                self.queue.append([x + 1, y - 1, AI.Action.UNCOVER])

        elif (pat[1][1] == 1 and pat[1][2] == -10 and pat[0][1] == 1 and pat[0][2] == -10):
            if self.Tiles[x + 1][y + 1].number < -99:
                self.queue.append([x + 1, y + 1, AI.Action.UNCOVER])

        elif (pat[1][1] == 2 and pat[1][2] == -10 and pat[0][1] == 2 and pat[0][2] == -10):
            self.queue.append([x - 1, y + 1, AI.Action.FLAG])
            self.queue.append([x, y + 1, AI.Action.FLAG])

        elif (pat[1][1] == 2 and pat[1][0] == -10 and pat[0][1] == 2 and pat[0][0] == -10 and pat2[2] == [True, True, True]
            and [t[2] for t in pat2]== [True, True, True]):
            self.queue.append([x - 1, y - 1, AI.Action.FLAG])
            self.queue.append([x, y - 1, AI.Action.FLAG])

        elif (pat[0][1] == 2 and pat[1][1] == 2 and pat[2][1] == 1 and pat[0][2] == -10 and pat[1][2] == -10 and pat[2][
            2] == -10
                and pat[0][2] != -10 and pat[1][2] != -10 and pat[2][2] != -10):  # 2	-10
            self.queue.append([x - 1, y + 1, AI.Action.FLAG])  # "2"	-10
            self.queue.append([x, y + 1, AI.Action.FLAG])  # 1	-10

        elif pat[1] == [1,2,1] and pat2[0] == [False, False, False] and pat2[2] == [True, True, True]:
            self.queue.append([x-1, y-1, AI.Action.FLAG])
            self.queue.append([x - 1, y + 1, AI.Action.FLAG])

        elif (pat[0][0] == -10 and pat[1][0] == -10 and pat[2][0] == -10 and pat[0][1] == 1 and pat[1][1] == 2 and
                pat[2][1] == 2 and pat[0][2] != -10 and pat[1][2] != -10 and pat[2][2] != -10):
            self.queue.append([x + 1, y - 1, AI.Action.FLAG])  # -10	2

        elif (pat[1][0] == 1 and pat[1][1] == 2 and pat[1][2] == 2 and pat[0][0] == 1 and pat[0][1] == -10 and pat[0][
            2] == -10):
            self.queue.append([x - 1, y + 1, AI.Action.FLAG])
            self.queue.append([x - 1, y, AI.Action.FLAG])

        elif (pat[1][1] == 2 and len(notuncvr) == 2):
            for nuc in notuncvr:
                self.queue.append([nuc[0], nuc[1], AI.Action.FLAG])

        elif (pat[1][1] == 1 and len(notuncvr) == 1):
            for nuc in notuncvr:
                self.queue.append([nuc[0], nuc[1], AI.Action.FLAG])

        elif (pat[1][1] == 3 and len(notuncvr) == 3):
            for nuc in notuncvr:
                self.queue.append([nuc[0], nuc[1], AI.Action.FLAG])

    # for i in [-1, 0, 1]:
    #	print("\t".join([str(pat[i+1][0]), str(pat[1+i][1]), str(pat[i+1][2])]))

    def identifyPatterns4(self, x, y):
        pat = [[0 for _ in range(3)] for _ in range(3)]
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                pat[i + 1][j + 1] = self.Tiles[x + i][y + j].number
        notuncvr = []
        pat2 = [[False for _ in range(3)] for _ in range(3)]
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                pat2[i + 1][j + 1] = self.Tiles[x + i][y + j].uncover
                if not self.Tiles[x + i][y + j].uncover:
                    notuncvr.append([x + i, y + j])

        if [t[0] for t in pat2] == [False, False, False] and [t[1] for t in pat] == [1, 2, 1] and [t[2] for t in
                                                                                                   pat2] == [True, True,
                                                                                                             True]:
            self.queue.append([x - 1, y - 1, AI.Action.FLAG])
            self.queue.append([x + 1, y - 1, AI.Action.FLAG])

        elif pat2[2] == [False, False, False] and pat2[0] == [True,True,True] and pat[1][0]==1 and pat[1]==[1, 1, 1]:
            self.queue.append([x + 1, y + 1, AI.Action.UNCOVER])

    def identifyPatterns5(self, x, y):
        pat = [[0 for _ in range(3)] for _ in range(3)]
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                pat[i + 1][j + 1] = self.Tiles[x + i][y + j].number
        notuncvr = []
        pat2 = [[False for _ in range(3)] for _ in range(3)]
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                pat2[i + 1][j + 1] = self.Tiles[x + i][y + j].uncover
                if not self.Tiles[x + i][y + j].uncover:
                    notuncvr.append([x + i, y + j])

        if (pat[1][1] == 2 and len(notuncvr) == 2):
            for nuc in notuncvr:
                self.queue.append([nuc[0], nuc[1], AI.Action.FLAG])

        elif (pat[1][1] == 1 and len(notuncvr) == 1):
            for nuc in notuncvr:
                self.queue.append([nuc[0], nuc[1], AI.Action.FLAG])

        elif (pat[1][1] == 3 and len(notuncvr) == 3):
            for nuc in notuncvr:
                self.queue.append([nuc[0], nuc[1], AI.Action.FLAG])

        elif [t[2] for t in pat2] == [False, False, False] and [t[1] for t in pat] == [1, 2, 1] and [t[0] for t in
                                                                                                   pat2] == [True, True,
                                                                                                             True]:
            self.queue.append([x - 1, y + 1, AI.Action.FLAG])
            self.queue.append([x + 1, y + 1, AI.Action.FLAG])

        elif (pat[1] == [2,1,1] or pat[1]==[1,1,1]) and pat2[0] == [False, False, False] and pat2[2]==[True, True, True]:
            self.queue.append([x-1, y-1, AI.Action.UNCOVER])

        elif (pat[1] == [2,1,1] or pat[1]==[1,1,1]) and pat2[2] == [False, False, False] and pat2[0]==[True, True, True]:
            self.queue.append([x+1, y-1, AI.Action.UNCOVER])

        elif pat[1] == [1,2,1] and pat2[0] == [False, False, False] and pat2[2]==[True, True, True]:
            self.queue.append([x-1, y-1, AI.Action.FLAG])
            self.queue.append([x - 1, y + 1, AI.Action.FLAG])

        elif pat[1] == [1,2,1] and pat2[2] == [False, False, False] and pat2[0]==[True, True, True]:
            self.queue.append([x + 1, y - 1, AI.Action.FLAG])
            self.queue.append([x + 1, y + 1, AI.Action.FLAG])
