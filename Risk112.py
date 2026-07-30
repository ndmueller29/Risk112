from cmu_graphics import *
from PIL import Image
import random
import copy
import os
import pathlib
import ast
from territoryClass import *
from boardClass import *
from fightClass import *
from animationClass import *
from cardClass import *



# --- SETUP FUNCTIONS ----------------------------------------------------



#this is the first function that gets called, and is only run once
def onAppStart(app):

    #make the screen bigger
    app.width = 1300
    app.height = 780

    #no active animations to start
    app.stepsPerSecond = 15
    app.animationCounter = 0
    explosionUpload(app)
    app.allAnimations = []

    loadDice(app)

    loadTroopPics(app)
    app.startScreen = True #start on the start screen

    #initialize these early so that onKeyPress doesn't crash
    app.fightWon = False
    app.readyToFortify = False

#this function gets called each time a new game is started
def loadNewGame(app):

    createNewBoard(app) #creates the board, randomizing who gets each territory

    #load in the cards
    loadDeck(app)
    app.topOfDeck = 0 #index of top card
    app.setsTurnedIn = 0
    app.giveCard = True

    app.loadingScreen = False #no longer on the loading screen

    #initializing variables to their inactive state
    app.currentFight = Fight()
    app.fightWon = False
    app.readyToFortify = False
    app.fortifyTerr1 = None
    app.fortifyTerr2 = None
    app.winner = None
    app.whoseTurn = 1 #player 1 always goes first
    app.phase = 1 #each turn starts with phase 1
    app.selectedTerr = None
    app.placeTroopsNum = calculateTroopsToPlace(app)
    app.message = f'Player 1: Place your {app.placeTroopsNum} troops'
    app.cornerMessage = 'End Phase'
    app.rules = False

#this function gets called to load in an old game
def loadOldGame(app, saveData):

    createBoard(app) #load in the territories, but don't randomly assign them

    #restoring territorial ownership and troop numbers
    for i in range(len(app.board.t)):
        territory = app.board.t[i]

        playerNum = saveData[f'terr {i}: player']
        numTroops = saveData[f'terr {i}: numTroops']

        territory.setPlayer(playerNum)
        territory.drawnCMUImage = CMUImage(territory.drawnImage)
        territory.numTroops = numTroops


    #restoring the state of the cards and deck
    app.deck = []
    for i in range(saveData['deckLength']):
        terr = saveData[f'card {i}: terr']
        cardType = saveData[f'card {i}: type']
        player = saveData[f'card {i}: player']
        
        app.deck.append(Card(terr, cardType, player))

    app.topOfDeck = saveData['topOfDeck']
    app.setsTurnedIn = saveData['setsTurnedIn']
    app.giveCard = saveData['giveCard']

    #set active players and whose turn
    app.activePlayerList = saveData['activePlayersList']
    app.whoseTurn = saveData['whose turn']

    #everything else is the same as loading a new game

    #initializing variables to their inactive state
    app.loadingScreen = False
    app.currentFight = Fight()
    app.fightWon = False
    app.readyToFortify = False
    app.fortifyTerr1 = None
    app.fortifyTerr2 = None
    app.winner = None
    app.phase = 1 #each turn starts with phase 1
    app.selectedTerr = None
    app.placeTroopsNum = calculateTroopsToPlace(app)
    app.message = (
        f'Player {app.whoseTurn}: Place your {app.placeTroopsNum} troops')
    app.cornerMessage = 'End Phase'
    app.rules = False

