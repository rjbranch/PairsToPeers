#Things marked as important, including those which should potentially be changed down the line, are marked with "#NOTE"

import random
import math
import datetime
import time

import pygame, eztext
import pygame.mixer

from textrect import *

pygame.init()

#Loads in all of the fonts used by the game
font = pygame.font.SysFont(None, 25)
answer_card_font = pygame.font.Font('fonts/OpenSans-Regular.ttf', 16)
scenario_card_font = pygame.font.Font('fonts/OpenSans-Regular.ttf', 32)
big_bold_font = pygame.font.Font('fonts/OpenSans-Bold.ttf', 36)
bigger_bold_font = pygame.font.Font('fonts/OpenSans-Bold.ttf', 48)

#Initializes the mixer and loads in all of the sounds used by the game
pygame.mixer.init()
sound_blop = pygame.mixer.Sound('sound/Blop-Mark_DiAngelo-79054334_CHOPPED.ogg')
sound_applause = pygame.mixer.Sound('sound/Auditorium_Applause_CHOPPED.ogg')

#In the following section, a number of constants are defined.
#These variables have self explanatory names, and are referred to throughout the rest of the code but never change in value.
#Editing these values in the code can change various aspects of the gameplay, like the player's speed.
COLOR_RED = (255,0,0)
COLOR_GREEN = (0,255,0)
COLOR_BLUE = (0,0,255)
COLOR_LIGHTPINK = (255,225,255)
COLOR_LIGHTGREEN = (204,255,204)
COLOR_LIGHTBLUE = (204, 225, 255)
COLOR_WHITE = (255,255,255)
COLOR_BLACK = (0,0,0)
COLOR_POINTS_0 = (204,0,0)
COLOR_POINTS_1 = (204,44,0)
COLOR_POINTS_2 = (204,84,0)
COLOR_POINTS_3 = (204,124,0)
COLOR_POINTS_4 = (204,164,0)
COLOR_POINTS_5 = (204,204,0)
COLOR_POINTS_6 = (164,204,0)
COLOR_POINTS_7 = (124,204,0)
COLOR_POINTS_8 = (84,204,0)
COLOR_POINTS_9 = (44,204,0)
COLOR_POINTS_10 = (0,204,0)
GAME_WIDTH = 1024
GAME_HEIGHT = 768
FRAMES_PER_SECOND = 30
ANSWERS_PER_PLAYER = 2 #The number of answer cards that each player will have at any given time.  Currently set to 2 just because I don't have many answer cards written.
GOOD_CARD_POINTS = 6
POINTS_TO_WIN = 100
startTime = 0
#The rest of these constants relate specifically to the locations of images on the game screen.  Tweaking with these could definitely mess up how everything looks.

#Main Menu
POS_BOTTOMCORNER = (0, 512)
POS_TOPCORNER = (768, 0)
POS_LOGO = (180, 60)
POS_PLAYGAME = (90, 450)
POS_HOWTOPLAY = (390, 450)
POS_OPTIONS = (690, 450)

#INSTRUCTIONS
POS_HEADER_INSTRUCTIONS = (400, 30)
POS_DESC_SCENARIO = (90, 130)
RECT_DESC_SCENARIO = pygame.Rect(90, 180, 754, 80)
POS_DESC_RESPONSE = (90, 250)
RECT_DESC_RESPONSE = pygame.Rect(90, 300, 754, 110)
POS_DESC_CHOICE = (90,400)
RECT_DESC_CHOICE = pygame.Rect(90, 450, 754, 110)
POS_DESC_SCORE = (90,550)
RECT_DESC_SCORE = pygame.Rect(90, 600, 754, 110)
stringDescScenario = "At the start of each turn a scenario, describing a situation you might experience on a daily basis, will be revealed . Your task is to respond to this scenario card using an appropriate response card."
stringDescResponse = "You will be dealt 5 random response cards every time a scenario card is placed. These cards represent specific reactions to the situation that is presented in the scenario card. Each hand of five dealt cards will contain at least one appropriate response, and your job is to pick the best one."
stringDescChoice = 'You can use their mouse to select the card that you feel best fits the scenario. Clicking the "Play Card" button to the right of the card will finalize your choice. Make sure to think hard, but be quick! You need to submit your answer before the timer ticks down to 0.'
stringDescScore = "After playing your card, you will be shown a summary of the number of points each card in your hand would have received when paired with that scenario. Your total score is displayed in the top right corner, and the game ends at 100 points."

#In-Game Screen
POS_ANSWER1 = (190,570)
POS_ANSWER2 = (325,570)
POS_ANSWER3 = (460,570)
POS_ANSWER4 = (595,570)
POS_ANSWER5 = (730,570)
POS_PLAY = (740, 300)
POS_SCENARIO = (385, 285)
POS_MAINMENU = (0, 0)
POS_SCORE = (768, 0)
POS_SCENARIODECK = (25, 285)
POS_ANSWERDECK = (45, 570)
POS_POINTVALS = [(240,680),(375,680),(510,680),(645,680),(780,680)]
POS_SCORETEXT = (788,10)

#Customization
POS_SQUARE_WHITE = (570, 365)
POS_SQUARE_LIGHTPINK = (770, 365)
POS_SQUARE_LIGHTBLUE = (570, 565)
POS_SQUARE_LIGHTGREEN = (770, 565)
POS_CARD_CUBES = (70, 365)
POS_CARD_MARBLE = (215, 365)
POS_CARD_PINK = (360, 365)
POS_CARD_STONE = (70, 565)
POS_CARD_TILE = (215, 565)
POS_CARD_WOVEN = (360, 565)
POS_BOX_SOUND = (768, 0)
POS_SELECT_ARTWORK = (150, 210)
POS_CHOOSE_BACKGROUND = (630, 210)

#About
POS_HEADER_ABOUT = (330, 30)
POS_DESCRIPTION = (90, 130)
RECT_DESCRIPTION = pygame.Rect(90, 180, 754, 80)
POS_CREATORS = (90, 250)
RECT_CREATORS = pygame.Rect(90, 300, 754, 110)
POS_THANKS = (90,400)
RECT_THANKS = pygame.Rect(90, 450, 754, 300)
stringDescription = "Pairs to Peers is a game designed to help children who suffer from an Autism Spectrum disorder.  Through responsive card-based gameplay it allows a child to learn how to recognize and respond to various social stimuli."
stringCreators = 'Created by Edgar Hu, Ryan Branch, Austin Trieu and Derek Xia.\nThis game was made as our semester project for the "Gaming for the Greater Good" section of ENGR100 at the University of Michigan College of Engineering.\nThe GitHub repository for the game can be found at http://github.com/rjbranch/PairsToPeers/'
stringThanks = "David Clark, for creating the TextRect module\nJerome Rasky, for creating the EzText module, and Bryant Sell for their improvements of it\nMark DiAngelo and SoundBible.com user Thore for their recordings of the sounds used in this game\nSteve Matteson, for creating the OpenSans and OpenSans Bold fonts used in this project"

#Difficulty
POS_EASY = (384,100)
POS_MEDIUM = (384,300)
POS_HARD = (384,500)

#Diagnostics
POS_SCREENSHOT = (768, 0)
POS_PLAYER_NAME_REPORT = (180, 140)
POS_TIMESTAMP_REPORT = (180, 220)
POS_DETAIL1_REPORT = (80, 320)
POS_DETAIL2_REPORT = (80, 380)
POS_DETAIL3_REPORT = (80, 440)
POS_DETAIL4_REPORT = (80, 500)
POS_DETAIL5_REPORT = (80, 560)
POS_BREAKDOWN_TEXT = (595, 300)
POS_BREAKDOWN_GREAT = (630, 350)
POS_BREAKDOWN_OK = (770, 350)
POS_BREAKDOWN_POOR = (630, 530)
POS_BREAKDOWN_TIMEUP = (770, 530)

