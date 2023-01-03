import random

#global variables: number of players and number of enemies. Initialize empty dict to start:
player_num = 0
enemy_num = 0
dnd_dict=dict()


#define character class
class character:
    def __init__(self, name='', roll=0, dex=0, alive=1, char_align=''):
        self.name=name
        self.roll=roll
        self.dex=dex
        self.alive=alive
        self.char_align=char_align
    def fliplivestate(self):
        self.alive = (-1*self.alive)+1 #alternates between 1 and 0
    def setdex(self):
        while True:
            try:
                self.dex=int(input(f"what is {self.name}'s dexterity? ").strip())
                break
            except:
                print('dexterity must be an integer value. please try again.')
            



#dict defined thusly: player name, roll, dex (default of 0 unless needed),
#living status (1=alive, 0=dead/downed),
#enemy status (1 if enemy, 0 if player or friendly NPC)
#for nat 20 or nat 1: set to 1000 and -1000, respectively.
def create_dict(dnd_dict):

    char_status='players'

    print(f"enter {char_status} one at a time. if no new {char_status}, type 'DONE'. \n ")
    while True:

        while True: #initialize name
            name = input('%s name: ' %('player' if char_status=='players' else 'enemy')).strip().upper()
            if len(name) > 0:
                break
            else:
                print('please enter a valid name.')

        if name == 'DONE':
            if char_status == 'players':
                char_status = 'enemies'
                print(f"\nenter {char_status} one at a time. if no new {char_status}, type 'DONE'. \n ")
                continue
            else:    
                break


        while True: #initialize initiative roll
            try:
                roll = int(input(f"{name}'s roll: ").strip())
                if(roll == 20 or roll == 1):
                    nat=input('natural? (y/n) ')
                    if nat == 'y':
                        if roll == 20:
                            roll = 1000
                        else:
                            roll = -1000
                break
            except:
                print('roll must be an integer value. Please try again.')


        if char_status=='players': #set character alignment based on char_status switch
            align = 0
        else:
            align = 1

        
        player = character(name, roll, 0, 1, align)
        dnd_dict[name] = player
        print(' ')
    
    return dnd_dict




#set players/enemies to dead state:
def flipalive(dnd_dict):
    
    print("please enter who was downed/revived. if finished, type 'DONE'. \n")
    while True:
        try:
            name=input('player/enemy name: ').upper().strip()
            if name == 'DONE':
                print('\n')
                break
            dnd_dict[name].fliplivestate()
        except:
            print("this player/enemy does not exist. please type a valid name or 'DONE'.")




#take players and enemies entered in create_dict and produce a turn order based on rolls and dex scores
def turn_generator(dnd_dict):

    rolls=[dnd_dict[k].roll for k in dnd_dict.keys()]
    rolls=list(set(rolls))
    rolls.sort(reverse=True)
    
    turn_order=list()
    
    for r in rolls:
        
        players = [dnd_dict[k].name for k in dnd_dict.keys() if dnd_dict[k].roll==r and dnd_dict[k].alive==1] #match roll and is alive
        
        if len(players) == 1:
            
            turn_order.append(players[0])
            
        else:
        
            for p in players: #if multiple players, first determine their dex
                if dnd_dict[p].dex==0:
                    dnd_dict[p].setdex()
                    
            dex_list=[dnd_dict[p].dex for p in players]
            dex_list=list(set(dex_list))
            dex_list.sort(reverse=True)

            for d in dex_list:
                dex_players=[p for p in players if dnd_dict[p].dex==d]
                
                if len(dex_players) == 1:
                    turn_order.append(dex_players[0])
                else:
                    random.shuffle(dex_players)
                    for dp in dex_players:
                        turn_order.append(dp)

    return turn_order






#game loop
dnd_dict=create_dict(dnd_dict) #initialize turn order
round_num=1


print('\n\n') #separate game loop from initialization inputs
while True:

    player_num = len([p for p in dnd_dict.keys() if dnd_dict[p].char_align==0 and dnd_dict[p].alive==1])
    enemy_num = len([e for e in dnd_dict.keys() if dnd_dict[e].char_align==1 and dnd_dict[e].alive==1])
    
    if player_num == 0 or enemy_num == 0:
        if player_num == 0:
            print('\nCOMBAT OVER. ENEMIES WIN.')
        else:
            print('\nCOMBAT OVER. PLAYERS WIN.')
        break
    
    turn_order=turn_generator(dnd_dict)
    downed=[k for k in dnd_dict.keys() if dnd_dict[k].alive==0]
    
    print(f'\nROUND {round_num} \n')
    
    print('TURN ORDER:')
    for p in turn_order:
        print(p)
    print('\n')

    if len(downed) > 0:
        print('DOWNED:')
        for p in downed:
            print(p)
        print('\n')

    while True:
        flipalive_check=input('anyone downed/revived? (y/n): ').lower().strip()
        if flipalive_check != 'y' and flipalive_check != 'n':
            print("input must be either 'y' or 'n'. please try again.")
        else:
            break
            
    if flipalive_check == 'y':
        flipalive(dnd_dict)


    while True:
        new_players=input('any new players/enemies? (y/n): ').lower().strip()
        if new_players != 'y' and new_players != 'n':
            print("input must be either 'y' or 'n'. please try again.")
        else:
            break
            
    if new_players == 'y':
        dnd_dict=create_dict(dnd_dict)

    round_num += 1










    
    