def createBoard(app):

    #all images used in this function were cropped from one singular image
    #the url for the website with the image is:
    #https://commons.wikimedia.org/wiki/File:Risk_board.svg


    #uploading and placing North American territories

    alaskaImage = openImage("images/alaska.png")
    alaska = Territory(70, 105, alaskaImage, 72, 89)

    westernCanadaImage = openImage("images/westernCanada.png")
    westernCanada = Territory(164, 154, westernCanadaImage, 164, 155)

    northernCanadaImage = openImage("images/northernCanada.png")
    northernCanada = Territory(196, 83, northernCanadaImage, 180, 95)

    centralCanadaImage = openImage("images/centralCanada.png")
    centralCanada = Territory(252, 177, centralCanadaImage, 242, 172)

    easternCanadaImage = openImage("images/easternCanada.png")
    easternCanada = Territory(327, 170, easternCanadaImage, 325, 168)

    greenlandImage = openImage("images/greenland.png")
    greenland = Territory(450, 97, greenlandImage, 448, 83, beaches=True)

    westernUSAImage = openImage("images/westernUSA.png")
    westernUSA = Territory(176, 247, westernUSAImage, 174, 238)

    easternUSAImage = openImage("images/easternUSA.png")
    easternUSA = Territory(263, 259, easternUSAImage, 258, 263)

    mexicoImage = openImage("images/mexico.png")
    mexico = Territory(179, 346, mexicoImage, 178, 337)

    #assign north american neighbors
    alaska.neighborsList.extend([westernCanada, northernCanada])
    westernCanada.neighborsList.extend([alaska, northernCanada, westernUSA,
                                        centralCanada])
    northernCanada.neighborsList.extend([alaska, greenland, westernCanada,
                                         centralCanada])
    centralCanada.neighborsList.extend([westernCanada, northernCanada,
                                        easternCanada, westernUSA, easternUSA])
    easternCanada.neighborsList.extend([centralCanada, greenland, easternUSA])
    greenland.neighborsList.extend([northernCanada, easternCanada])
    westernUSA.neighborsList.extend([westernCanada, centralCanada, easternUSA,
                                     mexico])
    easternUSA.neighborsList.extend([westernUSA, centralCanada, easternCanada,
                                     mexico])
    mexico.neighborsList.extend([westernUSA, easternUSA])
    
    #uploading and placing South American territories

    colombiaImage = openImage("images/colombia.png")
    colombia = Territory(282, 417, colombiaImage, 262, 410)

    peruImage = openImage("images/peru.png")
    peru = Territory(272, 503, peruImage, 272, 510)

    brazilImage = openImage("images/brazil.png")
    brazil = Territory(329, 508, brazilImage, 344, 483)

    argentinaImage = openImage("images/argentina.png")
    argentina = Territory(280, 645, argentinaImage, 280, 615,
                                                            beaches=True)

    #assign south american neighbors
    colombia.neighborsList.extend([peru, brazil])
    peru.neighborsList.extend([colombia, brazil, argentina])
    brazil.neighborsList.extend([colombia, peru, argentina])
    argentina.neighborsList.extend([peru, brazil])

    #uploading and placing European territories

    icelandImage = openImage("images/iceland.png")
    iceland = Territory(585, 87, icelandImage, 585, 129, beaches=True)

    britishIslesImage = openImage("images/britishIsles.png")
    britishIsles = Territory(555, 217, britishIslesImage, 576, 232,
                                                            beaches=True)
    
    spainImage = openImage("images/spain.png")
    spain = Territory(585, 319, spainImage, 585, 329)

    germanyImage = openImage("images/germany.png")
    germany = Territory(663, 233, germanyImage, 665, 236)

    italyImage = openImage("images/italy.png")
    italy = Territory(673, 311, italyImage, 673, 299)

    easternEuropeImage = openImage("images/easternEurope.png")
    easternEurope = Territory(781, 202, easternEuropeImage, 767, 192)

    scandanaviaImage = openImage("images/scandanavia.png")
    scandanavia = Territory(675, 130, scandanaviaImage, 667, 130)

    #assign european neighbors
    iceland.neighborsList.extend([britishIsles, scandanavia])
    britishIsles.neighborsList.extend([spain, germany, iceland, scandanavia])
    spain.neighborsList.extend([britishIsles, germany, italy])
    germany.neighborsList.extend([britishIsles, spain, italy, scandanavia,
                                  easternEurope])
    italy.neighborsList.extend([spain, germany, easternEurope])
    easternEurope.neighborsList.extend([scandanavia, germany, italy])
    scandanavia.neighborsList.extend([iceland, britishIsles, easternEurope,
                                      germany])
    
    #uploading and placing Asian territories
    
    russia1Image = openImage("images/russia1.png")
    russia1 = Territory(898, 145, russia1Image, 885, 145)

    russia2Image = openImage("images/russia2.png")
    russia2 = Territory(944, 124, russia2Image, 947, 106)

    russia3Image = openImage("images/russia3.png")
    russia3 = Territory(1039, 76, russia3Image, 1034, 74)

    russia4Image = openImage("images/russia4.png")
    russia4 = Territory(1150, 115, russia4Image, 1128, 78, beaches=True)

    kazakhstanImage = openImage("images/kazakhstan.png")
    kazakhstan = Territory(867, 265, kazakhstanImage, 872, 267)

    mongoliaImage = openImage("images/mongolia.png")
    mongolia = Territory(1027, 163, mongoliaImage, 1023, 166)

    northernChinaImage = openImage("images/northernChina.png")
    northernChina = Territory(1042, 234, northernChinaImage, 1034, 243)

    southernChinaImage = openImage("images/southernChina.png")
    southernChina = Territory(1003, 309, southernChinaImage, 1003, 324)

    japanImage = openImage("images/japan.png")
    japan = Territory(1160, 250, japanImage, 1166, 269, beaches=True)

    middleEastImage = openImage("images/middleEast.png")
    middleEast = Territory(800, 403, middleEastImage, 800, 403, beaches=True)

    indiaImage = openImage("images/india.png")
    india = Territory(935, 399, indiaImage, 938, 384)

    southeastAsiaImage = openImage("images/southeastAsia.png")
    southeastAsia = Territory(1035, 427, southeastAsiaImage, 1027, 412,
                                                        beaches=True)

    #assigning asian neighbors
    russia1.neighborsList.extend([russia2, southernChina, kazakhstan])
    russia2.neighborsList.extend([russia1, russia3, mongolia, northernChina,
                                  southernChina])
    russia3.neighborsList.extend([russia2, russia4, mongolia])
    russia4.neighborsList.extend([russia3, mongolia, northernChina, japan])
    kazakhstan.neighborsList.extend([russia1, southernChina, india, middleEast])
    mongolia.neighborsList.extend([russia2, russia3, russia4, northernChina])
    northernChina.neighborsList.extend([mongolia, russia4, japan, russia2,
                                        southernChina])
    southernChina.neighborsList.extend([northernChina, russia2, russia1,
                                        kazakhstan, india, southeastAsia])
    japan.neighborsList.extend([russia4, northernChina])
    middleEast.neighborsList.extend([kazakhstan, india])
    india.neighborsList.extend([middleEast, kazakhstan, southernChina,
                                southeastAsia])
    southeastAsia.neighborsList.extend([india, southernChina])
    
    #uploading and placing African territories

    westAfricaImage = openImage("images/westAfrica.png")
    westAfrica = Territory(630, 469, westAfricaImage, 635, 469, beaches=True)
    
    northAfricaImage = openImage("images/northAfrica.png")
    northAfrica = Territory(712, 427, northAfricaImage, 710, 426)

    centralAfricaImage = openImage("images/centralAfrica.png")
    centralAfrica = Territory(717, 561, centralAfricaImage, 717, 561)

    eastAfricaImage = openImage("images/eastAfrica.png")
    eastAfrica = Territory(778, 544, eastAfricaImage, 763, 506)

    southAfricaImage = openImage("images/southAfrica.png")
    southAfrica = Territory(676, 678, southAfricaImage, 725, 668,
                                                            beaches=True)

    madagascarImage = openImage("images/madagascar.png")
    madagascar = Territory(830, 675, madagascarImage, 830, 675, beaches=True)

    #assign african neighbors
    westAfrica.neighborsList.extend([northAfrica, eastAfrica, centralAfrica])
    eastAfrica.neighborsList.extend([northAfrica, centralAfrica, southAfrica,
                                     westAfrica, madagascar])
    centralAfrica.neighborsList.extend([westAfrica, southAfrica, eastAfrica])
    northAfrica.neighborsList.extend([westAfrica, eastAfrica])
    southAfrica.neighborsList.extend([centralAfrica, eastAfrica, madagascar])
    madagascar.neighborsList.extend([southAfrica, eastAfrica])

    #uploading and placing Oceanian territories

    indonesiaImage = openImage("images/indonesia.png")
    indonesia = Territory(1030, 550, indonesiaImage, 1048, 545, beaches=True)

    papauNewGuineaImage = openImage("images/papauNewGuinea.png")
    papauNewGuinea = Territory(1212, 520, papauNewGuineaImage, 1150, 518,
                                                          beaches=True)

    westernAustraliaImage = openImage("images/westernAustralia.png")
    westernAustralia = Territory(1075, 660, westernAustraliaImage, 1089, 660,
                                                              beaches=True)

    easternAustraliaImage = openImage("images/easternAustralia.png")
    easternAustralia = Territory(1172, 650, easternAustraliaImage, 1175, 627)

    #assign oceanian neighbors
    indonesia.neighborsList.extend([westernAustralia, papauNewGuinea])
    papauNewGuinea.neighborsList.extend([indonesia, easternAustralia])
    westernAustralia.neighborsList.extend([indonesia, easternAustralia])
    easternAustralia.neighborsList.extend([westernAustralia, papauNewGuinea])

    #assign international neighbors
    alaska.neighborsList.append(russia4)
    greenland.neighborsList.append(iceland)
    mexico.neighborsList.append(colombia)
    colombia.neighborsList.append(mexico)
    brazil.neighborsList.append(westAfrica)
    iceland.neighborsList.append(greenland)
    spain.neighborsList.append(westAfrica)
    italy.neighborsList.extend([westAfrica, northAfrica, middleEast])
    easternEurope.neighborsList.extend([russia1, kazakhstan, middleEast])
    russia1.neighborsList.append(easternEurope)
    russia4.neighborsList.append(alaska)
    kazakhstan.neighborsList.append(easternEurope)
    middleEast.neighborsList.extend([easternEurope, italy, northAfrica,
                                     eastAfrica])
    southeastAsia.neighborsList.append(indonesia)
    westAfrica.neighborsList.extend([brazil, spain, italy])
    eastAfrica.neighborsList.append(middleEast)
    northAfrica.neighborsList.extend([italy, middleEast])
    indonesia.neighborsList.append(southeastAsia)

    app.board = Board([alaska, westernCanada, northernCanada, centralCanada,
                      easternCanada, greenland, westernUSA, easternUSA, mexico,
                      colombia, peru, brazil, argentina, iceland, britishIsles,
                      spain, germany, italy, easternEurope, scandanavia,
                      russia1, russia2, russia3, russia4, kazakhstan, mongolia,
                      northernChina, southernChina, japan, middleEast, india,
                      southeastAsia, westAfrica, eastAfrica, centralAfrica,
                      northAfrica, southAfrica, madagascar, indonesia,
                      papauNewGuinea, westernAustralia, easternAustralia])
    
def createNewBoard(app):
    createBoard(app)
    randomizeTerritories(app)

def explosionUpload(app):

