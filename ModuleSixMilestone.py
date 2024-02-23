# Nathan Grzywacz
# Afterlife Rediscovery (Module 7 Milestone Assignment submission)
# It's a little long, but I put a LOT of work into it!

def parse_command(command,aliases):
    if command.strip() == '':
        print('\033[31mYou must command. Time doesn\'t flow here.')
        return 'none'
    args = command.lower().strip().split()  # sets string lowercase, removes leading/trailing whitespace,makes list of words
    for word in args:  # removes whitespace mid-text
        if word == "":
            args.remove(word)

    if args[0] in aliases['move']:  # Check command for functions one at a time
        if not (len(args) > 1):
            print('\033[31mChoose a direction.')
            return('none')
        if args[1] in aliases['north']: # if it's move, make sure the second argument is a valid direction
            return('North')
        elif args[1] in aliases['east']:
            return('East')
        elif args[1] in aliases['south']:
            return('South')
        elif args[1] in aliases['west']:
            return('West')
        else:
            input('\033[31mThat is not a valid direction. Try again')

    elif args[0] in aliases['grab']:
        if (len(args) > 1):
            return('Grab',args[1])
        else:
            print('\033[31mYou didn\'t grab anything.')
            return 'none'
    elif args[0] in aliases['quit']:
        return('Quit')
    elif args[0] in aliases['help']:
        return('Help')
    elif args[0] in aliases['north']:  # otherwise if they just typed a single word, check if its a direction
        return('North')
    elif args[0] in aliases['east']:
        return('East')
    elif args[0] in aliases['south']:
        return('South')
    elif args[0] in aliases['west']:
        return('West')
    else:
        print('The command is not recognized. Try \'help\' if you\'re confused\n')
        return('none')

def print_description(location,rooms,inventory):
    # attempting this formatting because rooms[location]['Direction']['Items'] was not fun to read
    room = rooms[location]
    items = room['Items']
    description = room['Description']
    possible_directions = room['Directions']

    print('\033[35m', end='') # makes stuff purple
    print(('\n' * 18) + location, end='\n')  # clears terminal
    print(description, end='\n\n\n')  # prints the rooms description with some space after
    if not bool(items):  # Should evaluate to false if there are no items in the Items dictionary!
        if(location != 'Light'):
            print('\033[31mNothing left here stands out to you.\n\033[35m')
    else:
        for item in items:  # for each item in your locations Items list, print the description of it
            print(f'An object shines a color against the darkness. The \033[31m{item}\033[35m stands out to you.\n')

    output = '\033[0mIt looks like you can go:\n'
    for direction, room in possible_directions.items():
        output += direction + '\n'
    if(location != 'Light'):  # print where the player can go, unless they're at the end.
        print(output, end='\n\n')
    if (inventory and (location != 'Light')):  # print the players inventory, unless it's empty
        print('inventory:' + str(inventory))

def move(dir, rooms, location): # returns direction of travel if valid
    room = rooms[location]
    directions = room['Directions']

    if dir in directions:
        print(f'\033[31mYou head {dir}, into the {directions[dir]}')
        return directions[dir]
    else:
        print('\033[31mSeems that direction is not one you can... or wish... to go')

def help():  # prints the help screen for the user
    print(('\n' * 18), end='\n')  # clears terminal
    help_screen = (
        "This is the help screen! Below are the commands you're able to type\n\n"
        "\033[31m\'Help\'\033[0m- Brings you to this very screen!\n\n"
        "\033[31m\'Move <direction>\'\033[0m- Allows you to input which direction you'd like to travel in!\n"
        "Available directions are listed above your inventory.\n\n"
        "\033[31m\'Grab <item>\'\033[0m- Allows you to pick up an item and add it to your inventory. Try grabbing something!\n\n"
        "\033[31m\'Quit\'-\033[0m Exits the program and gives you the freedom you deserve.\n"
    )
    print(help_screen)
    print('\n\nPress Enter at any time to return to the game!')