backgroundColor = COLOR_WHITE
soundOn = True
timeStamp = time.time()
stringTimeStamp = datetime.datetime.fromtimestamp(timeStamp).strftime('%H:%M %m/%d/%Y ')

class Object(pygame.sprite.Sprite):
	def __init__(self, file_name, position):
		self.image = pygame.image.load(file_name)
		self.rect = pygame.Rect(position[0], position[1], self.image.get_size()[0], self.image.get_size()[1])

#These two lines create the window in which the game is played, titling it "Pairs to Peers".
gameDisplay = pygame.display.set_mode((GAME_WIDTH,GAME_HEIGHT))
pygame.display.set_caption("Pairs to Peers")

#Loads in all of the objects and sprites necessary for the game
#Main Menu
spr_bottomCorner = pygame.image.load("img/corner_blue_bottomleft.png")
spr_topCorner = pygame.image.load("img/corner_blue_topright.png")
obj_logo = Object("img/logo.png", POS_LOGO)
obj_buttonPlayGame = Object("img/button_Play_Game.png", POS_PLAYGAME)
obj_buttonHowToPlay = Object("img/button_How_To_Play.png", POS_HOWTOPLAY)
obj_buttonOptions = Object("img/button_Options.png", POS_OPTIONS)

#In-game screen
cardArtwork = "cubes"
obj_answerCard1 = Object("img/answerCard_blue.png", POS_ANSWER1)
obj_answerCard2 = Object("img/answerCard_blue.png", POS_ANSWER2)
obj_answerCard3 = Object("img/answerCard_blue.png", POS_ANSWER3)
obj_answerCard4 = Object("img/answerCard_blue.png", POS_ANSWER4)
obj_answerCard5 = Object("img/answerCard_blue.png", POS_ANSWER5)
obj_playCard = Object("img/button_medium_green.png", POS_PLAY)
obj_scoreDisplay = Object("img/button_medium_blue.png", POS_SCORE)
obj_buttonMainMenu = Object("img/button_Main_Menu.png", POS_MAINMENU)
answerObjArray = [obj_answerCard1, obj_answerCard2, obj_answerCard3, obj_answerCard4, obj_answerCard5]
spr_scenarioCard = pygame.image.load("img/scenarioCard_blue.png")
spr_backOfAnswerCard = pygame.image.load("img/card_back_small_" + cardArtwork + ".png")
spr_backOfScenarioCard = pygame.image.load("img/card_back_large_" + cardArtwork + ".png")

#Customization screen
obj_square_white = Object("img/square_white_green.png", POS_SQUARE_WHITE)
obj_square_lightpink = Object("img/square_lightpink.png", POS_SQUARE_LIGHTPINK)
obj_square_lightblue = Object("img/square_lightblue.png", POS_SQUARE_LIGHTBLUE)
obj_square_lightgreen = Object("img/square_lightgreen.png", POS_SQUARE_LIGHTGREEN)
obj_card_cubes = Object("img/card_back_small_cubes_green.png", POS_CARD_CUBES)
obj_card_marble = Object("img/card_back_small_marble.png", POS_CARD_MARBLE)
obj_card_pink = Object("img/card_back_small_pink.png", POS_CARD_PINK)
obj_card_stone = Object("img/card_back_small_stone.png", POS_CARD_STONE)
obj_card_tile = Object("img/card_back_small_tile.png", POS_CARD_TILE)
obj_card_woven = Object("img/card_back_small_woven.png", POS_CARD_WOVEN)
obj_box_sound = Object("img/box_sound_on.png", POS_BOX_SOUND)
spr_selectArtwork = pygame.image.load("img/box_select_artwork.png")
spr_chooseBackground = pygame.image.load("img/box_choose_background.png")
squareObjArray = [obj_square_white, obj_square_lightpink, obj_square_lightblue, obj_square_lightgreen]
cardBackObjArray = [obj_card_cubes, obj_card_marble, obj_card_pink, obj_card_stone, obj_card_tile, obj_card_woven, obj_box_sound]

#Difficulty screen
obj_buttonEasy = Object("img/button_Difficulty_Easy.png", POS_EASY)
obj_buttonMedium = Object("img/button_Difficulty_Medium.png", POS_MEDIUM)
obj_buttonHard = Object("img/button_Difficulty_Hard.png", POS_HARD)

#Diagnostic screen
obj_buttonScreenshot = Object("img/button_Screenshot.png", POS_SCREENSHOT)
spr_responseBreakdown = pygame.image.load("img/answerCard_Blue.png")

#This class defines the scenario cards, which players consider when playing their corresponding answer card.
class Scenario:

	#MEMBER VARIABLES#
		# scenarioText - a string describing the scenario
		# arrPoints - array containing answer point vals
		# beenPlayed - a boolean that keeps track of whether or not the scenario has already been in play during the current game

	#Default constructor
	def __init__(self):
		self.scenarioText = "SCENARIO INITIALIZED WITHOUT TEXT"
		self.arrPoints = []
		self.beenPlayed = False

	#Constructor Method
	def __init__(self, cardText, arrPoints):
		self.scenarioText = cardText
		self.beenPlayed = False #Scenario cards are initialized having not been played
		self.arrPoints = arrPoints
	#This method is used to denote that the scenario card has now been played
	def play(self):
		self.beenPlayed = True

	def getPointVal(self, cardNum):
		return self.arrPoints[cardNum]

class Answer:

	#MEMBER VARIABLES#
		# ansText - a string describing the scenario
		# numCard - number of the action card
		# pointVal - an int that will keep track of how many points playing this card will give. Changes based on scenario
		# beenDealt - a boolean that keeps track of whether or not an answer card has been dealt to a player already
		# beenPlayed - a boolean that keeps track of whether or not the scenario has already been in play during the current game
		#NOTE: beenPlayed isn't necessary for the functionality of this game, it simply exists in case someone were to change it later on such that enough cards were added to make recycling cards unwanted/unnecessary

	#Default constructor
	def __init__(self):
		self.ansText = "ANSWER INITIALIZED WITHOUT TEXT"
		self.numCard = -1
		self.pointVal = -1
		self.beenDealt = False
		self.BeenPlayed = False

	#cons
	def __init__(self, cardText, cardNum):
		self.ansText = cardText
		self.beenDealt = False
		self.beenPlayed = False
		self.numCard = cardNum

	#call this to change the number of points an answer is worth each round
	def setPoints(self, points):
		self.pointVal = points

	#NOTE: Stores that a card has in fact been played.  This is only useful if we don't want to recycle cards.
	def playCard(self):
		self.beenPlayed = True
		#following line incorrect since scoring system hasn't been started yet
		#pointsOfPlayer = pointsofPlayer + pointVal

	def getCardNum(self):
		return self.numCard

	def getText(self):
		return self.ansText

#This class defines the players of the game
class Player:

	#MEMBER VARIABLES#
		# isHuman - a boolean denoting whether the player is a human (true) or an AI (false)
		# playerName - a string of the name of the player
		# playerNum - the integer value denoting the player's number (1 = Player 1, 2 = Player 2, etc.)
		# score - the integer value of the player's score
		# handArray - array that stores the cards in a player's hand

	#Constructor Method
	def __init__(self, name, number, human):
		self.isHuman = human
		self.playerName = name
		self.playerNum = number
		self.score = 0 #Players are initialized with 0 points
		self.handArray = []#Initializes handArray as an empty array

	#This method is used to increase a player's score by a given number of points
	def addPoints(self, pointsToAdd):
		self.score += pointsToAdd

	def setPoints(self, numPoints):
		self.score = numPoints

	def getPoints(self):
		return self.score

	def getHand(self):
		return self.handArray

	def clearHand(self):
		self.handArray = []

	def getName(self):
		return self.playerName

	def setName(self, nameIn):
		self.playerName = nameIn