#https://www.deviantart.com/fralexion/art/Ashey-Explosion-Sprite-Sheet-440151065
    explosionFullImage = openImage("images/explosionSpriteSheet.png")
    
    #algorithm of transferring spritesheet to list was taken from sprites.py
    #which was a file found in CMUGraphicsDemos and was posted on Piazza
    app.explosion = [explosionFullImage]
    for i in range(4):
        #only taking the sprites in the first column
        left = 30
        right = 125
        
        top = i * (512/4) + 20
        bottom = top + (512/4) - 22

        sprite = explosionFullImage.crop([left, top, right, bottom])

        #the following algorithm was inpired by "pixelEditing.py"
        #see territoryClass.py line 70 for full citation

        tempImage = Image.new(mode='RGBA', size=sprite.size)

        #fixes background transparency
        for x in range(sprite.width):
            for y in range(sprite.height):
                r,g,b,transparency = sprite.getpixel((x,y))
                if (transparency == 255): #the image is fully nontransparent
                    tempImage.putpixel((x,y),(r,g,b))

        sprite = CMUImage(tempImage) #convert to CMUImage
        app.explosion.append(sprite) #app.explosion is a list with all sprites

def loadDice(app):

    #https://www.freeiconspng.com/img/27656
    dice1image = openImage("images/1dice.png")
    #https://www.nicepng.com/ourpic/u2y3w7y3a9y3a9i
    #1_dice-png-background-pair-of-dice/
    dice2image = openImage("images/2dice.png")
    #https://snipstock.com/image/dice-png-images-3-png-78160
    dice3image = openImage("images/3dice.png")

    #list of all dice images in CMUImage form
    app.dice = [CMUImage(dice1image),CMUImage(dice2image),CMUImage(dice3image)]

def loadTroopPics(app):

    app.troopPics = []

    #all troop photos were cropped from this photo:
    #https://www.boardgamehalv.com/how-to-play-risk-board-game/

    #troop 1
    troop1blue = openImage("images/troop1.png")

    #the following algorithm (used 6 times) was inpired by "pixelEditing.py"
    #see territoryClass.py line 70 for full citation

    #change the color to a red for the troops facing right
    troop1right = Image.new(mode='RGBA', size=troop1blue.size)
    for x in range(troop1right.width):
        for y in range(troop1right.height):
            r,g,b, transparency = troop1blue.getpixel((x,y))
            if (transparency == 255): #the image is fully nontransparent
                troop1right.putpixel((x,y),(171,14,14))

    #change the color to a better blue to mimic the silhouette art style
    troop1left = Image.new(mode='RGBA', size=troop1blue.size)
    for x in range(troop1left.width):
        for y in range(troop1left.height):
            r,g,b, transparency = troop1blue.getpixel((x,y))
            if (transparency == 255): #the image is fully nontransparent
                troop1left.putpixel((x,y),(32,75,101))

    #the pictures are all stored in a list
    app.troopPics.append(CMUImage(troop1right.transpose(Image.FLIP_LEFT_RIGHT)))
    app.troopPics.append(CMUImage(troop1left))
    
    #troop 2
    troop2blue = openImage("images/troop2.png")

    #change the color to a red for the troops facing right
    troop2right = Image.new(mode='RGBA', size=troop2blue.size)
    for x in range(troop2right.width):
        for y in range(troop2right.height):
            r,g,b, transparency = troop2blue.getpixel((x,y))
            if (transparency == 255): #the image is fully nontransparent
                troop2right.putpixel((x,y),(171,14,14))

    #change the color to a better blue to mimic the silhouette art style
    troop2left = Image.new(mode='RGBA', size=troop2blue.size)
    for x in range(troop2left.width):
        for y in range(troop2left.height):
            r,g,b, transparency = troop2blue.getpixel((x,y))
            if (transparency == 255): #the image is fully nontransparent
                troop2left.putpixel((x,y),(32,75,101))

    #the pictures are all stored in a list
    app.troopPics.append(CMUImage(troop2right.transpose(Image.FLIP_LEFT_RIGHT)))
    app.troopPics.append(CMUImage(troop2left))

    #troop 3
    troop3blue = openImage("images/troop3.png")

    #change the color to a red for the troops facing right
    troop3right = Image.new(mode='RGBA', size=troop3blue.size)
    for x in range(troop3right.width):
        for y in range(troop3right.height):
            r,g,b, transparency = troop3blue.getpixel((x,y))
            if (transparency == 255): #the image is fully nontransparent
                troop3right.putpixel((x,y),(171,14,14))

    #change the color to a better blue to mimic the silhouette art style
    troop3left = Image.new(mode='RGBA', size=troop3blue.size)
    for x in range(troop3left.width):
        for y in range(troop3left.height):
            r,g,b, transparency = troop3blue.getpixel((x,y))
            if (transparency == 255): #the image is fully nontransparent
                troop3left.putpixel((x,y),(32,75,101))

    #the pictures are all stored in a list
    app.troopPics.append(CMUImage(troop3right.transpose(Image.FLIP_LEFT_RIGHT)))
    app.troopPics.append(CMUImage(troop3left))

def loadDeck(app):
    listOfNum = shuffle(list(range(42))) #0-41 in a random order

    app.deck = [] #no cards so far
    for i in range(42):
        #one card per territory, each card has a type of 0, 1, or 2
        app.deck.append(Card(listOfNum[i], i%3))

def shuffle(L):

    #swaps 50 random indices to randomize the list
    for i in range(50):
        i1 = random.randrange(42)
        i2 = random.randrange(42)
        temp = L[i1]
        L[i1] = L[i2]
        L[i2] = temp

    return L

def openImage(fileName):
        
    #this function was taken from basicPILMethods.py,
    #which was demoed in lecture and was sent to us via email
    #within a folder called CMUGraphicsDemos


    return Image.open(os.path.join(pathlib.Path(__file__).parent,fileName))

#this method assigns each territory to a random player
def randomizeTerritories(app):
    numTerritories = len(app.board.t)
    numPlayers = len(app.activePlayerList)
    currentPlayer = 1

    #create a new list that is a shallow copy
    #this allows the program to remove the territories from the copy one by one
    #while still being able to change the actual territories,
    #without affecting the main 
    boardCopy = copy.copy(app.board.t)

    #first, we need to find how many extra territories there will be
    #when every country gets the same number territories
    numExtraTerritories = numTerritories % numPlayers

    #each of these territories will be given to a random player
    while (numExtraTerritories > 0):
        randTerrNum= random.randrange(len(boardCopy)) #picks a random territory
        randTerr = boardCopy[randTerrNum]
        boardCopy.pop(randTerrNum)
        randPlayer = random.randrange(1, numPlayers+1)
        randTerr.setPlayer(randPlayer)
        randTerr.drawnCMUImage = CMUImage(randTerr.drawnImage)
        numExtraTerritories -= 1

    #now that there are a correct number of territories,
    #we will cycle through the players and assign them random territories 1 by 1
    while (len(boardCopy) > 0):
        randTerrNum = random.randrange(len(boardCopy)) #picks a random territory
        randTerr = boardCopy[randTerrNum]
        boardCopy.pop(randTerrNum)
        randTerr.setPlayer(currentPlayer)
        randTerr.drawnCMUImage = CMUImage(randTerr.drawnImage)

        #cycle through the players
        if (currentPlayer == numPlayers):
            currentPlayer = 1
        else:
            currentPlayer += 1



# --- MOUSE PRESS EVENTS ----------------------------------------------------



def onMousePress(app, mouseX, mouseY):

    #the main onMousePress function
    #just sends you to the correct helper function depending on game state

    if (app.startScreen):
        onStartScreenMousePress(app, mouseX, mouseY)
    elif (app.loadingScreen):
        onLoadingScreenMousePress(app, mouseX, mouseY)
    elif (app.winner != None):
        onEndScreenMousePress(app, mouseX, mouseY)
    elif (app.currentFight.existence or app.fightWon):
        ongoingFightMousePress(app, mouseX, mouseY)
    elif (app.readyToFortify):
        onReadyToFortifyMousePress(app, mouseX, mouseY)
    else:
        if (app.rules):
            app.rules = False #we're on the rules tab, so any click takes us out
        elif (distance(mouseX, mouseY, 1260, 740) <= 25):
            app.rules = True #the rules tab was clicked
        elif (app.phase == 1):
            onPhase1MousePress(app, mouseX, mouseY)
        elif (app.phase == 2):
            onPhase2MousePress(app, mouseX, mouseY)
        elif (app.phase == 3):
            onPhase3MousePress(app, mouseX, mouseY)

