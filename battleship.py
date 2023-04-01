import random
from recognizer import recognize, tts_speak
from ships import small_ship, medium_ship, big_ship, huge_ship, Positions
import pygame

# Method for initializing the game field
def initField():
    f = []
    for i in range(10):
        f.append([])
        for j in range(10):
            f[i].append("o")
    return f

# Method for displaying the game field
def displayField(field):
    for i in range(10):
        line = ""
        for j in range(10):
            line += field[i][j]
        print(line)

# Method for drawing a grid onto the game field to make fields more distinguishable
def drawGrid(screen):
    blockSize = 50
    for x in range(50, 550, blockSize):
        for y in range(50, 550, blockSize):
            rect = pygame.Rect(x, y, blockSize, blockSize)
            pygame.draw.rect(screen, (255,255,255), rect, 1)
    for i in range(10):
        rect = pygame.Rect(70+50*i, 20, 20, 20)
        c = chr(65+i)
        screen.blit(pygame.font.Font(None, 24).render(c, True, (0,0,0)), (rect.x, rect.y))
    for i in range(10):
        rect = pygame.Rect(20, 70+50*i, 20, 20)
        screen.blit(pygame.font.Font(None, 24).render(str(i), True, (0,0,0)), (rect.x, rect.y))
    
    for x in range(1050, 1550, blockSize):
        for y in range(50, 550, blockSize):
            rect = pygame.Rect(x, y, blockSize, blockSize)
            pygame.draw.rect(screen, (255,255,255), rect, 1)
    for i in range(10):
        rect = pygame.Rect(1070+50*i, 20, 20, 20)
        c = chr(65+i)
        screen.blit(pygame.font.Font(None, 24).render(c, True, (0,0,0)), (rect.x, rect.y))
    for i in range(10):
        rect = pygame.Rect(1020, 70+50*i, 20, 20)
        screen.blit(pygame.font.Font(None, 24).render(str(i), True, (0,0,0)), (rect.x, rect.y))

# Method for checking if schips collide
def checkCollision(field, ship):
    for i in range(ship.length):
        match ship.positioning:
            case Positions.horizontal:
                if ship.pos[0]+i > len(field)-1:
                    return True
                if field[ship.pos[1]][ship.pos[0]+i] == "x" or field[ship.pos[1]][ship.pos[0]+i+1 if ship.pos[0]+i < 9 else ship.pos[0]+i] == "x" or field[ship.pos[1]][ship.pos[0]+i-1 if ship.pos[0]+i > 0 else ship.pos[0]+i] == "x" or field[ship.pos[1]+1 if ship.pos[1] < 9 else 9][ship.pos[0]+i] == "x" or field[ship.pos[1]-1 if ship.pos[1] > 0 else 0][ship.pos[0]+i] == "x":
                    return True
            case Positions.vertical:
                if ship.pos[1]+i > len(field)-1:
                    return True
                if field[ship.pos[1]+i][ship.pos[0]] == "x" or field[ship.pos[1]+i+1 if ship.pos[1]+i < 9 else ship.pos[1]+i][ship.pos[0]] == "x" or field[ship.pos[1]+i-1 if ship.pos[1]+i > 0 else ship.pos[1]+i][ship.pos[0]] == "x" or field[ship.pos[1]+i][ship.pos[0]+1 if ship.pos[0] < 9 else 9] == "x" or field[ship.pos[1]+i][ship.pos[0]-1 if ship.pos[0] > 0 else 0] == "x":
                    return True
    return False

# Method for adding elements to the game field
def addToField(screen, field, list, ship, botOn=False, cnt=None, auto=False):
    if checkCollision(field, ship):
        setShips(screen, field, list, botOn, cnt+1, auto)
        return
    positions = []
    for i in range(ship.length):
        match ship.positioning:
            case Positions.vertical:
                field[ship.pos[1]+i][ship.pos[0]] = "x"
                positions.append((ship.pos[1]+i, ship.pos[0]))
                if not botOn or auto: pygame.draw.rect(screen, (200,100,150), pygame.Rect(ship.pos[0]*50+50, (ship.pos[1]+i)*50+50, 50, 50))
            case Positions.horizontal:
                field[ship.pos[1]][ship.pos[0]+i] = "x"
                positions.append((ship.pos[1], ship.pos[0]+i))
                if not botOn or auto: pygame.draw.rect(screen, (200,100,150), pygame.Rect((ship.pos[0]+i)*50+50, ship.pos[1]*50+50, 50, 50))
        drawGrid(screen)
        if botOn == False:
            pygame.display.update()
    ship.pos = positions
    list.append(ship)        
    setShips(screen, field, list, botOn, cnt, auto)