#Diagnostic class
#Contains information from each round used to track
#Total Score, Average Response Time, Rounds played
#Number of Good/Acceptable/Bad/No response answers	
class Diagnostic:

	#Member Variables#
		#pointsRecieved - Integer describing the number of points the user got this round
		#timeUp - Boolean describing whether the round ended due to time running out
		#timeToAns - Integer describing the amount of time taken to answer, in milliseconds
		#timeGiven - Integer describing the maximum amount of time the user could have taken, in milliseconds
		#scenarioIndex - index of the scenario card that was present during this round
		#answerIndex - index of the answer card that was present during this round

	#Default constructor
	def __init__(self):
		self.pointsRecieved = 0
		self.timeUp = False
		self.timeToAns = 0
		self.timeGiven = 0
		self.scenario = Scenario()
		self.answerIndex = 0

	#Constructor with inputs
	def __init__(self, roundPoints, outOfTime, ansTime, givenTime, numScenario, numAnswer):
		self.pointsRecieved = roundPoints
		self.timeUp = outOfTime
		self.timeToAns = ansTime
		self.timeGiven = givenTime
		self.scenarioIndex = numScenario
		self.answerIndex = numAnswer

	def getRoundPoints(self):
		return self.pointsRecieved

	def getTimeUp(self):
		return self.timeUp

	def getTimeToAns(self):
		return self.timeToAns

	def getTimeGiven(self):
		return self.timeGiven

#This function takes in a one-dimensional array and "shuffles" the contents, ordering them randomly.
#NOTE: I realize that this python's random.shuffle() function makes this an incredibly simple task, but I figure we should have it as a separate function instead of just calling random.shuffle() directly every time, in case there's every any sort of functionality we need to add to shuffling.
def shuffle(inArray):
	random.shuffle(inArray)
	return inArray