def onStartScreenMousePress(app, mouseX, mouseY):
    #if we selected new game, go to loading screen, which is how new game starts
    if (550 <= mouseX <= 750 and 335 <= mouseY <= 385):
        app.startScreen = False
        app.loadingScreen = True
    
    #if we selected load game, we need to read our save file
    elif (550 <= mouseX <= 750 and 455 <= mouseY <= 505):
        saveDataTxt = readFile('saveData.txt')

        #if there is nothing in the save file, there is no game to load
        #so simply do nothing

        #else, convert the text file to a dictionary and load our old game
        if (saveDataTxt != ''):
            app.startScreen = False
            saveData = ast.literal_eval(saveDataTxt)
            loadOldGame(app, saveData)

def onLoadingScreenMousePress(app, mouseX, mouseY):

    #3 player mode
    if (550 <= mouseX <= 750 and 335 <= mouseY <= 385):
        app.activePlayerList = [1,2,3]
        loadNewGame(app)

    #4 player mode
    elif (550 <= mouseX <= 750 and 395 <= mouseY <= 445):
        app.activePlayerList = [1,2,3,4]
        loadNewGame(app)

    #5 player mode
    elif (550 <= mouseX <= 750 and 455 <= mouseY <= 505):
        app.activePlayerList = [1,2,3,4,5]
        loadNewGame(app)

    #6 player mode
    elif (550 <= mouseX <= 750 and 515 <= mouseY <= 565):
        app.activePlayerList = [1,2,3,4,5,6]
        loadNewGame(app)

def ongoingFightMousePress(app, mouseX, mouseY):
    fight = app.currentFight #create a alias for easy access to the fight object

    #if the fight is just starting, choose the number of troops
    if (fight.numAttackers == None and not app.fightWon):
        #set attackers based on user choice
        if (500-70 <= mouseX <= 500+70 and 415-95 <= mouseY <= 415+95):
            fight.numAttackers = 1
        elif (fight.attackingTerr.numTroops > 2 and 
              650-70 <= mouseX <= 650+70 and 415-95 <= mouseY <= 415+95):
            fight.numAttackers = 2
        elif (fight.attackingTerr.numTroops > 3 and 
              800-70 <= mouseX <= 800+70 and 415-95 <= mouseY <= 415+95):
            fight.numAttackers = 3
    
    #if the fight is ready but hasn't happened yet, then do the fight
    if (fight.numAttackers != None and not app.fightWon):
        #set defenders
        if (fight.numAttackers == 1 or fight.defendingTerr.numTroops < 2):
            fight.numDefenders = 1
        else:
            fight.numDefenders = 2
        
        #roll the dice
        attackingRolls = []
        for i in range(fight.numAttackers):
            diceroll = random.randrange(1,7)
            attackingRolls.append(diceroll)
        defendingRolls = []
        for i in range(fight.numDefenders):
            diceroll = random.randrange(1,7)
            defendingRolls.append(diceroll)

        #fight

        #we want the highest roll, so we sort so that i = -1 gives the highest
        attackingRolls.sort()
        defendingRolls.sort()

        app.animationCounter = 3 #sets up the 3 frame explosion animation

        #for each pair, see who won
        for i in range(1, len(defendingRolls) + 1):
            index = -1 * i
            #defending territory wins
            if (defendingRolls[index] >= attackingRolls[index]):
                fight.attackingTerr.numTroops -= 1
                newAnimation = Animation(app.explosion,
                        fight.attackingTerr.textcx, fight.attackingTerr.textcy)
                #add the animation centered on the attacking terr in the list
                app.allAnimations.append(newAnimation)

            #attacking territory wins
            else:
                fight.defendingTerr.numTroops -= 1
                newAnimation = Animation(app.explosion,
                        fight.defendingTerr.textcx, fight.defendingTerr.textcy)
                #add the animation centered on the defending terr in the list
                app.allAnimations.append(newAnimation)

        #check for winner
        if (fight.defendingTerr.numTroops == 0):
            disputedTerr = fight.defendingTerr #alias of the territory that lost
            defendingPlayerNum = disputedTerr.player #save the losing playerNum
            disputedTerr.setPlayer(app.whoseTurn) #change the owner of the terr
            disputedTerr.drawnCMUImage = CMUImage(disputedTerr.drawnImage)
            disputedTerr.numTroops += 1
            fight.attackingTerr.numTroops -= 1

            #if there are troops to move, allow the user to move them
            if (fight.attackingTerr.numTroops > 1 or
                fight.defendingTerr.numTroops > 1):
                
                app.fightWon = True

                #designates which two territories to highlight
                app.fortifyTerr1 = fight.attackingTerr
                app.fortifyTerr2 = fight.defendingTerr

            #give a card
            if (app.giveCard):
                app.deck[app.topOfDeck].setPlayer(app.whoseTurn) #give top card
                app.topOfDeck = app.topOfDeck + 1
                app.giveCard = False

            #see if that player has been eliminated
            alive = False
            for territory in app.board.t:
                #if any remaining are still that player's, they are still alive
                if (territory.player == defendingPlayerNum):
                    alive = True

            #if alive is still False, that player is dead
            if (not alive):
                app.activePlayerList.remove(defendingPlayerNum)

                #reallocate cards
                for card in app.deck:
                    if (card.player == defendingPlayerNum):
                        card.setPlayer(app.whoseTurn)

                #see if this player has won
                if (len(app.activePlayerList) == 1):
                    app.winner = app.activePlayerList[0] #set winner

                    #clear data of some variables
                    writeFile('saveData.txt', '')
                    app.fortifyTerr1 = None
                    app.fortifyTerr2 = None
                    app.selectedTerr = False
                    app.message = ""
                    app.fightWon = False

        
        fight.reset() #always reset the fight object at the end of the fight

    #if the fight is over, allocate troops
    if (app.fightWon):
        app.message = "Move troops with arrow keys"
        app.cornerMessage = "Done"

        #only mouse press that matters is "Done" (move troops with arrow keys)
        if (945-90 <= mouseX <= 945+90 and 750-20 <= mouseY <= 750+20):
            app.message = f"Player {app.whoseTurn}: Attack!"
            app.cornerMessage = "End Phase"
            app.fightWon = False
            app.fortifyTerr1 = None
            app.fortifyTerr2 = None

def onReadyToFortifyMousePress(app, mouseX, mouseY):
    #only mouse press that matters in fortification is "End Turn"
    if (945-90 <= mouseX <= 945+90 and 750-20 <= mouseY <= 750+20):
        moveToNextTurn(app)

def onPhase1MousePress(app, mouseX, mouseY):
    #territoryClicked is a reference to the actual territory that was clicked
    territoryClicked = whichTerritoryClicked(app, mouseX, mouseY)

    #if a valid territory was clicked, then place a troop there
    if (territoryClicked != None and territoryClicked.player == app.whoseTurn):
        territoryClicked.numTroops += 1
        app.placeTroopsNum -= 1

        #if there are no more troops left to place, then move to next phase
        if (app.placeTroopsNum == 0):
            app.phase = 2
            app.selectedTerr = None
            app.message = f'Player {app.whoseTurn}: Attack!'

        #final troop has a special message
        elif (app.placeTroopsNum == 1):
            app.message = f'Player {app.whoseTurn}: Place your final troop'
        
        #prompt the user to place troops
        else:
            app.message = (
        f'Player {app.whoseTurn}: Place your {app.placeTroopsNum} troops')