# Method for setting the positions of ships
def setShips(screen, playingField, list, botOn, cnt=6, auto=False):
    if botOn:
        if cnt > 4:
            pos = random.randint(0,9), random.randint(0,9)
            direction = Positions.vertical if random.randint(0,1) == 0 else Positions.horizontal
            s = small_ship(pos, direction)
            addToField(screen, playingField, list, s, True, cnt=cnt-1, auto=auto)
        elif cnt > 3:
            pos = random.randint(0,9), random.randint(0,9)
            direction = Positions.vertical if random.randint(0,1) == 0 else Positions.horizontal
            s = medium_ship(pos, direction)
            addToField(screen, playingField, list, s, True, cnt=cnt-1, auto=auto)
        elif cnt > 1:    
            pos = random.randint(0,9), random.randint(0,9)
            direction = Positions.vertical if random.randint(0,1) == 0 else Positions.horizontal
            s = big_ship(pos, direction)
            addToField(screen, playingField, list, s, True, cnt=cnt-1, auto=auto)
        elif cnt > 0:
            pos = random.randint(0,9), random.randint(0,9)
            direction = Positions.vertical if random.randint(0,1) == 0 else Positions.horizontal
            s = huge_ship(pos, direction)
            addToField(screen, playingField, list, s, True, cnt=cnt-1, auto=auto)
        return
    else:
        if cnt > 4:
            pygame.event.get()
            tts_speak("Press space to start")
            temp = True
            while temp:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_SPACE:
                                temp=False
            p = recognize("Position of ship", "pos")
            pos = ord(p[0])-65, int(p[1])
            direction = Positions.vertical if recognize("Orientation of ship", "orient") == 0 else Positions.horizontal
            s = small_ship(pos, direction)
            addToField(screen, playingField, list, s, False, cnt-1)
        elif cnt > 3:
            pygame.event.get()
            tts_speak("Press space to start")
            temp = True
            while temp:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_SPACE:
                                temp=False
            p = recognize("Position of ship", "pos")
            pos = ord(p[0])-65, int(p[1])
            direction = Positions.vertical if recognize("Orientation of ship", "orient")  == 0 else Positions.horizontal
            s = medium_ship(pos, direction)
            addToField(screen, playingField, list, s, False, cnt-1)
        elif cnt > 1:
            pygame.event.get()
            tts_speak("Press space to start")
            temp = True
            while temp:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_SPACE:
                                temp=False
            p = recognize("Position of ship", "pos")
            pos = ord(p[0])-65, int(p[1])
            direction = Positions.vertical if recognize("Orientation of ship", "orient")  == 0 else Positions.horizontal
            s = big_ship(pos, direction)
            addToField(screen, playingField, list, s, False, cnt-1)
        elif cnt > 0:
            pygame.event.get()
            tts_speak("Press space to start")
            temp = True
            while temp:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_SPACE:
                                temp=False
            p = recognize("Position of ship", "pos")
            pos = ord(p[0])-65, int(p[1])
            direction = Positions.vertical if recognize("Orientation of ship", "orient")  == 0 else Positions.horizontal
            s = huge_ship(pos, direction)
            addToField(screen, playingField, list, s, False, cnt-1)
        return

# Method for attacking the ships of the enemy
def attack(pos, screen, field, list, hitlist, bot, auto):
    if (pos[1],pos[0]) not in hitlist:
        for i in range(len(list)):
            for j in range(len(list[i].pos)):
                if (pos[1], pos[0]) == list[i].pos[j]:
                    list[i].hits += 1
                    hitlist.append((pos[1], pos[0]))
                    if bot == False:
                        pygame.draw.rect(screen, (50,230,100), pygame.Rect((pos[0]*50)+1050, (pos[1]*50)+50, 50, 50))
                    else:
                        pygame.draw.rect(screen, (50,230,100), pygame.Rect((pos[0]*50)+50, (pos[1]*50)+50, 50, 50))
                    return
        hitlist.append((pos[1], pos[0]))
        if bot == False:
            pygame.draw.rect(screen, (10,10,10), pygame.Rect((pos[0]*50)+1050, (pos[1]*50)+50, 50, 50))
        else:
            pygame.draw.rect(screen, (10,10,10), pygame.Rect((pos[0]*50)+50, (pos[1]*50)+50, 50, 50))
    else:
        if bot == True or auto:
            attack((random.randint(0,9), random.randint(0,9)), screen, field, list, hitlist, bot, auto)
        else:
            p = recognize("Error - Position to attack", "pos")
            po = ord(p[0])-65, int(p[1])
            attack(po, screen, field, list, hitlist, bot, auto)

# Method for checking the state of the game
def checkGame(list, enemyList):
    count = 0
    for i in range(len(list)):
        if list[i].hits == list[i].length:
            count += 1
    if count == len(list):
        tts_speak("You lose!")
        return False
      
    count = 0
    for i in range(len(enemyList)):
        if enemyList[i].hits == enemyList[i].length:
            count += 1
    if count == len(enemyList):
        tts_speak("You win!")
        return False
    
    return True
        
def main():
    # Initializing the Game Field
    gameState = True
    playingField = initField()
    enemyField = initField()
    shipList = []
    enemyShipList = []
    userHitlist = []
    enenemyHitlist = []
    # Displaying the game field
    pygame.init()
    size = 1550, 550
    screen = pygame.display.set_mode(size)
    screen.fill((100,50,250))
    drawGrid(screen)
    pygame.display.update()
    # Setting the ships for both player and enemy
    # For demonstration purposes
    # Ships can either be set automatically or per voice commands
    setShips(screen, playingField, shipList, True, auto=True) 
    #setShips(screen, playingField, shipList, False)
    setShips(screen, enemyField, enemyShipList, True)
    displayField(playingField)
    tts_speak("Press space to attack")
    # Playing of the game starts
    while gameState:
        gameState = checkGame(shipList, enemyShipList)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return
                    if event.key == pygame.K_SPACE:
                        #p = recognize("Position to attack", "pos")
                        #pos = ord(p[0])-65, int(p[1])
                        #attack(pos, screen, enemyField, enemyShipList, userHitlist, False, False)
                        # For demonstration purposes
                        
                        # Player can attack with voice commands while enemy attacks automatically
                        attack((random.randint(0,9), random.randint(0,9)), screen, enemyField, enemyShipList, userHitlist, False, True)
                        attack((random.randint(0,9), random.randint(0,9)), screen, playingField, shipList, enenemyHitlist, True, False)
        drawGrid(screen)
        pygame.display.update()
    
if __name__ == "__main__":
    main()