#This function builds the deck of scenario cards.  More lines can be added accordingly whenever more cards are to be added.
def buildScenarios():
	scenarios = []
	card = Scenario("A person walks up to you on the first day of school and says hello.", [0,6,0,0,0,7,0,10,10,9,6,0,0,0,0,0,0,0,0,4,0,10,6,0,9,0,0])
	scenarios.append(card)
	card = Scenario("Your friend is crying.", [7,9,0,0,5,0,0,4,4,4,0,0,0,0,10,10,8,0,0,0,0,0,4,0,0,0,5])
	scenarios.append(card)
	card = Scenario("You are hungry.", [0,8,0,10,5,0,0,0,0,0,0,0,0,0,0,0,0,0,6,0,0,0,0,0,0,0,2])
	scenarios.append(card)
	card = Scenario("You are looking for a pencil but can't find one.", [0,8,0,0,9,0,0,0,0,0,0,4,0,0,0,0,0,0,5,0,0,0,0,0,0,0,0])
	scenarios.append(card)
	card = Scenario("There is a bully, saying mean things, who won't leave you alone.", [0,8,10,0,5,0,0,4,4,4,0,0,5,0,0,0,0,8,5,0,0,0,4,5,0,8,6])
	scenarios.append(card)
	card = Scenario("You notice that someone in your class has candy and you want some.", [0,6,0,5,0,0,0,9,9,8,0,0,0,0,0,0,0,0,10,0,0,9,0,0,8,0,0])
	scenarios.append(card)
	card = Scenario("You are offered candy by a friend.", [0,0,0,0,0,0,0,5,6,6,8,7,0,0,0,5,0,0,9,10,0,0,4,6,8,2,0])
	scenarios.append(card)
	card = Scenario("You have a bloody nose.", [0,10,0,0,7,0,0,0,0,0,0,0,0,0,0,0,0,5,0,0,0,0,0,0,0,0,8])
	scenarios.append(card)
	card = Scenario("You forgot your homework.", [8,8,0,0,8,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
	scenarios.append(card)
	card = Scenario("Someone asks you for directions.", [6,5,0,0,6,0,0,8,8,10,7,5,0,0,10,4,0,0,0,0,0,4,0,0,0,0,0])
	scenarios.append(card)
	#card = Scenario("Someone calls you autistic.", [0,10,8,0,0,0,4,0,0,0,0,0,0,0,0,0,0,7,0,0,0,0,4,5,0,10,3])
	#scenarios.append(card)
	card = Scenario("Teacher asks you a question.", [2,5,0,0,5,0,0,0,0,0,6,6,0,0,0,0,0,0,6,2,0,0,0,0,5,0,0])
	scenarios.append(card)
	card = Scenario("You have you put on your coat.", [0,9,0,0,5,0,0,0,0,0,8,0,0,0,6,0,0,0,4,8,0,0,0,0,6,0,0])
	#card = Scenario("another scenario goes here")
	#scenarios.append(card)
	return scenarios

#This function builds the deck of answer cards.  More lines can be added accordingly whenever more cards are to be added.
def buildAnswers():
	answers = []
	card = Answer("Say you're sorry", 0)
	answers.append(card)
	card = Answer("Ask for help", 1)
	answers.append(card)
	card = Answer("Turn around and walk away", 2)
	answers.append(card)
	card = Answer("Eat some food", 3)
	answers.append(card)
	card = Answer("Look around", 4)
	answers.append(card)
	card = Answer("Clap your hands", 5)
	answers.append(card)
	card = Answer("Yell at them", 6)
	answers.append(card)
	card = Answer("Say hello", 7)
	answers.append(card)
	card = Answer("Introduce yourself", 8)
	answers.append(card)
	card = Answer("Ask for their name", 9)
	answers.append(card)
	card = Answer("Nod your head", 10)
	answers.append(card)
	card = Answer("Shrug your shoulders", 11)
	answers.append(card)
	card = Answer("Do nothing", 12)
	answers.append(card)
	card = Answer("Call 911", 13)
	answers.append(card)
	card = Answer("Offer to help", 14)
	answers.append(card)
	card = Answer("Give them a hug", 15)
	answers.append(card)
	card = Answer("Offer them tissues", 16)
	answers.append(card)
	card = Answer("Run away", 17)
	answers.append(card)
	card = Answer("Say please", 18)
	answers.append(card)
	card = Answer("Say thank you", 19)
	answers.append(card)
	card = Answer("Congratulate them", 20)
	answers.append(card)
	card = Answer("Offer a high five", 21)
	answers.append(card)
	card = Answer("Talk about your day", 22)
	answers.append(card)
	card = Answer("Push away", 23)
	answers.append(card)
	card = Answer("Jump up and down in excitement", 24)
	answers.append(card)
	card = Answer("Ignore them", 25)
	answers.append(card)
	card = Answer("Cry", 26)
	answers.append(card)
	#card = Answer("another answer goes here", 21)
	#answers.append(card)
	return answers

def resetSquares():
	obj_square_white.image = pygame.image.load("img/square_white.png")
	obj_square_lightpink.image = pygame.image.load("img/square_lightpink.png")
	obj_square_lightgreen.image = pygame.image.load("img/square_lightgreen.png")
	obj_square_lightblue.image = pygame.image.load("img/square_lightblue.png")

def resetCardBacks():
	obj_card_cubes.image = pygame.image.load("img/card_back_small_cubes.png")
	obj_card_marble.image = pygame.image.load("img/card_back_small_marble.png")
	obj_card_pink.image = pygame.image.load("img/card_back_small_pink.png")
	obj_card_stone.image = pygame.image.load("img/card_back_small_stone.png")
	obj_card_tile.image = pygame.image.load("img/card_back_small_tile.png")
	obj_card_woven.image = pygame.image.load("img/card_back_small_woven.png")

#This function takes a string, a color, and a coordinate as input and displays text on the screen accordingly
def displayMessage(messageText,messageColor,messageLocation, font=font):
	screen_text = font.render(messageText, True, messageColor)
	gameDisplay.blit(screen_text, messageLocation)

#This function takes some text and the coordinates of a button rectangle and places text on the button appropriately.
def buttonText(text, color, xPos, yPos, width, height, size):
	return 0

#This is the main function of the program.	It handles everything that's going on at each moment of the game
def gameLoop():
	backgroundColor = COLOR_WHITE
	soundOn = True
	cardArtwork = "cubes"
	pointFeedbackArray = []
	feedbackTextArray = []
	pointVal = 0
	winningStreak = 0.0

	gameRun = True #Boolean that stores whether the game should be running
	playersIn = False #Boolean that stores whether all of the player information has been input
	clock = pygame.time.Clock()
	scenarioArray = []#Initializes the array that will eventually store the scenario cards
	answerArray = []#Initializes the array that will eventually store the answer cards
	diagnosticArray = [] #Initializes the array that will store the diagnostic information
	scenarioArray = buildScenarios()
	answerArray = buildAnswers()
	scenarioArray = shuffle(scenarioArray)
	answerArray = shuffle(answerArray)
	answerRects = [pygame.Rect(POS_ANSWER1[0] + 10, POS_ANSWER1[1] + 10, 108, 150),
				   pygame.Rect(POS_ANSWER2[0] + 10, POS_ANSWER2[1] + 10, 108, 150),
				   pygame.Rect(POS_ANSWER3[0] + 10, POS_ANSWER3[1] + 10, 108, 150),
				   pygame.Rect(POS_ANSWER4[0] + 10, POS_ANSWER4[1] + 10, 108, 150),
				   pygame.Rect(POS_ANSWER5[0] + 10, POS_ANSWER5[1] + 10, 108, 150)]
	scenarioRect = pygame.Rect(POS_SCENARIO[0] + 20, POS_SCENARIO[1] + 20, 300, 216)
	playRect = pygame.Rect(POS_PLAY[0] + 20, POS_PLAY[1] + 20, 200, 100)
	feedbackTextRect = pygame.Rect(256, 50, 512, 100)
	feedbackSubtextRect = pygame.Rect(256, 150, 512, 100)
	scoreTextRect = pygame.Rect(760,35,216,90)
	nameColor = COLOR_BLACK
	nameBox = eztext.Input(x=400, y=50, font=big_bold_font, maxlength=20, color=nameColor, prompt='Name: ')

	cardSelected = 0
	canPlay = False
	nextRound = False
	hasWinningCard = False
	gameWon = False
	minPointsHand = 0
	timeAllowed = 15000
	timeThisRound = 0.0
	countdown = 0
	nextRoundRendered = playCardRendered = render_textrect("Next Round", scenario_card_font, playRect, COLOR_BLACK, [191,255,191])
	showFeedback = False
	hasFeedback = False
	feedbackDone = False
	isPaused = 0
	dataProcessed = False
	totalResponseTime = 0
	numGreat = 0
	numOkay = 0
	numPoor = 0
	numTimeUp = 0
	fullscreen = False
	hasDealt = False
	counting = True
	tempName = "No Name"
	hasIncremented = False
	cheating = True
	setCheating = False
	nameString = ""
	screenshotTaken = False
	#The gameSceen variable is used to set and determine which screen of the game should be currently displayed on the screen.
	#The following key describes the screen to which each individual integer corresponds
	#1 = Instructions
	#2 = Main Menu
	#3 = About
	#4 = Gameplay
	#5 = Endgame
	#6 = Player selection
	#7 = Customization
	#8 = Difficulty
	#9 = Diagnostics
	gameScreen = 2

	player = Player('No Name', 1, True)

	currentScenario = scenarioArray.pop() #Effectively deals a scenario card to the game from the deck

	while gameRun: #Continues to execute until gameRun is set to false

		while (gameScreen == 1 and gameRun):
			descScenarioRendered = render_textrect(stringDescScenario, answer_card_font, RECT_DESC_SCENARIO, COLOR_BLACK, backgroundColor)
			descResponseRendered = render_textrect(stringDescResponse, answer_card_font, RECT_DESC_RESPONSE, COLOR_BLACK, backgroundColor)
			descChoiceRendered = render_textrect(stringDescChoice, answer_card_font, RECT_DESC_CHOICE, COLOR_BLACK, backgroundColor)
			descScoreRendered =  render_textrect(stringDescScore, answer_card_font, RECT_DESC_SCORE, COLOR_BLACK, backgroundColor)
			gameDisplay.fill(backgroundColor)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					gameRun = False #Ends the game if they user attempts to close the window
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						gameRun = False
				if event.type == pygame.MOUSEBUTTONDOWN:
					# Set the x, y positions of the mouse click
					x, y = event.pos
					if ((obj_buttonMainMenu.rect.collidepoint(x, y))):
						if soundOn:
							sound_blop.play()
						gameScreen = 2
			displayMessage("Scenario Cards:", COLOR_BLACK, POS_DESC_SCENARIO, big_bold_font)
			displayMessage("Response Cards:", COLOR_BLACK, POS_DESC_RESPONSE, big_bold_font)
			displayMessage("Making the Choice:", COLOR_BLACK, POS_DESC_CHOICE, big_bold_font)
			displayMessage("Feedback and Scoring:", COLOR_BLACK, POS_DESC_SCORE, big_bold_font)
			displayMessage("How to Play", COLOR_BLACK, POS_HEADER_INSTRUCTIONS, bigger_bold_font)
			gameDisplay.blit(obj_buttonMainMenu.image, obj_buttonMainMenu.rect)
			gameDisplay.blit(descScenarioRendered, RECT_DESC_SCENARIO.topleft)
			gameDisplay.blit(descResponseRendered, RECT_DESC_RESPONSE.topleft)
			gameDisplay.blit(descChoiceRendered, RECT_DESC_CHOICE.topleft)
			gameDisplay.blit(descScoreRendered, RECT_DESC_SCORE.topleft)
			pygame.display.update() #Updates the screen every frame
			clock.tick(FRAMES_PER_SECOND)

		while (gameScreen == 2 and gameRun):
			gameWon = False
			winningStreak = 0
			gameDisplay.fill(backgroundColor)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					gameRun = False #Ends the game if they user attempts to close the window
				if event.type == pygame.MOUSEBUTTONDOWN:
					# Set the x, y positions of the mouse click
					x, y = event.pos
					if ((obj_buttonPlayGame.rect.collidepoint(x, y))):
						if soundOn:
							sound_blop.play()
						diagnosticArray = []
						#startTime = pygame.time.get_ticks()
						gameScreen = 8
					elif((obj_buttonOptions.rect.collidepoint(x, y))):
						if soundOn:
							sound_blop.play()
						gameScreen = 7
					elif ((obj_logo.rect.collidepoint(x, y))):
						if soundOn:
							sound_blop.play()
						gameScreen = 3
					elif ((obj_buttonHowToPlay.rect.collidepoint(x, y))):
						if soundOn:
							sound_blop.play()
						gameScreen = 1
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_F11:
						if fullscreen == True:
							pygame.display.set_mode((GAME_WIDTH,GAME_HEIGHT))
							fullscreen = False
						elif fullscreen == False:
							pygame.display.set_mode((GAME_WIDTH,GAME_HEIGHT), pygame.FULLSCREEN)
							fullscreen = True
					if event.key == pygame.K_ESCAPE:
						gameRun = False
				#NOTE: Developer setting, uncomment to access diagnostics from pressing "D" at main menu
				#if event.type == pygame.KEYDOWN:
				#	if event.key == pygame.K_d:
				#		gameScreen = 9


			gameDisplay.blit(obj_logo.image, obj_logo.rect)
			gameDisplay.blit(obj_buttonPlayGame.image, obj_buttonPlayGame.rect)
			gameDisplay.blit(obj_buttonHowToPlay.image,obj_buttonHowToPlay.rect)
			gameDisplay.blit(obj_buttonOptions.image, obj_buttonOptions.rect)
			gameDisplay.blit(spr_bottomCorner, POS_BOTTOMCORNER)
			gameDisplay.blit(spr_topCorner, POS_TOPCORNER)
			pygame.display.update() #Updates the screen every frame
			clock.tick(FRAMES_PER_SECOND)

		while (gameScreen == 3 and gameRun):
			descriptionRendered = render_textrect(stringDescription, answer_card_font, RECT_DESCRIPTION, COLOR_BLACK, backgroundColor)
			creatorsRendered = render_textrect(stringCreators, answer_card_font, RECT_CREATORS, COLOR_BLACK, backgroundColor)
			thanksRendered = render_textrect(stringThanks, answer_card_font, RECT_THANKS, COLOR_BLACK, backgroundColor)
			gameDisplay.fill(backgroundColor)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					gameRun = False #Ends the game if they user attempts to close the window
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						gameRun = False
				if event.type == pygame.MOUSEBUTTONDOWN:
					# Set the x, y positions of the mouse click
					x, y = event.pos
					if ((obj_buttonMainMenu.rect.collidepoint(x, y))):
						if soundOn:
							sound_blop.play()
						gameScreen = 2
			displayMessage("Description:", COLOR_BLACK, POS_DESCRIPTION, big_bold_font)
			displayMessage("The Project", COLOR_BLACK, POS_CREATORS, big_bold_font)
			displayMessage("Thanks to:", COLOR_BLACK, POS_THANKS, big_bold_font)
			displayMessage("About our Game", COLOR_BLACK, POS_HEADER_ABOUT, bigger_bold_font)
			gameDisplay.blit(obj_buttonMainMenu.image, obj_buttonMainMenu.rect)
			gameDisplay.blit(descriptionRendered, RECT_DESCRIPTION.topleft)
			gameDisplay.blit(creatorsRendered, RECT_CREATORS.topleft)
			gameDisplay.blit(thanksRendered, RECT_THANKS.topleft)
			pygame.display.update() #Updates the screen every frame
			clock.tick(FRAMES_PER_SECOND)

		while (gameScreen == 4 and gameRun):
			gameDisplay.fill(backgroundColor)
			timeThisRound = timeAllowed / ((winningStreak / 10) + 1) #This is used in the incremental difficulty system
			#displayMessage("DIFFICULTY MULTIPLIER = " + str(timeThisRound / timeAllowed),COLOR_BLACK,(100,150))
			for event in pygame.event.get():
				
				if event.type == pygame.QUIT:
					gameRun = False #Ends the game if they user attempts to close the window
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						gameRun = False

				if (((pygame.time.get_ticks() - startTime) > timeThisRound) and (isPaused == 0)):
					#display message + no points this round
					nextRound = True
					canPlay = False
					showFeedback = True
					pointVal = 0

					if (hasIncremented == False):
						diagnosticObject = Diagnostic(pointVal, True, timeThisRound, timeThisRound, currentScenario, hand[cardSelected].getCardNum())
						diagnosticArray.append(diagnosticObject)
						hasIncremented = True


				if event.type == pygame.MOUSEBUTTONDOWN:
					# Set the x, y positions of the mouse click
					x, y = event.pos
					for card in range(len(answerObjArray)):
						if ((nextRound == False)):
							if (answerObjArray[card].rect.collidepoint(x, y)):
								if (cardSelected >= 0):
									answerObjArray[cardSelected].image = pygame.image.load('img/answerCard_blue.png')
								answerObjArray[card].image = pygame.image.load('img/answerCard_green.png')
								if soundOn:
									sound_blop.play()
								cardSelected = card
								if nextRound == False:
									canPlay = True

					if ((obj_playCard.rect.collidepoint(x, y)) and ((canPlay == True) or (nextRound == True))):
						if soundOn:
							sound_blop.play()

						if canPlay == True:
							canPlay = False
							nextRound = True
							isPaused = 1
							counting = False

							for card in range(len(answerObjArray)):
								answerObjArray[card].image = pygame.image.load('img/answerCard_blue.png')

							hand = player.getHand()
							pointVal = currentScenario.getPointVal(hand[cardSelected].getCardNum())
							player.addPoints(pointVal)

							diagnosticObject = Diagnostic(pointVal, False, (pygame.time.get_ticks() - startTime), timeThisRound, currentScenario ,hand[cardSelected].getCardNum())
							diagnosticArray.append(diagnosticObject)

							#This if statement used in the incremental difficulty system.
							if (pointVal >= 6):
								winningStreak = winningStreak + 1.0
							showFeedback = True

						else:

							answerObjArray[cardSelected].image = pygame.image.load('img/answerCard_blue.png')

							hand = player.getHand()
							pointFeedbackArray = [] #Stores the integer value of points that each card is worth in the 0 through 4 positions.
							feedbackTextArray = [] #Stores the actual text 'objects' of the point values to be played on the screen.  Ordering is just like pointFeedbackArray.
							for card in range(5):
								pointFeedbackArray.append(currentScenario.getPointVal(hand[card].getCardNum()))

							canPlay = False
							nextRound = False
							showFeedback = False
							hasIncremented = False

							if(player.getPoints() >= POINTS_TO_WIN):
								gameWon = True
								canPlay = False
								if soundOn:
									sound_applause.play()
								gameScreen = 9

							tempScenario = currentScenario
							currentScenario = scenarioArray.pop()

							scenarioArray.append(tempScenario)
							scenarioArray = shuffle(scenarioArray)

							cards = 0
							while(cards < 5):
								answerArray.append(hand[cards])
								cards = cards + 1

							answerArray = shuffle(answerArray)
							player.clearHand()
							cardsInHand = len(player.handArray)

							for x in xrange(0, (5 - cardsInHand)): #Iterates until the user's hand is full
								
								player.handArray.append(answerArray.pop()) #This is effectively dealing a card, as it removes the last element from the answer deck and places it in the player's hand

							hand = player.getHand()
							hasWinningCard = False
							pointFeedbackArray = [] #Stores the integer value of points that each card is worth in the 0 through 4 positions.
							feedbackTextArray = [] #Stores the actual text 'objects' of the point values to be played on the screen.  Ordering is just like pointFeedbackArray.
							for card in range(5):
								pointFeedbackArray.append(currentScenario.getPointVal(hand[card].getCardNum()))
							minPointsHand = 0
							startTime = pygame.time.get_ticks()
							isPaused = 0
							feedbackDone = False
							hasDealt = False
							counting = True

					if (obj_buttonMainMenu.rect.collidepoint(x, y)):
						player.setPoints(0)
						player.clearHand()
						showFeedback = False #Ensures previous game's feedback won't be shown when new game is started
						nextRound = False
						canPlay = False
						scenarioArray = shuffle(scenarioArray)
						currentScenario = scenarioArray.pop()
						answerArray = shuffle(answerArray)
						hasDealt = False
						feedbackDone = False
						if (soundOn):
							sound_blop.play()
						gameScreen = 2

			pygame.time.set_timer(pygame.USEREVENT + 1, 100)
			pygame.event.post(pygame.event.Event(pygame.USEREVENT + 1))

			gameDisplay.blit(obj_answerCard1.image, obj_answerCard1.rect)
			gameDisplay.blit(obj_answerCard2.image, obj_answerCard2.rect)
			gameDisplay.blit(obj_answerCard3.image, obj_answerCard3.rect)
			gameDisplay.blit(obj_answerCard4.image, obj_answerCard4.rect)
			gameDisplay.blit(obj_answerCard5.image, obj_answerCard5.rect)
			gameDisplay.blit(obj_scoreDisplay.image, obj_scoreDisplay.rect)
			gameDisplay.blit(obj_buttonMainMenu.image, obj_buttonMainMenu.rect)
			gameDisplay.blit(spr_scenarioCard, POS_SCENARIO)

			if not hasDealt:
				turnGoing = True
				cardsInHand = len(player.handArray)

				for x in xrange(0, (5 - cardsInHand)): #Iterates until the user's hand is full
					player.handArray.append(answerArray.pop()) #This is effectively dealing a card, as it removes the last element from the answer deck and places it in the player's hand

				while (not hasWinningCard):
					#Attempts to make the user's hand have a winning card
					answerArray.insert(0, player.handArray.pop())
					player.handArray.append(answerArray.pop())
					for card in player.handArray: #Iterates through all 5 cards in the user's hand
						if (currentScenario.getPointVal(card.getCardNum()) > minPointsHand):
							minPointsHand = currentScenario.getPointVal(card.getCardNum())
					if (minPointsHand >= GOOD_CARD_POINTS):
						player.handArray = shuffle(player.handArray)
						hasWinningCard = True

				hand = player.getHand()
				hasDealt = True
				player.handArray.append(answerArray)
				#Cards have been dealt

			if (not feedbackDone):
				hand = player.getHand()
				pointFeedbackArray = [] #Stores the integer value of points that each card is worth in the 0 through 4 positions.
				feedbackTextArray = [] #Stores the actual text 'objects' of the point values to be played on the screen.  Ordering is just like pointFeedbackArray.
				for card in range(5):
					pointFeedbackArray.append(currentScenario.getPointVal(hand[card].getCardNum()))

				feedbackDone = True

			for cardNum in xrange(0,5): #Shows answer cards on the screen
				answerCardRendered = render_textrect(hand[cardNum].ansText, answer_card_font, answerRects[cardNum], COLOR_BLACK, COLOR_WHITE)
				if answerCardRendered:
					gameDisplay.blit(answerCardRendered, answerRects[cardNum].topleft)

			spr_backOfAnswerCard = pygame.image.load("img/card_back_small_" + cardArtwork + ".png")
			spr_backOfScenarioCard = pygame.image.load("img/card_back_large_" + cardArtwork + ".png")
			gameDisplay.blit(spr_backOfScenarioCard, POS_SCENARIODECK)
			gameDisplay.blit(spr_backOfAnswerCard, POS_ANSWERDECK)

			for i in range(len(pointFeedbackArray)):
				numPoints = pointFeedbackArray[i]
				if (numPoints == 0):
					valColor = COLOR_POINTS_0
				elif (numPoints == 1):
					valColor = COLOR_POINTS_1
				elif (numPoints == 2):
					valColor = COLOR_POINTS_2
				elif (numPoints == 3):
					valColor = COLOR_POINTS_3
				elif (numPoints == 4):
					valColor = COLOR_POINTS_4
				elif (numPoints == 5):
					valColor = COLOR_POINTS_5
				elif (numPoints == 6):
					valColor = COLOR_POINTS_6
				elif (numPoints == 7):
					valColor = COLOR_POINTS_7
				elif (numPoints == 8):
					valColor = COLOR_POINTS_8
				elif (numPoints == 9):
					valColor = COLOR_POINTS_9
				elif (numPoints == 10):
					valColor = COLOR_POINTS_10
				feedbackText = big_bold_font.render(str(numPoints), True, valColor)
				feedbackTextArray.append(feedbackText)
			if (pointVal == 0):
				winningStreak = 0
				if (((pygame.time.get_ticks() - startTime) > timeThisRound) and (isPaused == 0)):
					mainFeedbackString = "Sorry, time's up."
				else:
					mainFeedbackString = "Sorry, that's incorrect."
			elif (pointVal <= 5):
				mainFeedbackString = "Okay, but think about different responses."
			elif (pointVal <= 10):
				mainFeedbackString = "Great answer!"
			mainFeedbackTextRendered = render_textrect(mainFeedbackString, scenario_card_font, feedbackTextRect, COLOR_BLACK, backgroundColor, 1)
			mainFeedbackSubtextRendered = render_textrect(("+ " + str(pointVal) + " points"), big_bold_font, feedbackSubtextRect, COLOR_BLACK, backgroundColor, 1)

			playCardRendered = render_textrect("Play Card", scenario_card_font, playRect, COLOR_BLACK, [191,255,191])
			nextRoundRendered = render_textrect("Next Round", scenario_card_font, playRect, COLOR_BLACK, [191,255,191])
			scenarioCardRendered = render_textrect(currentScenario.scenarioText, scenario_card_font, scenarioRect, COLOR_BLACK, COLOR_WHITE)
			score = str(player.getPoints())

			scoreBoxRendered = render_textrect(("Score: " + str(score)), big_bold_font, pygame.Rect(760,35,216,60), COLOR_BLACK, [158,206,255])
			if counting:
				countdown = int(math.floor(((timeThisRound - pygame.time.get_ticks())/1000 + startTime/1000) + 1.9))

			if countdown < 0:
				countdown = 0
			timerRendered = render_textrect("Time: "+ str(countdown), big_bold_font, pygame.Rect(680,70,168,60), COLOR_BLACK, [158,206,255])

			if gameWon == True:
				displayMessage("Congratulations!  You won.",COLOR_BLACK,[278,158],big_bold_font) #Congratulates the user upon winning
				displayMessage("Press ENTER to go to the Game Over screen.",COLOR_BLACK,[32,32]) #Draws some text

			if timerRendered:
				gameDisplay.blit(timerRendered, pygame.Rect(788,60,178,160))

			if scoreBoxRendered:
				gameDisplay.blit(scoreBoxRendered, POS_SCORETEXT)
			if scenarioCardRendered:
				gameDisplay.blit(scenarioCardRendered, scenarioRect.topleft)

			if nextRound == True:
				gameDisplay.blit(obj_playCard.image, obj_playCard.rect)
				gameDisplay.blit(nextRoundRendered, playRect.topleft)

			if canPlay == True:
				gameDisplay.blit(obj_playCard.image, obj_playCard.rect)
				gameDisplay.blit(playCardRendered, playRect.topleft)

			if (showFeedback == True):
				gameDisplay.blit(mainFeedbackTextRendered, feedbackTextRect.topleft)
				gameDisplay.blit(mainFeedbackSubtextRendered, feedbackSubtextRect.topleft)
				for i in range(len(pointFeedbackArray)):
					gameDisplay.blit(feedbackTextArray[i], POS_POINTVALS[i])

			if (cheating == True):
				for i in range(len(pointFeedbackArray)):
					gameDisplay.blit(feedbackTextArray[i], POS_POINTVALS[i])

			pygame.display.update() #Updates the screen every frame
			clock.tick(FRAMES_PER_SECOND)

		while (gameScreen == 5 and gameRun): #Executes after the game has ended
			gameDisplay.fill(COLOR_BLACK)
			displayMessage("GAME OVER!  Press ENTER to play again, or SPACE to quit.",COLOR_RED,[GAME_WIDTH/3,GAME_HEIGHT/2])

			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_RETURN:
						gameLoop() #Restarts the game if the player presses the ENTER key
					if event.key == pygame.K_SPACE:
						gameRun = False #Closes the game if the player presses the SPACE key
					if event.key == pygame.K_ESCAPE:
						gameRun = False
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					gameRun = False #Ends the game if they user attempts to close the window
			pygame.display.update() #Updates the screen every frame
			clock.tick(FRAMES_PER_SECOND)

		while (gameScreen == 6 and gameRun):
			gameDisplay.fill(backgroundColor)
			displayMessage("This is the PLAYER SELECTION screen.",COLOR_RED,[GAME_WIDTH/3,GAME_HEIGHT/2])
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					gameRun = False #Ends the game if they user attempts to close the window
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						gameRun = False
			pygame.display.update() #Updates the screen every frame
			clock.tick(FRAMES_PER_SECOND)
			timer_event = pygame.USEREVENT + 1
			pygame.time.set_timer(timer_event, 250)

		while (gameScreen == 7 and gameRun):
			#NOTE:  The entire "selecting" (changing an image to the green version and making sure the rest are blue when it is clicked on) process could be done a lot more efficiently using pointers.  For now, I don't really know how to do that.  Maybe we could figure out down the line, but it would be a very late game thing since these actions are taken so infrequently that there wouldn't really be a huge difference in efficiency.
			gameDisplay.fill(backgroundColor)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					gameRun = False #Ends the game if they user attempts to close the window
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						gameRun = False
				if event.type == pygame.MOUSEBUTTONDOWN:
					# Set the x, y positions of the mouse click
					x, y = event.pos
					if ((obj_buttonMainMenu.rect.collidepoint(x, y))):
						if soundOn:
							sound_blop.play()
						gameScreen = 2
					elif ((obj_square_white.rect.collidepoint(x, y))):
						if soundOn:
							sound_blop.play()
						backgroundColor = COLOR_WHITE
						resetSquares()
						obj_square_white.image = pygame.image.load("img/square_white_green.png")
					elif ((obj_square_lightpink.rect.collidepoint(x, y))):
						if soundOn:
							sound_blop.play()
						backgroundColor = COLOR_LIGHTPINK
						resetSquares()
						obj_square_lightpink.image = pygame.image.load("img/square_lightpink_green.png")
					elif ((obj_square_lightgreen.rect.collidepoint(x, y))):
						if soundOn:
							sound_blop.play()
						backgroundColor = COLOR_LIGHTGREEN
						resetSquares()
						obj_square_lightgreen.image = pygame.image.load("img/square_lightgreen_green.png")
					elif((obj_square_lightblue.rect.collidepoint(x, y))):
						if soundOn:
							sound_blop.play()
						backgroundColor = COLOR_LIGHTBLUE
						resetSquares()
						obj_square_lightblue.image = pygame.image.load("img/square_lightblue_green.png")
					elif ((obj_card_cubes.rect.collidepoint(x, y))):
						if soundOn:
							sound_blop.play()
						cardArtwork = "cubes"
						resetCardBacks()
						obj_card_cubes.image = pygame.image.load("img/card_back_small_cubes_green.png")
					elif ((obj_card_marble.rect.collidepoint(x, y))):
						if soundOn:
							sound_blop.play()
						cardArtwork = "marble"
						resetCardBacks()
						obj_card_marble.image = pygame.image.load("img/card_back_small_marble_green.png")
					elif((obj_card_pink.rect.collidepoint(x, y))):
						if soundOn:
							sound_blop.play()
						cardArtwork = "pink"
						resetCardBacks()
						obj_card_pink.image = pygame.image.load("img/card_back_small_pink_green.png")
					elif ((obj_card_stone.rect.collidepoint(x, y))):
						if soundOn:
							sound_blop.play()
						cardArtwork = "stone"
						resetCardBacks()
						obj_card_stone.image = pygame.image.load("img/card_back_small_stone_green.png")
					elif ((obj_card_tile.rect.collidepoint(x, y))):
						if soundOn:
							sound_blop.play()
						cardArtwork = "tile"
						resetCardBacks()
						obj_card_tile.image = pygame.image.load("img/card_back_small_tile_green.png")
					elif((obj_card_woven.rect.collidepoint(x, y))):
						if soundOn:
							sound_blop.play()
						cardArtwork = "woven"
						resetCardBacks()
						obj_card_woven.image = pygame.image.load("img/card_back_small_woven_green.png")
					elif((obj_box_sound.rect.collidepoint(x, y))):
						if soundOn:
							obj_box_sound.image = pygame.image.load("img/box_sound_off.png")
						elif not(soundOn):
							sound_blop.play()
							obj_box_sound.image = pygame.image.load("img/box_sound_on.png")
						soundOn = not(soundOn)

			gameDisplay.blit(obj_buttonMainMenu.image, obj_buttonMainMenu.rect)
			gameDisplay.blit(obj_square_white.image, obj_square_white.rect)
			gameDisplay.blit(obj_square_lightpink.image, obj_square_lightpink.rect)
			gameDisplay.blit(obj_square_lightblue.image,obj_square_lightblue.rect)
			gameDisplay.blit(obj_square_lightgreen.image, obj_square_lightgreen.rect)
			gameDisplay.blit(obj_card_cubes.image, obj_card_cubes.rect)
			gameDisplay.blit(obj_card_marble.image, obj_card_marble.rect)
			gameDisplay.blit(obj_card_pink.image, obj_card_pink.rect)
			gameDisplay.blit(obj_card_stone.image, obj_card_stone.rect)
			gameDisplay.blit(obj_card_tile.image, obj_card_tile.rect)
			gameDisplay.blit(obj_card_woven.image, obj_card_woven.rect)
			gameDisplay.blit(obj_box_sound.image, obj_box_sound.rect)
			gameDisplay.blit(spr_selectArtwork, POS_SELECT_ARTWORK)
			gameDisplay.blit(spr_chooseBackground, POS_CHOOSE_BACKGROUND)
			pygame.display.update() #Updates the screen every frame
			clock.tick(FRAMES_PER_SECOND)

		while (gameScreen == 8 and gameRun):
			if (setCheating == False):
				cheating = False
				setCheating = True
			gameDisplay.fill(backgroundColor)
			gameDisplay.blit(obj_buttonMainMenu.image, obj_buttonMainMenu.rect)
			gameDisplay.blit(obj_buttonEasy.image, obj_buttonEasy.rect)
			gameDisplay.blit(obj_buttonMedium.image, obj_buttonMedium.rect)
			gameDisplay.blit(obj_buttonHard.image, obj_buttonHard.rect)

			#NOTE: In order for the output image to correctly contain all elements of the screen, the event handling portion of the while loop needs to come after any drawing that occurs.
			events = pygame.event.get()
			for event in events:
				if event.type == pygame.QUIT:
					gameRun = False #Ends the game if they user attempts to close the window
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						gameRun = False
				if event.type == pygame.MOUSEBUTTONDOWN:
					# Set the x, y positions of the mouse click
					x, y = event.pos
					if ((obj_buttonMainMenu.rect.collidepoint(x, y))):
						if soundOn:
							sound_blop.play()
						gameScreen = 2
					if ((obj_buttonEasy.rect.collidepoint(x, y))):
						if soundOn:
							sound_blop.play()
						timeAllowed = 30000
						timeStamp = time.time()
						stringTimeStamp = datetime.datetime.fromtimestamp(timeStamp).strftime('%H:%M %m/%d/%Y ')
						startTime = pygame.time.get_ticks()
						gameScreen = 4
					if ((obj_buttonMedium.rect.collidepoint(x, y))):
						if soundOn:
							sound_blop.play()
						timeAllowed = 20000
						timeStamp = time.time()
						stringTimeStamp = datetime.datetime.fromtimestamp(timeStamp).strftime('%H:%M %m/%d/%Y ')
						startTime = pygame.time.get_ticks()
						gameScreen = 4
					if ((obj_buttonHard.rect.collidepoint(x, y))):
						if soundOn:
							sound_blop.play()
						timeAllowed = 15000
						timeStamp = time.time()
						stringTimeStamp = datetime.datetime.fromtimestamp(timeStamp).strftime('%H:%M %m/%d/%Y ')
						startTime = pygame.time.get_ticks()
						gameScreen = 4
				if ((event.type == pygame.KEYDOWN) or (event.type == pygame.KEYUP)):
					tempName = nameBox.update(events)
					if (isinstance(tempName, basestring)):
						player.setName(tempName)
						nameColor = COLOR_BLUE
						if ((player.getName() == "Chesney") or (player.getName() == "chesney") or (player.getName() == "CHESNEY")):
							#print("Cheat mode activated.")
							cheating = True
						else:
							if (cheating == True):
								#print("Cheat mode deactivated.")
								cheating = False

						nameString = "Name set to " + player.getName() + "."
					else:
						nameString = ""

			nameBox.draw(gameDisplay)

			if ((player.getName() != "No Name") and (player.getName() != "")):
				displayMessage("Name set to " + player.getName() + ".", COLOR_BLACK, (350, 10), scenario_card_font)
			if (cheating == True):
				displayMessage("Cheat mode activated.", COLOR_BLACK, (350, 720), scenario_card_font)

			pygame.display.update() #Updates the screen every frame
			clock.tick(FRAMES_PER_SECOND)

		while (gameScreen == 9 and gameRun):

			while (dataProcessed == False):
				numGreat = 0
				numOkay = 0
				numPoor = 0
				numTimeUp = 0
				endTime = time.time()
				totalPlaytime = (int(round(endTime - timeStamp)))
				playerName = player.getName()
				finalPoints = player.getPoints()
				roundsToComplete = len(diagnosticArray)
				breakdownRectGreatHeading = pygame.Rect(POS_BREAKDOWN_GREAT[0] + 10, POS_BREAKDOWN_GREAT[1] + 10, 108, 150)
				breakdownRectOkayHeading = pygame.Rect(POS_BREAKDOWN_OK[0] + 10, POS_BREAKDOWN_OK[1] + 10, 108, 150)
				breakdownRectPoorHeading = pygame.Rect(POS_BREAKDOWN_POOR[0] + 10, POS_BREAKDOWN_POOR[1] + 10, 108, 150)
				breakdownRectTimeUpHeading = pygame.Rect(POS_BREAKDOWN_TIMEUP[0] + 10, POS_BREAKDOWN_TIMEUP[1] + 10, 108, 150)
				breakdownGreatHeadingRendered = render_textrect("Great responses:", answer_card_font, breakdownRectGreatHeading, COLOR_BLACK, COLOR_WHITE, 1)
				breakdownOkayHeadingRendered = render_textrect("Okay responses:", answer_card_font, breakdownRectOkayHeading, COLOR_BLACK, COLOR_WHITE, 1)
				breakdownPoorHeadingRendered = render_textrect("Poor responses:", answer_card_font, breakdownRectPoorHeading, COLOR_BLACK, COLOR_WHITE, 1)
				breakdownTimeUpHeadingRendered = render_textrect("Ran out of time:", answer_card_font, breakdownRectTimeUpHeading, COLOR_BLACK, COLOR_WHITE, 1)

				if (timeAllowed == 15000):
					difficultyString = "Hard"
				elif (timeAllowed == 20000):
					difficultyString = "Medium"
				elif (timeAllowed == 30000):
					difficultyString = "Easy"
				else:
					difficultyString = "INVALID"

				min, sec = divmod(totalPlaytime, 60)
				playtimeString = "%02d:%02d" % (min, sec)

				for d in diagnosticArray:
					pointsRound = d.getRoundPoints()
					timeRanOut = d.getTimeUp()
					responseTime = d.getTimeToAns()
					totalResponseTime = totalResponseTime + responseTime
					if (pointsRound >= 6):
						numGreat = numGreat + 1
					elif (pointsRound > 0):
						numOkay = numOkay + 1
					elif (pointsRound == 0):
						if (timeRanOut == True):
							numTimeUp = numTimeUp + 1
						else:
							numPoor = numPoor + 1

				numGreatText = big_bold_font.render(str(numGreat), True, COLOR_BLACK)
				numOkayText = big_bold_font.render(str(numOkay), True, COLOR_BLACK)
				numPoorText = big_bold_font.render(str(numPoor), True, COLOR_BLACK)
				numTimeUpText = big_bold_font.render(str(numTimeUp), True, COLOR_BLACK)
				avgResponseTime = int(round((totalResponseTime / roundsToComplete) / 1000))
				dataProcessed = True

			gameDisplay.fill(backgroundColor)
			if (screenshotTaken == True):
				displayMessage('Screenshot saved as "diagnosticOutput.png" in game directory.', COLOR_BLACK, (40, 720), scenario_card_font)
			displayMessage("Player Name: " + playerName,COLOR_BLACK,POS_PLAYER_NAME_REPORT,big_bold_font)
			displayMessage(stringTimeStamp,COLOR_BLACK,POS_TIMESTAMP_REPORT,big_bold_font)
			displayMessage("Avg. Response Time: " + str(avgResponseTime) + " seconds",COLOR_BLACK,POS_DETAIL1_REPORT,scenario_card_font)
			displayMessage("Final Points: " + str(finalPoints),COLOR_BLACK,POS_DETAIL2_REPORT,scenario_card_font)
			displayMessage("Rounds to Complete: " + str(roundsToComplete),COLOR_BLACK,POS_DETAIL3_REPORT,scenario_card_font)
			displayMessage("Total Playtime: " + playtimeString,COLOR_BLACK,POS_DETAIL4_REPORT,scenario_card_font)
			displayMessage("Difficulty: " + difficultyString,COLOR_BLACK,POS_DETAIL5_REPORT,scenario_card_font)
			displayMessage("Response Breakdown:",COLOR_BLACK,POS_BREAKDOWN_TEXT,scenario_card_font)
			gameDisplay.blit(spr_responseBreakdown, POS_BREAKDOWN_GREAT)
			gameDisplay.blit(spr_responseBreakdown, POS_BREAKDOWN_OK)
			gameDisplay.blit(spr_responseBreakdown, POS_BREAKDOWN_POOR)
			gameDisplay.blit(spr_responseBreakdown, POS_BREAKDOWN_TIMEUP)

			gameDisplay.blit(obj_buttonMainMenu.image, obj_buttonMainMenu.rect)
			gameDisplay.blit(obj_buttonScreenshot.image, obj_buttonScreenshot.rect)

			gameDisplay.blit(breakdownGreatHeadingRendered, breakdownRectGreatHeading.topleft)
			gameDisplay.blit(breakdownOkayHeadingRendered, breakdownRectOkayHeading.topleft)
			gameDisplay.blit(breakdownPoorHeadingRendered, breakdownRectPoorHeading.topleft)
			gameDisplay.blit(breakdownTimeUpHeadingRendered, breakdownRectTimeUpHeading.topleft)

			gameDisplay.blit(numGreatText, (POS_BREAKDOWN_GREAT[0] + 50, POS_BREAKDOWN_GREAT[1]+75))
			gameDisplay.blit(numOkayText, (POS_BREAKDOWN_OK[0] + 50, POS_BREAKDOWN_OK[1]+75))
			gameDisplay.blit(numPoorText, (POS_BREAKDOWN_POOR[0] + 50, POS_BREAKDOWN_POOR[1]+75))
			gameDisplay.blit(numTimeUpText, (POS_BREAKDOWN_TIMEUP[0] + 50, POS_BREAKDOWN_TIMEUP[1]+75))

		#NOTE: In order for the output image to correctly contain all elements of the screen, the event handling portion of the while loop needs to come after any drawing that occurs.
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					gameRun = False #Ends the game if they user attempts to close the window
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						gameRun = False
				if event.type == pygame.MOUSEBUTTONDOWN:
					# Set the x, y positions of the mouse click
					x, y = event.pos
					if ((obj_buttonMainMenu.rect.collidepoint(x, y))):
						if soundOn:
							sound_blop.play()
						player.setPoints(0)
						dataProcessed = False
						screenshotTaken = False
						gameScreen = 2
						
					if ((obj_buttonScreenshot.rect.collidepoint(x, y))):
						if soundOn:
							sound_blop.play()
						if (screenshotTaken == False):
							pygame.image.save(gameDisplay, "diagnosticOutput.png")
							screenshotTaken = True
			pygame.display.update() #Updates the screen every frame
			clock.tick(FRAMES_PER_SECOND)

	pygame.quit()
	quit()

gameLoop()