def onPhase2MousePress(app, mouseX, mouseY):
    #if "Done" is pressed, the phase is over
    if (945-90 <= mouseX <= 945+90 and 750-20 <= mouseY <= 750+20):
        app.phase = 3
        app.message = f'Player {app.whoseTurn}: Fortify your troops'
        app.cornerMessage = "End Turn"

    
    #ATTACK LOGIC
    selectedTerritory = whichTerritoryClicked(app, mouseX, mouseY)

    #the click was on no territory
    if (selectedTerritory == None):
        app.selectedTerr = None
    #the click was on their own territory
    elif (selectedTerritory.player == app.whoseTurn):
        #this territory is eligible to attack
        if (selectedTerritory.numTroops > 1):
            app.selectedTerr = selectedTerritory
        else:
            app.selectedTerr = None
    #the click was on an opponent's territory
    else:
        attackingTerr = app.selectedTerr
        defendingTerr = selectedTerritory
        #if an attacking terr is selected and these territories border, fight
        if (app.selectedTerr!=None and app.selectedTerr.player == app.whoseTurn 
                    and doTerritoriesBorder(app, attackingTerr, defendingTerr)):
            fight(app, attackingTerr, defendingTerr)
        app.selectedTerr = None
    
def onPhase3MousePress(app, mouseX, mouseY):
    #if "Done" is pressed, the phase is over
    if (945-90 <= mouseX <= 945+90 and 750-20 <= mouseY <= 750+20):
        moveToNextTurn(app)

    #FORTIFY LOGIC
    selectedTerritory = whichTerritoryClicked(app, mouseX, mouseY)

    #the click was on no territory or an opponent's territory
    if (selectedTerritory == None or selectedTerritory.player != app.whoseTurn):
        app.selectedTerr = None
    #the click was on their own territory
    else:
        #if no selected territory, then this is it
        if (app.selectedTerr == None):
            app.selectedTerr = selectedTerritory
        #if there is a selected terr, check to see if they connect and fortify
        else:
            if (territoriesAreConnected(app.selectedTerr, selectedTerritory)):
                app.message = "Move troops with arrow keys"
                app.readyToFortify = True
                app.fortifyTerr1 = app.selectedTerr
                app.fortifyTerr2 = selectedTerritory
            #if not connected, that is the new starting terr
            else:
                app.selectedTerr = selectedTerritory

def onEndScreenMousePress(app, mouseX, mouseY):
    #pressing the screen after the game is over does nothing
    #the only way to do anything after the game is over is pressing 'n'
    pass



# --------- HELPER FUNCTIONS -----------------------------------------



def whichTerritoryClicked(app, mouseX, mouseY):
    #returns the territory that was clicked on, or None if no terr was clicked
    for territory in app.board.t:
        if (distance(mouseX, mouseY, territory.textcx, territory.textcy) < 40):
            return territory

def distance(x1, y1, x2, y2):
    return ((x2-x1)**2 + (y2-y1)**2)**0.5

def calculateTroopsToPlace(app):
    availTroops = 0
    occupiedTerritories = 0

    #count territories
    for territory in app.board.t:
        if (territory.player == app.whoseTurn):
            occupiedTerritories += 1

    #add troops accordingly
    if (occupiedTerritories < 9):
        availTroops = 3
    else:
        availTroops = occupiedTerritories//3
    
    #check for continent bonus and add troops accordingly
    continentBonus = calculateContinentBonus(app)
    availTroops += continentBonus

    #check for continent bonus and add troops accordingly
    cardBonus = 0
    keepChecking = True
    while (keepChecking):
        #check for sets finds only one set at a time
        #once it finds no sets, we will leave the loop
        extraBonus, keepChecking = checkForSets(app)
        cardBonus += extraBonus
        
    availTroops += cardBonus

    return availTroops

def calculateContinentBonus(app):
    #check each continent
    currentBonus = 0

    #North America
    NAcount = 0
    for i in range(0, 9): #e.g. the first 9 territories are in north america
        territory = app.board.t[i]
        if (territory.player == app.whoseTurn):
            NAcount += 1
        else:
            break

    #add to score
    if (NAcount == 9):
        currentBonus += 5
    

    #South America
    SAcount = 0
    for i in range(9, 13):
        territory = app.board.t[i]
        if (territory.player == app.whoseTurn):
            SAcount += 1
        else:
            break

    #add to score
    if (SAcount == 4):
        currentBonus += 2

    #Europe
    Europecount = 0
    for i in range(13, 20):
        territory = app.board.t[i]
        if (territory.player == app.whoseTurn):
            Europecount += 1
        else:
            break

    #add to score
    if (Europecount == 7):
        currentBonus += 5

    #Asia
    Asiacount = 0
    for i in range(20, 32):
        territory = app.board.t[i]
        if (territory.player == app.whoseTurn):
            Asiacount += 1
        else:
            break

    #add to score
    if (Asiacount == 12):
        currentBonus += 7

    #Asia
    Africacount = 0
    for i in range(32, 38):
        territory = app.board.t[i]
        if (territory.player == app.whoseTurn):
            Africacount += 1
        else:
            break

    #add to score
    if (Africacount == 6):
        currentBonus += 3

    #Oceania
    Oceaniacount = 0
    for i in range(38, 42):
        territory = app.board.t[i]
        if (territory.player == app.whoseTurn):
            Oceaniacount += 1
        else:
            break

    #add to score
    if (Oceaniacount == 4):
        currentBonus += 2

    return currentBonus

def checkForSets(app):
    myCardsCount = [(0, []), (0, []), (0, [])] #type0, type1, and type2 cards
                                            #and the associated card positions

    #see how many cards of each type you have
    for i in range(42):
        card = app.deck[i]
        if (card.player == app.whoseTurn):
            oldNumCards, cardPos = myCardsCount[card.type]
            newNumCards = oldNumCards + 1
            cardPos.append(i)
            myCardsCount[card.type] = (newNumCards, cardPos)

    #see if you have enough to complete a set
    for i in range(3):
        numCards, cardPos = myCardsCount[i]
        if (numCards >= 3):
            #these are the cards being traded in
            card1 = app.deck[cardPos[0]]
            card2 = app.deck[cardPos[1]]
            card3 = app.deck[cardPos[2]]

            #reset the cards and place them at the bottom of the deck
            card1.setPlayer(0)
            card2.setPlayer(0)
            card3.setPlayer(0)
            app.deck.extend([card1, card2, card3])

            #check for territory bonus nad apply when applicable
            if (app.board.t[card1.terr].player == app.whoseTurn):
                app.board.t[card1.terr].numTroops += 2
            if (app.board.t[card2.terr].player == app.whoseTurn):
                app.board.t[card2.terr].numTroops += 2
            if (app.board.t[card3.terr].player == app.whoseTurn):
                app.board.t[card3.terr].numTroops += 2

            #calculate bonus
            app.setsTurnedIn += 1
            if (app.setsTurnedIn <= 5):
                return 2*app.setsTurnedIn + 2, True
            else:
                return 5*(app.setsTurnedIn-3), True

            

    #if the code reached here, then no bonus, and stop checking
    return 0, False

def doTerritoriesBorder(app, terr1, terr2):
    if (terr2 in terr1.neighborsList):
        return True
    else:
        return False

#uses backtracking to see if territories are connected
def territoriesAreConnected(terr1, terr2):
    
    #using a helper function, where the path starts at terr1
    potentialPath = findAPath(terr1, terr2, [terr1])
    
    if (potentialPath != None):
        return True
    else:
        return False
    
def findAPath(start, end, path):
    print('')
    print('')
    print('')
    for terr in path:
        print(f'({terr.textcx}, {terr.textcy})')
        
    #base case - if our end goal is in the path, then that is the path we want
    if (end in path):
        return path
    
    #backtracking algorithm
    else:
        for borderTerr in start.neighborsList: #check each neighbor
            #if that neighbor is also your territory,
            #and we haven't gone there yet in our path,
            #then let's check this road
            if (borderTerr.player == start.player and borderTerr not in path):
                path.append(borderTerr)

                #recursively try to find a path from this new starting point
                solution = findAPath(borderTerr, end, path)

                #if we found a solution, then return that path
                if (solution != None):
                    return solution
                
                #no solution, so undo the move
                path.pop(-1)

                #keeping trying to find a solution.
                #if there's no solution down this path, return None
        return None

