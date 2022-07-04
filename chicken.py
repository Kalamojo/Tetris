from tkinter import *
import random

class tetris:
    def run(rows=12, columns=7):
        bg = '#3A3945'
        root = Tk()
        root.configure(background=bg)

        menubar = Menu(root)
        fileMenu = Menu(menubar, tearoff=0, background=bg, foreground='#F5F6F3')
        fileMenu.add_command(label="Easy", command=lambda: tetris.setup(1000))
        fileMenu.add_command(label="Medium", command=lambda: tetris.setup(500))
        fileMenu.add_command(label="Difficult", command=lambda: tetris.setup(250))
        fileMenu.add_command(label="No shot", command=lambda: tetris.setup(100))
        menubar.add_cascade(label="New Game", menu=fileMenu)
        menubar.add_command(label="Exit", command=lambda:root.destroy())
        root.config(menu=menubar)

        global canvas
        canvas = Canvas(root, width=columns*40+100, height=rows*40+100, highlightbackground='black')
        canvas.configure(background='#292629')
        canvas.pack(padx=200)

        global can2
        can2 = Canvas(root, width=160, height=160, highlightthickness=0)
        can2.configure(background=bg)
        can2.place(x=columns*40+320, y=(rows*40+100)/2 - 80)

        root.resizable(width=0, height=0)
        class Struct: pass
        canvas.data = Struct()
        canvas.data.rows = rows
        canvas.data.columns = columns
        canvas.data.timerDelay = 500
        canvas.data.score = 0
        canvas.data.displayScore = StringVar()
        canvas.data.nextText = StringVar()
        canvas.data.default = '#1b1e2a'
        canvas.data.temp = ""
        canvas.data.temp2 = ""

        label = Label(root, textvariable=canvas.data.displayScore, foreground='#D2363F', background=bg, width=0, height=1, font=("Arial", 20, "bold"))
        label.place(x=30, y=(rows*40+100)/2 - 160)
        label = Label(root, textvariable=canvas.data.nextText, foreground='#D2363F', background=bg, width=0, height=1, font=("Arial", 17, "bold"))
        label.place(x=columns*40+320, y=(rows*40+100)/2 - 160)

        canvas.create_text((canvas.data.columns*40+100)/2, (canvas.data.rows*40+100)/2-40,text="Tetris", font=f"Times {int((canvas.data.columns*40+100)/15)} bold", fill='#D2363F')
        canvas.create_text((canvas.data.columns*40+100)/2, (canvas.data.rows*40+100)/2+20,text="Press 'r' to begin or restart", font=f"Times {int((canvas.data.columns*40+100)/20)} bold", fill='#F5F6F3')

        root.bind("<Left>", tetris.left)
        root.bind("<Right>", tetris.right)
        root.bind("<Down>", tetris.down)
        root.bind("<Up>", tetris.flip)
        root.bind("r", lambda event: tetris.setup(canvas.data.timerDelay, event))

        root.mainloop()
    
    def timerFiredWrapper():
        if canvas.data.gameOver:
            tetris.drawMainMenu()
            return;
        canvas.data.temp = canvas.after(canvas.data.timerDelay, tetris.down)
        canvas.data.temp2 = canvas.after(canvas.data.timerDelay, tetris.timerFiredWrapper)

    def setup(d, event=0,):
        canvas.data.timerDelay = d
        try:
            canvas.after_cancel(canvas.data.temp)
            canvas.after_cancel(canvas.data.temp2)
        except ValueError:
            pass;
        canvas.data.nextText.set("Next Block:")
        tetris.initBoard()
        tetris.timerFiredWrapper()
        tetris.drawMainMenu()

    def initBoard():
        canvas.data.gameOver = False
        canvas.data.gameOverFr = False
        canvas.data.score = 0
        canvas.data.displayScore.set(f"Score: {canvas.data.score}")
        print("Score:", canvas.data.score)
        canvas.data.x = int(canvas.data.columns / 2)-1
        canvas.data.y = 0
        canvas.data.xCurr = canvas.data.x
        canvas.data.yCurr = canvas.data.y
        canvas.data.currentPiece = []
        canvas.data.futureInd = [random.randint(0, 6), 0]
        canvas.data.currentInd = [0, 0]
        canvas.data.board = []
        canvas.data.activity = []
        canvas.data.tileLoc = []
        canvas.data.nextLoc = []
        canvas.data.nextBoard = []
        for r in range(canvas.data.rows):
            tempColors = []
            tempLocs = []
            tempAct = []
            for c in range(canvas.data.columns):
                tempColors.append(canvas.data.default)
                tempLocs.append((c * (40+100/canvas.data.columns), r * (40+100/canvas.data.rows)))
                tempAct.append(False)
            canvas.data.board.append(tempColors)
            canvas.data.tileLoc.append(tempLocs)
            canvas.data.activity.append(tempAct)
        # work on next tile
        for i in range(3):
            tempColors = []
            tempLocs = []
            for j in range(4):
                tempColors.append(canvas.data.default)
                tempLocs.append((j * 40, i * 40))
            canvas.data.nextBoard.append(tempColors)
            canvas.data.nextLoc.append(tempLocs)
        
        colors = ('#536b84', '#8e8f86', '#f0bc43', '#a76c92', '#46a6dc', '#de313c', '#66874a')
        canvas.data.pieceColors = colors

        canvas.data.map = {
            0:{ 
                0:[[0, 0], [0, 1], [0, 2], [0, 3]],
                1:[[0, 2], [1, 2], [2, 2], [3, 2]],
                2:[[1, 0], [1, 1], [1, 2], [1, 3]],
                3:[[0, 1], [1, 1], [2, 1], [3, 1]],},
            1:{ 
                0:[[0, 0], [1, 0], [1, 1], [1, 2]],
                1:[[0, 1], [0, 2], [1, 1], [2, 1]],
                2:[[1, 0], [1, 1], [1, 2], [2, 2]],
                3:[[0, 1], [1, 1], [2, 0], [2, 1]],},
            2:{ 
                0:[[0, 2], [1, 0], [1, 1], [1, 2]],
                1:[[0, 1], [1, 1], [2, 1], [2, 2]],
                2:[[1, 0], [1, 1], [1, 2], [2, 0]],
                3:[[0, 0], [0, 1], [1, 1], [2, 1]],},
            3:{ 
                0:[[0, 0], [0, 1], [1, 0], [1, 1]],
                1:[[0, 0], [0, 1], [1, 0], [1, 1]],
                2:[[0, 0], [0, 1], [1, 0], [1, 1]],
                3:[[0, 0], [0, 1], [1, 0], [1, 1]],},
            4:{ 
                0:[[0, 1], [0, 2], [1, 0], [1, 1]],
                1:[[0, 1], [1, 1], [1, 2], [2, 2]],
                2:[[1, 1], [1, 2], [2, 0], [2, 1]],
                3:[[0, 0], [1, 0], [1, 1], [2, 1]],},
            5:{ 
                0:[[0, 1], [1, 0], [1, 1], [1, 2]],
                1:[[0, 1], [1, 1], [1, 2], [2, 1]],
                2:[[1, 0], [1, 1], [1, 2], [2, 1]],
                3:[[0, 1], [1, 0], [1, 1], [2, 1]],},
            6:{ 
                0:[[0, 0], [0, 1], [1, 1], [1, 2]],
                1:[[0, 2], [1, 1], [1, 2], [2, 1]],
                2:[[1, 0], [1, 1], [2, 1], [2, 2]],
                3:[[0, 1], [1, 0], [1, 1], [2, 0]],},
        }

        tetris.spawn_new()
    
    def drawMainMenu():
        if not canvas.data.gameOverFr:
            if canvas.data.gameOver:
                canvas.data.gameOverFr = True
            canvas.delete('all')
            for r in range(canvas.data.rows):
                for c in range(canvas.data.columns):
                    (x, y) = canvas.data.tileLoc[r][c]
                    color = canvas.data.board[r][c]
                    canvas.create_rectangle(x, y, x+40+100/canvas.data.columns, y+40+100/canvas.data.rows, fill=color, width=3)
        else:
            over = canvas.create_text((canvas.data.columns*40+100)/2, (canvas.data.rows*40+100)/2, text="Game Over", fill='#D2363F', font=f"Times {int((canvas.data.columns*40+100)/10)} bold")
            bbox = canvas.bbox(over)
            rect_item = canvas.create_rectangle(bbox, outline="black", fill="#292629", width=3)
            canvas.tag_raise(over,rect_item)


    def drawSubMenu(i):
        ind = canvas.data.map[i][0]
        color = canvas.data.pieceColors[i]
        can2.delete('all')
        for b in ind:
            (x, y) = canvas.data.nextLoc[b[0]][b[1]]
            can2.create_rectangle(x, y, x+40, y+40, fill=color, width=3)

    def left(event):
        movers = []
        moves = True
        for r in range(canvas.data.rows):
            for c in range(canvas.data.columns):
                if canvas.data.activity[r][c]:
                    if c == 0 or canvas.data.board[r][c-1] != canvas.data.default and not canvas.data.activity[r][c-1]:
                        moves = False
                        break
                    movers.append([r, c])
            if not moves:
                break
        if moves:
            canvas.data.xCurr -= 1
            for i in range(len(movers)):
                tetris.blockMoveX(movers[i][0], movers[i][1], -1)
                canvas.data.currentPiece[i][1] -= 1
            tetris.drawMainMenu()
        if tetris.check_next():
            tetris.spawn_new()
            tetris.drawMainMenu()
    
    def right(event):
        movers = []
        moves = True
        for r in range(canvas.data.rows):
            for c in reversed(range(canvas.data.columns)):
                if canvas.data.activity[r][c]:
                    if c == canvas.data.columns-1 or canvas.data.board[r][c+1] != canvas.data.default and not canvas.data.activity[r][c+1]:
                        moves = False
                        break
                    movers.append([r, c])
            if not moves:
                break
        if moves:
            canvas.data.xCurr += 1
            for i in range(len(movers)):
                tetris.blockMoveX(movers[i][0], movers[i][1], 1)
                canvas.data.currentPiece[i][1] += 1
            tetris.drawMainMenu()
        if tetris.check_next():
            tetris.spawn_new()
            tetris.drawMainMenu()

    def down(event = 0):
        movers = []
        moves = True
        for c in range(canvas.data.columns):
            for r in reversed(range(canvas.data.rows)):
                if canvas.data.activity[r][c]:
                    if r == canvas.data.rows-1 or canvas.data.board[r+1][c] != canvas.data.default and not canvas.data.activity[r+1][c]:
                        moves = False
                    movers.append([r, c])
        if moves:
            canvas.data.yCurr += 1
            for i in range(len(movers)):
                tetris.blockMoveY(movers[i][0], movers[i][1], 1)
                canvas.data.currentPiece[i][0] += 1
            tetris.drawMainMenu()
        if tetris.check_next():
            tetris.spawn_new()
            tetris.drawMainMenu()

    def flip(event):
        if canvas.data.xCurr >= 0:
            temp = canvas.data.currentPiece.copy()
            tempInd = canvas.data.currentInd[1]
            colors = canvas.data.board.copy()
            activities = canvas.data.activity.copy()
            rev = False
            try:
                for b in canvas.data.currentPiece:
                    canvas.data.board[b[0]][b[1]] = canvas.data.default
                    canvas.data.activity[b[0]][b[1]] = False
                canvas.data.currentInd[1] = 0 if canvas.data.currentInd[1] == 3 else canvas.data.currentInd[1] + 1
                canvas.data.currentPiece = [[y+canvas.data.yCurr, x+canvas.data.xCurr] for [y, x] in canvas.data.map[canvas.data.currentInd[0]][canvas.data.currentInd[1]]]
                for b in canvas.data.currentPiece:
                    if canvas.data.board[b[0]][b[1]] != canvas.data.default:
                        rev = True
                    canvas.data.board[b[0]][b[1]] = canvas.data.pieceColors[canvas.data.currentInd[0]]
                    canvas.data.activity[b[0]][b[1]] = True
            except IndexError:
                rev = True
            if rev:
                tetris.revert(temp, tempInd, colors, activities)
            else:
                if tetris.check_next():
                    tetris.spawn_new()
            tetris.drawMainMenu()
    
    def revert(t, i, co, a):
        canvas.data.currentPiece = t
        canvas.data.currentInd[1] = i
        for c in range(canvas.data.columns):
            for r in reversed(range(canvas.data.rows)):
                canvas.data.board[r][c] = co[r][c]
                canvas.data.activity[r][c] = a[r][c]

    def check_next():
        stoppers = []
        stops = False
        #for c in range(canvas.data.columns):
            #for r in reversed(range(canvas.data.rows)):
        for p in canvas.data.currentPiece:
            if canvas.data.activity[p[0]][p[1]]:
                if p[0] == canvas.data.rows-1 or canvas.data.board[p[0]+1][p[1]] != canvas.data.default and not canvas.data.activity[p[0]+1][p[1]]:
                    stops = True
                stoppers.append([p[0], p[1]])
        if stops:
            for m in stoppers:
                    canvas.data.activity[m[0]][m[1]] = False
            tetris.clear_row()
            return True
        return False

    def clear_row():
        clears = False
        ry = []
        for r in reversed(range(canvas.data.rows)):
            row = canvas.data.columns
            for c in range(canvas.data.columns):
                if canvas.data.board[r][c] != canvas.data.default:
                    row -= 1
            if row == 0:
                ry.append(r)
                clears = True
                for c in range(canvas.data.columns):
                    canvas.data.board[r][c] = canvas.data.default
                tetris.drawMainMenu()
        if clears:
            for i in reversed(range(len(ry))):
                canvas.data.score += 1
                canvas.data.displayScore.set(f"Score: {canvas.data.score}")
                print("Score:", canvas.data.score)
                for r in reversed(range(ry[i])):
                    for c in range(canvas.data.columns):
                        if canvas.data.board[r][c] != canvas.data.default:
                            tetris.blockMoveY(r, c, 1)
    
    def spawn_new():
        canvas.data.xCurr = canvas.data.x
        canvas.data.yCurr = canvas.data.y
        canvas.data.currentInd = canvas.data.futureInd
        p = canvas.data.map[canvas.data.currentInd[0]][0].copy()
        c = canvas.data.pieceColors[canvas.data.currentInd[0]]
        canvas.data.currentPiece = [[y+canvas.data.y, x+canvas.data.x] for [y, x] in p.copy()]
        for b in canvas.data.currentPiece:
            if canvas.data.board[b[0]][b[1]] != canvas.data.default:
                tetris.gameOver()
            canvas.data.board[b[0]][b[1]] = c
            canvas.data.activity[b[0]][b[1]] = True
        if tetris.check_next():
            tetris.gameOver()
        canvas.data.futureInd = [random.randint(0, 6), 0]
        tetris.drawSubMenu(canvas.data.futureInd[0])
    
    def blockMoveX(r, c, l):
        canvas.data.board[r][c+l], canvas.data.board[r][c] = canvas.data.board[r][c], canvas.data.board[r][c+l]
        canvas.data.activity[r][c+l], canvas.data.activity[r][c] = canvas.data.activity[r][c], canvas.data.activity[r][c+l]
    def blockMoveY(r, c, l):
        canvas.data.board[r+l][c], canvas.data.board[r][c] = canvas.data.board[r][c], canvas.data.board[r+l][c]
        canvas.data.activity[r+l][c], canvas.data.activity[r][c] = canvas.data.activity[r][c], canvas.data.activity[r+l][c]

    def gameOver():
        print("Game Over")
        canvas.data.gameOver = True
        #canvas.create_rectangle()


game = tetris
tetris.run(14, 10)