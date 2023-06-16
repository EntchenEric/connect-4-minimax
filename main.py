import pygame
import copy

pygame.init()

GAME_ACTIVE = True

# colors
BLUE = (30, 144, 255)
RED = (220, 20, 60)
YELLOW = (255, 255, 51)
GRAY = (129, 133, 137)
PLUM = (221,160,221)

HEIGHT = 900
SCREEN_RES = (HEIGHT / 6 * 7, HEIGHT)
FPS = 60

PADDING = 50
# This is not pixels. Be careful with this number.
SPACE_BETWEEN = 5

#also be carefull with this.
MAX_DEPTH = 4

CIRCLE_RADIUS = ((HEIGHT-PADDING)/6-(SPACE_BETWEEN*6))/2

SECTIONS = []

for y in range(6):
    for x in range(7):
        SECTIONS.append(
            (((SCREEN_RES[0] - PADDING/2)/7*(x + 1)), ((SCREEN_RES[1]-PADDING/2)/6*(y + 1))))

BOARD = [
    0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0
]

screen = pygame.display.set_mode(SCREEN_RES)
clock = pygame.time.Clock()

turn = 1

cashedMinimaxBoards = {}


def getSection(pos: tuple):
    for sectionid, section in enumerate(SECTIONS):
        if (pos[0] < section[0] and pos[1] < section[1]):
            return sectionid
    return None


def drawCircles(screen):
  for blockid, block in enumerate(BOARD):
        color = GRAY
        if(block == 1):
            color = YELLOW
        elif(block == 2):
            color = RED
        section = SECTIONS[blockid]
        pygame.draw.circle(surface=screen, color=color, center=(section[0] - CIRCLE_RADIUS, section[1] - CIRCLE_RADIUS), radius=CIRCLE_RADIUS)

def getWinner(board: list):
    for blockid, block in enumerate(board):
        if block != 0:
            if(blockid % 7 <= 3):
                if block == board[blockid + 1] and block == board[blockid + 2] and block == board[blockid + 3]:
                    return block
            if(blockid <= 20):
                if block == board[blockid + 7] and block == board[blockid + 14] and block == board[blockid + 21]:
                    return block
            if(blockid % 7 <= 3 and blockid <= 20):
                if block == board[blockid + 8] and block == board[blockid + 16] and block == board[blockid + 24]:
                    return block
            if blockid % 7 >= 3 and blockid <= 20:
                if block == board[blockid + 6] and block == board[blockid + 12] and block == board[blockid + 18]:
                    return block
    return None


def getWinnngSections(board: list):
    for blockid, block in enumerate(board):
        if block != 0:
            if(blockid % 7 <= 3):
                if block == board[blockid + 1] and block == board[blockid + 2] and block == board[blockid + 3]:
                    return (blockid, blockid + 1, blockid + 2, blockid + 3)
            if(blockid <= 20):
                if block == board[blockid + 7] and block == board[blockid + 14] and block == board[blockid + 21]:
                    return (blockid, blockid + 7, blockid + 14, blockid + 21)
            if(blockid % 7 <= 3 and blockid <= 20):
                if block == board[blockid + 8] and block == board[blockid + 16] and block == board[blockid + 24]:
                    return (blockid, blockid + 8, blockid + 16, blockid + 24)
            if blockid % 7 >= 3 and blockid <= 20:
                if block == board[blockid + 6] and block == board[blockid + 12] and block == board[blockid + 18]:
                    return (blockid, blockid + 6, blockid + 12, blockid + 18)
    return None

def minimax(board, depth, isMaximizing):
    winner = getWinner(board)
    if winner:
        print(winner)
    if (winner == 2):
        return 100
    elif (winner == 1):
        return -100
    elif not 0 in board:
        return 0
    
    if depth >= MAX_DEPTH:
        return 0

    if isMaximizing:
        bestScore = -1000
        for blockid, block in enumerate(board):
            if block == 0:
                if blockid > 34 or board[blockid + 7] != 0:
                    boardcopy = copy.deepcopy(board)
                    boardcopy[blockid] = 2
                    if str(boardcopy) in cashedMinimaxBoards:
                        return cashedMinimaxBoards[str(boardcopy)]
                    score = minimax(boardcopy, depth, False)
                    cashedMinimaxBoards[str(boardcopy)] = score
                    if score > bestScore:
                        bestScore = score
        return bestScore
    else:
        bestScore = 1000
        for blockid, block in enumerate(board):
            if block == 0:
                if blockid > 34 or board[blockid + 7] != 0:
                    boardcopy = copy.deepcopy(board)
                    boardcopy[blockid] = 1
                    if str(boardcopy) in cashedMinimaxBoards:
                        return cashedMinimaxBoards[str(boardcopy)]
                    score = minimax(boardcopy, depth + 1, True)
                    cashedMinimaxBoards[str(boardcopy)] = score
                    if score < bestScore:
                        bestScore = score
        return bestScore

def makeBotTurn():
    global cashedMinimaxBoards
    cashedMinimaxBoards = {}
    bestPos = None
    bestPoints = -9999
    for blockid, block in enumerate(BOARD):
        if block == 0:
            if blockid > 34 or BOARD[blockid + 7] != 0:
                boardcopy = copy.deepcopy(BOARD)
                boardcopy[blockid] = 2
                score = minimax(boardcopy, 0, False)
                if score > bestPoints:
                    bestPos = blockid
                    bestPoints = score
                    print("new best score of ", bestPoints, " at ", bestPos)
    BOARD[bestPos] = 2

while GAME_ACTIVE:
    screen.fill(BLUE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            GAME_ACTIVE = False      
        elif event.type == pygame.MOUSEBUTTONDOWN:
            section = getSection(pygame.mouse.get_pos())
            if(BOARD[section] == 0 and getWinner(BOARD) == None and 0 in BOARD):
                blockpos = section % 7

                while blockpos <= 34 and BOARD[blockpos + 7] == 0:
                    blockpos += 7

                BOARD[blockpos] = 1
                if(getWinner(BOARD) == None and 0 in BOARD):
                    blockid = 0

                    makeBotTurn()

        

    drawCircles(screen)

    if(getWinner(BOARD)):
        winningpos = getWinnngSections(BOARD)
        pygame.draw.line(surface=screen, color=PLUM, start_pos=(SECTIONS[winningpos[0]][0]-CIRCLE_RADIUS, SECTIONS[winningpos[0]][1]-CIRCLE_RADIUS), end_pos=(SECTIONS[winningpos[-1]][0]-CIRCLE_RADIUS, SECTIONS[winningpos[-1]][1]-CIRCLE_RADIUS), width=15)

    pygame.display.flip()
    clock.tick(FPS)