def fight(app, attackingTerr, defendingTerr):
    fight = app.currentFight #creates an alias for easy access

    #fight screen
    fight.existence = True
    
    #load territories
    fight.attackingTerr = attackingTerr
    fight.defendingTerr = defendingTerr

def moveToNextTurn(app):

    app.readyToFortify = False #done with fortification

    #no teritories are selected to start a turn
    app.selectedTerr = None
    app.fortifyTerr1 = None
    app.fortifyTerr2 = None

    app.phase = 1

    #go to next player
    currentPlayerIndex = app.activePlayerList.index(app.whoseTurn)
    nextPlayerIndex = (currentPlayerIndex + 1) % len(app.activePlayerList)
    app.whoseTurn = app.activePlayerList[nextPlayerIndex]


    #getting ready for next round
    app.placeTroopsNum = calculateTroopsToPlace(app)
    app.message = (
    f'Player {app.whoseTurn}: Place your {app.placeTroopsNum} troops')

    #the next person can recieve a card if there are any left
    if (app.topOfDeck < len(app.deck)):
        app.giveCard = True

    #save data from this turn to a text file (idea learned from class notes)
    saveData = dict()

    #save the player and troop number of each territory
    for i in range(len(app.board.t)):
        territory = app.board.t[i]
        saveData[f'terr {i}: player'] = territory.player
        saveData[f'terr {i}: numTroops'] = territory.numTroops

    #save each card type and who owns them
    for i in range(len(app.deck)):
        card = app.deck[i]
        saveData[f'card {i}: terr'] = card.terr
        saveData[f'card {i}: type'] = card.type
        saveData[f'card {i}: player'] = card.player
    
    #length of deck grows when cards are turned in, so we need to save deck len
    saveData['deckLength'] = len(app.deck)

    #also save other data related to the deck
    saveData['topOfDeck'] = app.topOfDeck
    saveData['setsTurnedIn'] = app.setsTurnedIn
    saveData['giveCard'] = app.giveCard

    #save who is still in the game and whose turn it is
    saveData['activePlayersList'] = app.activePlayerList
    saveData['whose turn'] = app.whoseTurn

    #write this all down in our text file
    writeFile('saveData.txt', repr(saveData))

def readFile(path):

    #this function was taken from the 15-112 course website under
    #"Class Notes: Strings -- 12. Basic IO"

    with open(path, "rt") as f:
        return f.read()

def writeFile(path, contents):

    #this function was taken from the 15-112 course website under
    #"Class Notes: Strings -- 12. Basic IO"

    with open(path, "wt") as f:
        f.write(contents)

# --- KEY PRESS EVENTS ----------------------------------------------------



def onKeyPress(app, key):
    #pressing 'n' at any time starts a new game by going to the loading screen
    if (key == 'n'):
        app.loadingScreen = True

    #at the end of a fight or during fortification, arrow keys can move troops
    if (app.fightWon or app.readyToFortify):
        if ((key == 'up' or key == 'right') and
                            app.fortifyTerr1.numTroops > 1):
            app.fortifyTerr1.numTroops -= 1
            app.fortifyTerr2.numTroops += 1
        if ((key == 'down' or key == 'left') and
                            app.fortifyTerr2.numTroops > 1):
            app.fortifyTerr2.numTroops -= 1
            app.fortifyTerr1.numTroops += 1

        #enter can end the troop movement process
        if (key == 'enter'):
            if (app.fightWon):
                app.message = f"Player {app.whoseTurn}: Attack!"
                app.cornerMessage = "End Phase"
                app.fightWon = False
                app.fortifyTerr1 = None
                app.fortifyTerr2 = None
            else:
                moveToNextTurn(app)




# --- TIMER EVENTS ---------------------------------------------------------



def onStep (app):
    #if there is an animation to run, the animation counter will be >0
    if (app.animationCounter > 0):
        app.animationCounter -= 1
    else: #if the counter is at 0, empty the animation list
        app.allAnimations = []




# --- GRAPHICS ----------------------------------------------------



def redrawAll(app):

    #redrawAll calls different helper functions depending on the game state

    if (app.startScreen):
        drawStartScreen(app)
    elif (app.loadingScreen):
        drawLoadingScreen(app)
    elif (app.rules):
        drawRules(app)
    else:
        drawBoard(app)

        #the end screen and fight screen go on top of the board
        if (app.winner != None):
            drawEndScreen(app)
        elif (app.currentFight.existence):
            drawFightScreen(app)

    drawAnimation(app) #only draws if any animations exist

def drawStartScreen(app):
    
    drawScreenSaver(app) #draws the logo and the troops in the background

    drawRect(650, 360, 200, 50, border='black', fill='gold', align='center')
    drawLabel("New Game", 650, 360, size=25, bold=True)

    drawRect(650, 480, 200, 50, border='black', fill='gold', align='center')
    drawLabel("Load Game", 650, 480, size=25, bold=True)

def drawLoadingScreen(app):

    drawScreenSaver(app) #draws the logo and the troops in the background

    drawLabel("How many players?", 650, 300, size=25, bold=True)

    drawRect(650, 360, 200, 50, border='black', fill='gold', align='center')
    drawLabel("3 players", 650, 360, size=25, bold=True)

    drawRect(650, 420, 200, 50, border='black', fill='gold', align='center')
    drawLabel("4 players", 650, 420, size=25, bold=True)

    drawRect(650, 480, 200, 50, border='black', fill='gold', align='center')
    drawLabel("5 players", 650, 480, size=25, bold=True)

    drawRect(650, 540, 200, 50, border='black', fill='gold', align='center')
    drawLabel("6 players", 650, 540, size=25, bold=True)

