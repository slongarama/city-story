#!/usr/bin/env python3

import serial # sudo pip install pyserial
import os
import random
import time
ser = serial.Serial('/dev/ttyUSB0', 9600) # For Raspberry Pi
# ser = serial.Serial('/dev/tty.SLAB_USBtoUART', 9600) # For Macbook

## ---------------------------------------------------------------------
## ---------------------------------------------------------------------
## INSTRUCTIONS FOR USE


## ---------------------------------------------------------------------
## ---------------------------------------------------------------------

# List of all available block tags
landtags = ['body-outline', 'utensils', 'door', 'dog', 'panther', 'pyramid', 'bank', 'treasure', 'skyscraper']
watertags = ['people', 'boat', 'birds']

# ---------------------------------------------------------------
# Declare voltage values for all blocks
landvals = {
    .4: 'body-outline',
    .54: 'utensils',
    .88: 'door',
    1.15: 'dog',
    1.39: 'panther',
    1.6: 'pyramid',
    1.98: 'bank',
    2.38: 'treasure',
    3: 'skyscraper',
}

seavals = {
    1.15: 'people',
    1.6: 'boat',
    2.38: 'birds',
}

# ---------------------------------------------------------------
# Accompanying story text for each block
paragraphs = {
    'body-outline': 'You were taking a tour around the local high school when you see a faint shadow on the floor, from far away. It looks like... a body?\n\nYou get closer. Is that an... outline of a body....?? A dead body??',
    'utensils': "On a quest to find the culprit, you decide to visit the local diner. They waitresses always know what's going on around town, and the gossip is hot today. You buy yourself a flat white and sit down, notebook in hand.",
    'door': "You notice around the town that many houses have beautiful red doors, and you wonder where they came from. What an odd town tradition. You inquire with your local guide, but he dismisses it offhandedly. Looks like it's not a clue.",
    'dog': "Aww, look a cute puppy! You run over to pet the dog and are immediately distracted. The dog owner is clearly angry with you, and it looks like this act of yours hasn't bought you any favors in town.",
    'panther': "The talk around the town is that the zookeeper has been acting fishy lately. Or is it... the aquarium keeper? Either way, you head downtown to investigate.",
    'pyramid': "There is a Mason temple at the edge of town, but it is largely abandoned now. You wonder when it was built, and what happened to its inhabitants. You even try to peak inside, but the dust on the ground is thick as carpet. Looks like nobody has been inside for ages.",
    'bank': "You head to the bank, because why else do people commit crimes. You're sure that if you follow the money, you'll be one step closer to finding the truth.",
    'treasure': "At the museum, you are amazed by the extensive and *very* expensive collection. You think to yourself how lucrative it would be to rob the museum, how it would make the museum a prime target. That, combined with the fact that the Atwoods are ardent investors in the the arts is very interesting.",
    'skyscraper': "The city is industrializing quickly. Town residents say that even in the last year, over three skyscrapers have started construction. You wonder if the real estate boom isn't turning some people's heats to greed.",
    'people': "You talk to the alien fanatic in town. His name is Bob, you know his type. Before you can even get a word out of your mouth, he starts talking about UFO's and alien landings in Iowa. You decide it's best to leave him alone.",
    'boat': "Thinking that a boat ride might offer you some fresh perspective, you take to the water. The view is beautiful, but it doesn't get you much further in the case.",
    'birds': "You arrive at the town hall to see that it is surrounded by birds. They're practically swarming, but you fight your way through up the front steps to talk to the mayor."
}


def getTags(parsed):
    ret = []
    val = parsed[0]

    # water vals
    if val < 1.20 and val > 1.10:
        ret.append('people')
    elif val < 1.65 and val > 1.55:
        ret.append('boat')
    elif val < 2.43 and val > 2.33:
        ret.append('birds')

    # land vals
    land = parsed[1:4]
    for val in land:
        if val < .45 and val > .35:
            ret.append('body-outline')
        elif val < .60 and val > .49:
            ret.append('utensils')
        elif val < .92 and val > .84:
            ret.append('door')
        elif val < 1.29 and val > 1.10:
            ret.append('dog')
        elif val < 1.45 and val > 1.34:
            ret.append('panther')
        elif val < 1.65 and val > 1.55:
            ret.append('pyramid')
        elif val < 2.03 and val > 1.93:
            ret.append('bank')
        elif val < 2.43 and val > 2.33:
            ret.append('treasure')
        elif val < 3.05 and val > 2.95:
            ret.append('skyscraper')

    return ret