# returns the items name if it exists and removes its value from the dictionary
def grab(item,rooms,location):
    room = rooms[location]
    items = room['Items']
    item_to_pickup = item.strip().lower()

    if not(items):  # If there are no items
        print('\033[35mLike a sandy mist falling through your fingers, you grab at a memory of nothing')
        print('\033[0m\033[3m(It looks like thats not an item you can grab! Is there anything in this room?)\033[23m')
        return('none')

    if(item_to_pickup in items.keys()):  # If the item exists in the room
        print(f'\033[31mYou picked up the {item_to_pickup}\n\n\033[35m' + str(items[item_to_pickup]))
        return(items.pop(item_to_pickup))
    else:
        print('\033[35mLike a sandy mist falling through your fingers, you grab at a memory of nothing')
        print('\033[0m\033[3m(It looks like thats not an item you can grab! Is there anything in this room?)\033[23m')

    return 'none'

def end_game(rooms,ready):
    if ready:
        print(
            "\033[35mYou\'ve collected enough memories to realize what\'s going on right in the nick of time!\n"
            "The light begins to engulf you, but it is no use. Within an instant you break free and leap\n" 
            "down the ladder and out the door. As you make it back to the darkness, the world fades to black.\n"
            "\033[0mMoments later, sirens are blaring in your ears. You open your eyes to find your father hunched over you\n"
            "He's crying, but is releived you are alive.\n"
            "Thats exactly right. You ARE alive... you made it! \033[31mCongratulations. you may live.\n\n\n\033[0m"
            "The end! Thanks for playing!"
              )

    else:
        print("You finally understand. But it\'s too late. The light engulfs you entirely as your vision fades to white.\n"
              "\033[0mYou were claimed by the heavens.\n"
              "Perhaps if you had claimed a bit more memory of your life before the shock, this would have ended differently."
              "\nThe End! Thanks for playing! But... I really do hope you try again!")