def drawScreenSaver(app):

    #draw background color
    grad = gradient('white', 'orange')
    drawRect(0, 0, 1300, 780, fill=grad, opacity=30)
    drawLabel("RISK112", 650, 50, size=75, bold=True)

    #draw troops

    #left infantry
    for i in range(36):
        drawImage(app.troopPics[0], 80+50*(i//9), 126+70*(i%9)-12*(i//9),
                                                        width=200, height=75)
        
    #left cavalry
    for i in range(7):
        drawImage(app.troopPics[2], -100+100*(i//4), 80+130*(i%4)+50*(i//4),
                                                        width=300, height=112)

    #left cannons
    for i in range(3):
        drawImage(app.troopPics[4], 100-100*(i//2), 640-130*(i%2)-50*(i//2),
                                                        width=300, height=112)

    #right infantry
    for i in range(36):
        drawImage(app.troopPics[1], 870+50*(i//9), 90+70*(i%9)+12*(i//9),
                                                        width=200, height=75)

    #right cavalry
    for i in range(7):
        drawImage(app.troopPics[3], 1100-100*(i//4), 80+130*(i%4)+50*(i//4),
                                                        width=300, height=112)

    #right cannons
    drawImage(app.troopPics[5], 900, 650, width=300, height=112)
    drawImage(app.troopPics[5], 900, 520, width=300, height=112)
    drawImage(app.troopPics[5], 1000, 590, width=300, height=112)

def drawBoard(app):

    #giving the board a weathered look
    grad = gradient('orange', 'white', 'orange', start='left-top')
    drawRect(0, 0, 1300, 780, fill=grad, opacity=30)

    color = 'black'

    #drawing each territory
    for territory in app.board.t:
        drawTerritory(app, territory)

        #find the color of the current player for the text
        if (territory.player == app.whoseTurn):
            color = territory.playerColor

        drawSeaRoutes(app) #draw the sea lines many times to match the art style
    
    #draw the appropriate message
    if (app.phase == 1):
        drawLabel(app.message, 650, 750, size=40, bold=True, fill=color)
    else:
        drawLabel(app.message, 500, 750, size=40, bold=True, fill=color)
        drawRect(945, 750, 180, 40, border='black', fill=None, align='center')
        drawLabel(app.cornerMessage, 945, 750, bold=True, size=30)

    #draw logo
    drawLabel("RISK112", 120, 745, size=50, bold=True, fill='fireBrick',
                                    border='black', borderWidth=4)
    drawStar(60, 700, 25, 5, fill='silver', border='black', borderWidth=3)
    drawStar(120, 700, 25, 5, fill='silver', border='black', borderWidth=3)
    drawStar(180, 700, 25, 5, fill='silver', border='black', borderWidth=3)

    #draw ocean names
    drawLabel("Pacific Ocean", 100, 447, size=20, bold=True, italic=True)
    drawLabel("Atlantic Ocean", 418, 313, size=20, bold=True, italic=True)
    drawLabel("Indian Ocean", 916, 581, size=20, bold=True, italic=True)
    drawLabel("Arctic Ocean", 650, 33, size=20, bold=True, italic=True)
    drawLabel("Pacific Ocean", 1195, 420, size=20, bold=True, italic=True)

    #draw compass (center of compass is at 507, 602)
    x, y = 507, 602
    drawCircle(x, y, 25, fill=None, border='red', borderWidth=10)
    drawCircle(x, y, 25, fill=None, border='black')
    drawCircle(x, y, 15, fill=None, border='black')

    drawPolygon(x-20, y-20, x, y-7, x-7, y)
    drawPolygon(x+20, y-20, x, y-7, x+7, y)
    drawPolygon(x-20, y+20, x, y+7, x-7, y)
    drawPolygon(x+20, y+20, x, y+7, x+7, y)

    drawPolygon(x, y-40, x, y, x-7, y-7, fill='silver')
    drawPolygon(x, y-40, x, y, x+7, y-7)
    drawPolygon(x+40, y, x, y, x+7, y-7, fill='silver')
    drawPolygon(x+40, y, x, y, x+7, y+7)
    drawPolygon(x, y+40, x, y, x+7, y+7, fill='silver')
    drawPolygon(x, y+40, x, y, x-7, y+7)
    drawPolygon(x-40, y, x, y, x-7, y+7, fill='silver')
    drawPolygon(x-40, y, x, y, x-7, y-7)
    
    drawLabel("N", x, y-60, size=24, bold=True)
    drawLabel("W", x-60, y, size=24, bold=True)
    drawLabel("S", x, y+60, size=24, bold=True)
    drawLabel("E", x+60, y, size=24, bold=True)

    #rules tab
    drawCircle(1260, 740, 25, fill=None, border='black', borderWidth=5)
    drawLabel('?', 1260, 740, size=30, bold=True)

def drawTerritory(app, territory):
    #highlights the number if appropriate
    if (territory == app.selectedTerr or territory == app.fortifyTerr1
                                      or territory == app.fortifyTerr2):
        color = 'yellow'
    else:
        color = None

    drawImage(territory.drawnCMUImage, territory.cx, territory.cy,
                                                        align='center')
    drawCircle(territory.textcx, territory.textcy, 20, opacity=75, fill=color)
    drawLabel(str(territory.numTroops), territory.textcx, territory.textcy,
                                                  size=24, bold=True)
    
def drawSeaRoutes(app):

    #these lines show territories that 'border' each other through sea routes
    drawLine(420, 470, 558, 449, dashes=True)
    drawLine(359, 80, 290, 70, dashes=True)
    drawLine(359, 80, 323, 114, dashes=True)
    drawLine(516, 91, 549, 109, dashes=True)
    drawLine(570, 260, 575, 275, dashes=True)
    drawLine(597, 151, 580, 176, dashes=True)
    drawLine(580, 176, 623, 162, dashes=True)
    drawLine(580, 176, 635, 212, dashes=True)
    drawLine(623, 121, 650, 111, dashes=True)
    drawLine(698, 374, 702, 392, dashes=True)
    drawLine(583, 382, 586, 384, dashes=True)
    drawLine(716, 329, 713, 326, dashes=True)
    drawLine(712, 332, 711, 331, dashes=True)
    drawLine(795, 476, 800, 472, dashes=True)
    drawLine(842, 631, 811, 569, dashes=True)
    drawLine(804, 679, 772, 689, dashes=True)
    drawLine(1155, 242, 1108, 259, dashes=True)
    drawLine(1155, 242, 1121, 206, dashes=True)
    drawLine(1091, 593, 1084, 587, dashes=True)
    drawLine(1082, 504, 1098, 505, dashes=True)
    drawLine(1076, 500, 1066, 475, dashes=True)
    drawLine(1115, 523, 1128, 565, dashes=True)
    drawLine(1213, 79, 1294, 59, dashes=True)
    drawLine(26, 79, 4, 64, dashes=True)

def drawFightScreen(app):

    #this is drawn on top of the board
    drawRect(650, 390, 500, 300, fill='red', align='center')
    if (app.currentFight.numAttackers == None): #confirming there is a fight
        drawTroopSelection(app)

def drawTroopSelection(app):
    drawLabel("Select your army size", 650, 265, size=40, bold=True)

    #1 troop
    drawRect(500, 415, 140, 190, fill=None, border='black', align='center')
    drawLabel("1 troop", 500, 340, size=34, bold=True)
    drawImage(app.dice[0], 500, 430, width=100, height=100, align='center')

    #2 troops
    if (app.currentFight.attackingTerr.numTroops > 2):
        drawRect(650, 415, 140, 190, fill=None, border='black', align='center')
        drawLabel("2 troops", 650, 340, size=34, bold=True)
        drawImage(app.dice[1], 650, 430, width=100, height=100, align='center')

    #3 troops
    if (app.currentFight.attackingTerr.numTroops > 3):
        drawRect(800, 415, 140, 190, fill=None, border='black', align='center')
        drawLabel("3 troops", 800, 340, size=34, bold=True)
        drawImage(app.dice[2], 800, 430, width=100, height=100, align='center')

def drawAnimation(app):

    #draw each animation in the list (usually the list is empty)
    for animation in app.allAnimations:
        numSprites = len(animation.img) - 1

        #draws the correct sprite based on the animation counter

        img = animation.img[numSprites-app.animationCounter]
        drawImage(img, animation.cx, animation.cy, align='center')

def drawEndScreen(app):
    
    #this is drawn on top of the board

    color = app.board.t[0].playerColor #tint the screen the color of the winner
    drawRect(0, 0, app.width, app.height, fill=color, opacity=50)
    drawLabel(f"Player {app.winner} wins!!", 650, 375, size=100)
    drawLabel("Press 'n' to start a new game", 650, 600, size=50, bold=True)

def drawRules(app):
    drawRect(0, 0, app.width, app.height, fill='red')

    #'X' in the top corner
    drawLine(1260, 10, 1290, 40)
    drawLine(1290, 10, 1260, 40)

    #phase 1
    text1 = "Phase 1: Deploy"
    text2 = "In this phase, you recieve"
    text3 = "a certain amount of troops"
    text4 = "to place in your territories."

    text5 = "To place a troop,"
    text6 = "click on the middle"
    text7 = "of the territory."

    text8 = "Once you finish placing troops,"
    text9 = "you will automatically"
    text10 = "move on the the next phase."""

    drawLabel(text1, 150, 50, size=30, bold=True)
    drawLabel(text2, 50, 100, size=20, bold=True, align='left')
    drawLabel(text3, 50, 120, size=20, bold=True, align='left')
    drawLabel(text4, 50, 140, size=20, bold=True, align='left')
    drawLabel(text5, 50, 170, size=20, bold=True, align='left')
    drawLabel(text6, 50, 190, size=20, bold=True, align='left')
    drawLabel(text7, 50, 210, size=20, bold=True, align='left')
    drawLabel(text8, 50, 240, size=20, bold=True, align='left')
    drawLabel(text9, 50, 260, size=20, bold=True, align='left')
    drawLabel(text10, 50, 280, size=20, bold=True, align='left')


    #side bar - gaining troops
    text1 = "How do I get more troops to deploy?"

    text2 = "The number of troops that you get"
    text3 = "to deploy at the start of your turn"
    text4 = "is based on 3 things."

    text5 = "First, you get 1 troop"
    text6 = "for every 3 territories you control."

    text7 = "Second, you get a bonus if you"
    text8 = "control every territory in a continent."
    text9 = "This bonus spans from 2 troops"
    text10 = "for South America to 7 troops for Asia."

    text11 = "Finally, if you have a set of three"
    text12 = "cards that match, you get a troop bonus"
    text13 = "that increases as the game goes on."
    text14 = "Cards are handled internally in this game"
    text15 = "and are applied automatically, but"
    text16 = "it's important to note that you only get"
    text17 = "a card after your turn if you defeated"
    text18 = "at least one territory that round."

    drawLine(0, 340, 375, 340)
    drawLine(375, 340, 375, 540)
    drawLine(375, 540, 425, 540)
    drawLine(425, 540, 425, 780)
    drawLabel(text1, 185, 365, size=20, bold=True)
    drawLabel(text2, 25, 410, size=20, bold=True, align='left')
    drawLabel(text3, 25, 430, size=20, bold=True, align='left')
    drawLabel(text4, 25, 450, size=20, bold=True, align='left')
    drawLabel(text5, 25, 480, size=20, bold=True, align='left')
    drawLabel(text6, 25, 500, size=20, bold=True, align='left')
    drawLabel(text7, 25, 530, size=20, bold=True, align='left')
    drawLabel(text8, 25, 550, size=20, bold=True, align='left')
    drawLabel(text9, 25, 570, size=20, bold=True, align='left')
    drawLabel(text10, 25, 590, size=20, bold=True, align='left')
    drawLabel(text11, 25, 620, size=20, bold=True, align='left')
    drawLabel(text12, 25, 640, size=20, bold=True, align='left')
    drawLabel(text13, 25, 660, size=20, bold=True, align='left')
    drawLabel(text14, 25, 680, size=20, bold=True, align='left')
    drawLabel(text15, 25, 700, size=20, bold=True, align='left')
    drawLabel(text16, 25, 720, size=20, bold=True, align='left')
    drawLabel(text17, 25, 740, size=20, bold=True, align='left')
    drawLabel(text18, 25, 760, size=20, bold=True, align='left')
    


    #phase 2
    text1 = "Phase 2: Attack"

    text2 = "When it's your turn to attack, first select"
    text3 = "which of your territories you wish to attack with."

    text4 = "Once the number in your territory gets highlighted,"
    text5 = "select a bordering territory to attack"
    text6 = "(dotted line sea routes also count as borders)."

    text7 = "You will be prompted to select an amount of dice to roll."
    text8 = "Once you select an option,"
    text9 = "you and the defending territory both roll."

    text10 = "The highest die from each group"
    text11 = "(and second highest, if applicable) get matched up,"
    text12 = "and the higher die wins the battle."
    text13 = "Tie goes to the defender."

    text14 = "If you successfully take over a territory,"
    text15 = "you will have the option to move"
    text16 = "more troops into that area."
    text17 = "You can do this with the arrow keys."
    text18 = "You must press 'Done' to continue on with your attack."
    
    text19 = "Once you are done attacking,"
    text20 = "click 'End phase' to move on to fortification"
    
    drawLabel(text1, 625, 50, size=30, bold=True)
    drawLabel(text2, 400, 100, size=20, bold=True, align='left')
    drawLabel(text3, 400, 120, size=20, bold=True, align='left')
    drawLabel(text4, 400, 150, size=20, bold=True, align='left')
    drawLabel(text5, 400, 170, size=20, bold=True, align='left')
    drawLabel(text6, 400, 190, size=20, bold=True, align='left')
    drawLabel(text7, 400, 220, size=20, bold=True, align='left')
    drawLabel(text8, 400, 240, size=20, bold=True, align='left')
    drawLabel(text9, 400, 260, size=20, bold=True, align='left')
    drawLabel(text10, 400, 290, size=20, bold=True, align='left')
    drawLabel(text11, 400, 310, size=20, bold=True, align='left')
    drawLabel(text12, 400, 330, size=20, bold=True, align='left')
    drawLabel(text13, 400, 350, size=20, bold=True, align='left')
    drawLabel(text14, 400, 380, size=20, bold=True, align='left')
    drawLabel(text15, 400, 400, size=20, bold=True, align='left')
    drawLabel(text16, 400, 420, size=20, bold=True, align='left')
    drawLabel(text17, 400, 440, size=20, bold=True, align='left')
    drawLabel(text18, 400, 460, size=20, bold=True, align='left')
    drawLabel(text19, 400, 490, size=20, bold=True, align='left')
    drawLabel(text20, 400, 510, size=20, bold=True, align='left')

    #phase 3
    text1 = "Phase 3: Fortify"

    text2 = "In this phase, you have the option"
    text3 = "to move some of your troops to"
    text4 = "a more advantageous position."
    
    text5 = "First, select the territory that"
    text6 = "you wish to move troops from."
    
    text7 = "Next, select the territory that"
    text8 = "you wish to move troops to."
    
    text9 = "There must be a safe path"
    text10 = "(through all friendly territory)"
    text11 = "to transport your troops."

    drawLabel(text1, 1100, 50, size=30, bold=True)
    drawLabel(text2, 950, 100, size=20, bold=True, align='left')
    drawLabel(text3, 950, 120, size=20, bold=True, align='left')
    drawLabel(text4, 950, 140, size=20, bold=True, align='left')
    drawLabel(text5, 950, 170, size=20, bold=True, align='left')
    drawLabel(text6, 950, 190, size=20, bold=True, align='left')
    drawLabel(text7, 950, 220, size=20, bold=True, align='left')
    drawLabel(text8, 950, 240, size=20, bold=True, align='left')
    drawLabel(text9, 950, 270, size=20, bold=True, align='left')
    drawLabel(text10, 950, 290, size=20, bold=True, align='left')
    drawLabel(text11, 950, 310, size=20, bold=True, align='left')


    #side bar - how to win
    text1 = "How do I win?"

    text2 = "The goal of RISK112 is"
    text3 = "WORLD DOMINATION."

    text4 = "The first player"
    text5 = "to control every territory"
    text6 = "in the world"
    text7 = "will be deemed the winner."

    drawLine(950, 400, 1300, 400)
    drawLine(950, 400, 950, 780)
    drawLabel(text1, 1125, 425, size=20, bold=True)
    drawLabel(text2, 975, 470, size=20, bold=True, align='left')
    drawLabel(text3, 975, 490, size=20, bold=True, align='left')
    drawLabel(text4, 975, 520, size=20, bold=True, align='left')
    drawLabel(text5, 975, 540, size=20, bold=True, align='left')
    drawLabel(text6, 975, 560, size=20, bold=True, align='left')
    drawLabel(text7, 975, 580, size=20, bold=True, align='left')

    #draw logo
    drawLabel("RISK112", 650, 670, size=50, bold=True, fill='fireBrick',
                                    border='black', borderWidth=4)
    drawStar(590, 625, 25, 5, fill='silver', border='black', borderWidth=3)
    drawStar(650, 625, 25, 5, fill='silver', border='black', borderWidth=3)
    drawStar(710, 625, 25, 5, fill='silver', border='black', borderWidth=3)


# ------------------------------------------------------------------------



#run the code
def main():
    runApp()

main()