def parseSerial(serialData):
	splitSerial = str(serialData, 'utf-8')
	splitSerial = splitSerial.split('--')
	parsed = []
	for val in splitSerial:
		parsed.append(float(val))
	return parsed

def printParagraph(tag):
    val = paragraphs.get(tag)
    print(val)

def createStory():
    ## ---------------------------------------------------------------------
    ## INTRO SEQUENCE
    ## ---------------------------------------------------------------------

    os.system('clear')
    name = input("Welcome to Hillville. What's your name?\n>>> ")

    os.system('clear')
    input(f"Hello, {name}! We're so glad you decided to visit our little neck of the woods. What brought you here today?\n>>> ")

    os.system('clear')
    print("\nOh, good!\n... ... ...\n... ... ...\n... ... ...\n... ... ...\n\n")
    print("It's so nice to have a visitor that didn't come just to gawk, for once... At who, you say? \n\nAt the Atwoods' of course, the big family up the hill.\n\nThat poor family. SUCH a tragedy. \n\nThough, and don't tell anyone I said this... Sometimes you can't help but wonder if they brought all this upon themselves...")

    print('\n**********************************************************************************************')
    print('**********************************************************************************************\n')

    ## ---------------------------------------------------------------------
    ## INSTRUCTIONS
    ## ---------------------------------------------------------------------
    time.sleep(5)

    print('Instructions:\n-- Each block represents a different component of the story.\n-- Mix and match blocks to sleuth out and unlock more details.\n-- Visit the maps in left to right, top down order.\n-- Find the perfect combination of blocks to solve the mystery.\n\n')

    print('\n**********************************************************************************************')
    print('**********************************************************************************************\n')

    time.sleep(4)

    print(f"And so, the journey of our brave hero {name} began.")

    time.sleep(10)


    ## ---------------------------------------------------------------------
    ## RANDOMLY CHOOSE ANSWER ARRAY
    ## ---------------------------------------------------------------------

    tags = []
    answer = []
    answer.append(random.choice(watertags))
    landanswers = random.sample(landtags, 3)

    for val in landanswers:
        answer.append(val)

    ## ---------------------------------------------------------------------
    ## START READING FROM SERIAL
    ## ---------------------------------------------------------------------

    while True:
        try:
            serialData = ser.readline()
            parsed = parseSerial(serialData)

            if len(parsed) != 4:
                continue

            oldtags = tags
            tags = getTags(parsed)

            if oldtags != tags:
                os.system('clear')
                print("Oh! You've visited a new place. I wonder what's going to happen now...")
                print("\n... ... ...\n... ... ...\n... ... ...\n... ... ...\n\n")

                for tag in tags:
                    printParagraph(tag)
                    print()

            ## -----------------------------------------------------------------
            ## ANSWER SEQUENCE
            ## -----------------------------------------------------------------

            if tags == answer:
                time.sleep()

                print(f"\nWait.\n\nWait a minute. Is this really right? Did you... solve the mystery of what happened to the Atwoods? \n\nEgad! You're a genius, {name}. Thank you for your service to this community!")

                print('\n**********************************************************************************************')
                print('**********************************************************************************************\n')

                print('\n\nThanks for playing! Good job solving the mystery. I know it was a tough one. Press Ctrl-C to start the game over!')

                try:
                    time.sleep(1000)
                except KeyboardInterrupt:
                    break

        except KeyboardInterrupt:
            break
        except Exception as e:
            print(e)

def main():
    while True:
        createStory()


if __name__ == "__main__":
	main()