def main():
    rooms = {  # Dictionary of the map of rooms and their information nested within.
        'Road': {
            'Description': "A road in the middle of nowhere. You\'re not sure why you are here, or where this road is.\n"
                           "But there is a building to your north, and something to your east",
            # Description of the room

            'Directions': {
                # Dictionary of possible directions of travel. The key will be the command the players input.
                'North': 'Room',
                'East': 'Darkness'
            },
            'Items': {}
        },
        'Room': {
            'Description': "Inside the building. A hollow cube. The room has no discernable features. No color, no light.\n"
                           "The room has exits in every direction. North, however, casts a single alluring beam of light. \nSome light in the eternal "
                           "darkness. But why?",  # Description of the room

            'Directions': {
                # Dictionary of possible directions of travel. The key will be the command the players input.
                'North': 'Attic',
                'East': 'Bedroom',
                'South': 'Road',
                'West': 'Kitchen'
            },
            'Items': {
                'shoe': 'Two shoes, forming a pair with two different shoes. A large work boot, and a pink girl\'s sneaker.'
            }
        },
        'Darkness': {
            'Description': "Darkness. As far as you can see, only darkness.\nSomehow in this void, you failed to immediately notice "
                           "a candle beneath your feet.\nThe poor candle's flame fails to project light onto anything nearby. A strange phenomonon.\n"
                           "You feel uneasy.",  # Description of the room

            'Directions': {
                # Dictionary of possible directions of travel. The key will be the command the players input.
                'West': 'Road'
            },
            'Items': {
                'candle': 'A candle perpetually burning a flame providing no light. It must mean something.'
            }
        },
        'Bedroom': {
            'Description': "From a dark room to a darker one. You can still see the beam of light from the previous room, even if just barely.\n"
                           "This new room feels crowded. A large block persists in the center of the room. soft. A bed maybe.\n"
                           "It is a shame that you don't feel tired. Don't feel much of anything right about now...",
            # Description of the room

            'Directions': {
                # Dictionary of possible directions of travel. The key will be the command the players input.
                'North': 'Closet',
                'West': 'Room'
            },
            'Items': {
                'picture': 'A framed picture, no larger than your hand. Portrays a father and child. The fathers clothes are torn.'
            }
        },
        'Closet': {
            'Description': "A smaller hole leads to this new room. Although... it isn't much of a room. Perhaps a closet.\n"
                           "It would explain the fabric feel of objects dangling infront of you. Bedroom... Closet... This must be someones house.\n"
                           "Wonder who's...\n"
                           "You feel worry.",  # Description of the room

            'Directions': {
                # Dictionary of possible directions of travel. The key will be the command the players input.
                'South': 'Bedroom'
            },
            'Items': {
                'jacket': 'A boys jacket, Clearly out of place. Why does it smell so familiar...'

            }
        },
        'Kitchen': {
            'Description': "Floor turns hard, you can hear your own footsteps now. First bit of sound since you've arrived.\n"
                           "The steps feel interrupted as you're blinded by an orb of reddish light. Like an eclipsed sun in a night sky, burning red.\n"
                           "Vibrantly, it sits alone on a table in a bowl of other colorless fruit. You can't focus on anything else when you're in it's presence.\n"
                           "Why is this object so alluring, yet infuriating.\n"
                           "you feel angry.",  # Description of the room

            'Directions': {
                # Dictionary of possible directions of travel. The key will be the command the players input.
                'East': 'Room'
            },
            'Items': {
                'apple': 'The only thing you can look at. An apple. A harmless fruit.'

            }
        },
        'Attic': {
            'Description': "Bumping into blocks. Floating blocks? No, a ladder. Why was it there? How could you not see it with the light?\n"
                           "Speaking of the light, it is closer now, almost blinding. The light shines all over the room, but illuminates nothing, not even the ladder.\n"
                           "Frustrated now, why is everything perpetually dark? Why are you alone? Memories feel impossible to grasp with this blinding light screaming your name.\n"
                           "It comes from the east.\n"
                           "You feel anticipation.",  # Description of the room

            'Directions': {
                # Dictionary of possible directions of travel. The key will be the command the players input.
                'East': 'Light',
                'South': 'Room'
            },
            'Items': {
                'box': 'A box of forgotten items. A stethoscope, and bodily thermometer lay inside, covered in dust'
            }
        },
        'Light': {
            'Description': "Climbing into the light, it fades. This is the end. You stare out the attic's window.\n"
                           "You see the wreckage on the street below. This was your father's house. The place of your life and half of your family.\n"
                           "But now you don't have any of that now. You are lost.",  # Description of the room
            'Directions': {
                # Dictionary of possible directions of travel. The key will be the command the players input.
                'None': 'There is no escape from the light'  # technically unreachable code, but cool flavor :)
            },
            'Items': {}
        },
    }
    aliases = {  # alternative commands for added simplicity
        'move': ['move', 'm', 'go', 'run', 'flee', 'trudge', 'walk'],
        'grab': ['grab', 'get', 'g', 'pick', 'pickup', 'p', 'lift', 'add'],
        'quit': ['quit', 'q'],
        'help': ['help', 'h'],
        'north': ['north', 'n'],
        'east': ['east', 'e'],
        'south': ['south', 's'],
        'west': ['west', 'w']
    }
    ready = False  # Boolean for when player becomes ready to win the game
    playing = True  # Boolean set false to end the game
    location = 'Road'  # String tracking players location. Initialized at spawn location: Road
    inventory = []  # List containing players items

    while playing:

        print_description(location,rooms,inventory)  # print the description of current location

        if location == 'Light':  # ends the game if the user is on the 'Light' tile
            if(len(inventory) > 5):
                ready = True
            end_game(rooms, ready)
            playing = False
            continue

        command = parse_command(input('\033[0mWhat do you want to do?\n'), aliases)  # Validate and return a proper command.
        # Command will always be a direction or name of a non-move function.
        if (command == None):
            continue
        elif(command in ['North','East','South','West']):  # if the command is a direction
            location_to_move = move(command, rooms, location)
            if not (location_to_move == None):
                location = location_to_move
        elif('Grab' in command):
            item_to_pickup = command[1]
            item = (grab(item_to_pickup, rooms,location))
            if not(item == 'none'):
                inventory.append(item_to_pickup)
        elif(command == 'Help'):
            help()
        elif(command == 'Quit'):
            playing = False;
            print('Thanks for playing! Shame you didn\'t see the end...')
            break
        elif(command == 'none'):
            print('\033[31mTry again.')
        else: print('SOMETHING WENT WRONG.')

        input('\033[0mEnter to continue...')

if __name__ == "__main__":
    print('\n\nWelcome to my game! \nCommands are \'help\' \'move\' \'grab\' and \'quit\'.')
    print('Try a few different inputs too, I made the input relatively robust. You can even just input a direction!\n')
    input('Try \'n\'!\n\033[31mPress Enter to Play')
    main()

