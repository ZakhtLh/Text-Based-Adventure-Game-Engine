import json
import random

#---Notes---#
#Make the game have more "milestone" progression to the story
#Some variable names share a name with a python instruction which is bad practice.
#Rather messy code
#Repeated code with only minor differences between them = bad
#Make a guide on how to create a compatible game through the json files
#Maybe have error checking if the creator has made an error (i.e "this room does not exist")
#Implement aggresiveness of npcs
#parse input is not currently working properly

#Either turn parse validate in just validating that a function exists with that name, remove parse validate and do function existing validation in "action" (or similar), or do a try except.
#calling npcs with a 2=< word long name doesn't work without including "_" in the input.
#Add aggressive functonality.

#Programming 1 - CW2 - Group Project:
#Universally Challenged

def update_save_file(save_file_dict,save_file_num):
    file_name="save_file_"+save_file_num+".json"
    with open(file_name, "w") as write_file:
        json.dump(save_file_dict, write_file,indent=4)
    write_file.close()

def read_save_file(save_file_num):
    file_name="save_file_"+save_file_num+".json"
    with open(file_name, mode="r") as read_file:   
        save_file_dict = json.load(read_file)
    read_file.close
    return(save_file_dict)

def read_default_save_file():
    with open("default_save_file.json", mode="r") as read_file:   
       default_save_file_dict = json.load(read_file)
    read_file.close
    return(default_save_file_dict)

def read_game_map():
    with open("game_map.json", mode="r") as read_file:   
        game_map_dict = json.load(read_file)
    read_file.close
    return(game_map_dict)

def read_items():
    with open("items.json", mode="r") as read_file:   
        items_dict = json.load(read_file)
    read_file.close
    return(items_dict)

def read_player():
    with open("player.json", mode="r") as read_file:   
        player_dict = json.load(read_file)
    read_file.close
    return(player_dict)

def read_npcs():
    with open("npcs.json", mode="r") as read_file:   
        npcs_dict = json.load(read_file)
    read_file.close
    return(npcs_dict)

def __init__():
    #List of Valid commands
    verb_commands=["go","drop","pickup","quit","help","view"]
    noun_commands=["north","east","south","west"]
    exit,save_file_num=start_menu()
    save_file_dict=read_save_file(save_file_num)
    game_map_dict=read_game_map()
    current_room=save_file_dict["save_file"]["player"]["current_room"]
    reset_player_health(save_file_num)
    return(verb_commands,noun_commands,exit,save_file_num)

def overwrite_saved(save_file_num):
    default_save_file_dict=read_default_save_file()
    default_save_file_dict["save_file"]=default_save_file_dict.pop("default_save_file")
    update_save_file(default_save_file_dict,save_file_num)

def saved_choice(option):
    print(f"Select saved game to {option}")
    save_file_1_dict=read_save_file("1")
    print(f"1 - {save_file_1_dict["save_file"]["player"]["current_room"]}")
    save_file_2_dict=read_save_file("2")
    print(f"2 - {save_file_2_dict["save_file"]["player"]["current_room"]}")
    save_file_3_dict=read_save_file("3")
    print(f"3 - {save_file_3_dict["save_file"]["player"]["current_room"]}")
    save_file_num="0"
    while ord(save_file_num)<49 or ord(save_file_num)>51: #Keeps asking the user for an input until it is valid. The Ord value gets the ascii value. 49 in ascii is "1" and 51 in ascii is "3".
        save_file_num=input()
        if save_file_num=="":
            print("Please enter valid option")
            save_file_num="0"
    if option=="overwrite":
        overwrite_saved(save_file_num)
    return(save_file_num)

def view_npcs(save_file_num):
    save_file_dict=read_save_file(save_file_num)
    current_room=save_file_dict["save_file"]["player"]["current_room"]
    if save_file_dict["save_file"]["game_map"][current_room]["location_npcs"]==None:
        print("There are no NPCs in this room")
    else:
        for npc in save_file_dict["save_file"]["game_map"][current_room]["location_npcs"]:
            print(npc.capitalize().replace("_"," "))

def player_options(save_file_num): #Displays the player what their options are and asks for an input
    #Player options
    game_map_dict=read_game_map()
    save_file_dict=read_save_file(save_file_num)
    current_room=save_file_dict["save_file"]["player"]["current_room"]
    print()
    print("#---OPTIONS---#")
    print(f"Current room: {current_room.replace("_", " ")}")
    print(game_map_dict["game_map"]["room_descriptions"][current_room])
    print()
    print("What would you like to do?")
    print()
    print("Go...") #Command is "go 'cardinal direction'"
    print(f"North - {game_map_dict["game_map"]["room_connections"][current_room]["north"].replace("_", " ")}")
    print(f"East - {game_map_dict["game_map"]["room_connections"][current_room]["east"].replace("_", " ")}")
    print(f"South - {game_map_dict["game_map"]["room_connections"][current_room]["south"].replace("_", " ")}")
    print(f"West - {game_map_dict["game_map"]["room_connections"][current_room]["west"].replace("_", " ")}")
    print()
    print("Drop...") #Command is "drop 'item_name'"
    temp=view_inventory(save_file_num)
    print("Pickup...") #Command is "pickup 'item_name'"
    view_dropped_items(save_file_num)
    print()
    print("Interact With:")
    view_npcs(save_file_num)
    print()
    print("View Stats")
    print("Help")
    print("Quit")

def check_key(seperated,save_file_num): #Checks if player has correct key
    save_file_dict=read_save_file(save_file_num)
    game_map_dict=read_game_map()
    current_room=save_file_dict["save_file"]["player"]["current_room"]
    key=game_map_dict["game_map"]["room_connections"][current_room][seperated[1]]+"_"+"key"
    if key in save_file_dict["save_file"]["player"]["inventory"]:
        return(True)
    else:
        return(False)

def is_empty(choice):
    if choice=="":
        return(True)
    else:
        return(False)

def verb_check(seperated,verb_commands):
    if seperated[0] in verb_commands:
        return(True)
    else:
        return(False)

def single_command(seperated):
    if len(seperated)==1:
        return(True)
    else:
        return(False)

def is_movement(seperated,noun_commands):
    if seperated[0]=="go" and seperated[1] in noun_commands:
            return(True)
    return(False)

def is_accessible(seperated,current_room,save_file_dict,game_map_dict):
    if save_file_dict["save_file"]["game_map"][game_map_dict["game_map"]["room_connections"][current_room][seperated[1]]]["accessible"]==False:#Checks whether the room chosen to move to is accessible
        return(False)
    else:
        return(True)

def item_movement(seperated):
    if (seperated[0]=="pickup" or seperated[0]=="drop") and len(seperated)>1:
        return(True)
    else:
        return(False)

def npc_name(seperated,save_file_dict,current_room):
    if single_command(seperated):
        print(seperated[0].replace(" ","_"))
        if seperated[0].replace(" ","_") in save_file_dict["save_file"]["game_map"][current_room]["location_npcs"]:
            seperated.append(seperated[0])
            seperated[0]="npc_interact"
            return(True,seperated)
    return(False,seperated)

def check_stats(seperated):
    if seperated[1]=="stats":
        return(True)
    else:
        return(False)
    
def parse_validate_input(verb_commands,noun_commands,choice,save_file_num): #Checks if the input is valid from 2 lists for each half for the input.
    if is_empty(choice):#If the inputs inputs nothing
        return(False,"")
    seperated=choice.split()
    save_file_dict=read_save_file(save_file_num)
    current_room=save_file_dict["save_file"]["player"]["current_room"]
    npc_result,seperated=npc_name(seperated,save_file_dict,current_room)
    if npc_result:
        return(True,seperated)
    if not verb_check(seperated,verb_commands):
        return(False,seperated)
    if single_command(seperated):
        return(True,seperated)
    if is_movement(seperated,noun_commands):
        game_map_dict=read_game_map()
        if not is_accessible(seperated,current_room,save_file_dict,game_map_dict):
            if game_map_dict["game_map"]["room_connections"][game_map_dict["game_map"]["room_connections"][current_room][seperated[1]]]!="wall":
                if check_key(seperated,save_file_num):
                    print("You use your key to open the door")
                    save_file_dict["save_file"]["game_map"][current_room].update({"accessible":True})
                    update_save_file(save_file_dict,save_file_num)
                    print("Door Unlocked...")
                    return(True,seperated)
                else:
                    print("Locked")
            else:
                print("Inaccessible")
        else:
            return(True,seperated)
    if check_stats(seperated):
        return(True,seperated)
    if item_movement(seperated):
        verb=seperated[1]
        for i in range(2,len(seperated)):
            verb+="_"+seperated[i]
        seperated[1]=verb
        return(True,seperated)
    return(False,seperated)

def quit(seperated,exit,save_file_num): #Saves the room the player was in when they quit for the next time they play. This will be expanded upon to add more stuff saved and the ability to save to a seperate file
    exit=True
    print("Exiting...")
    print("Exited")
    return(exit)

def talk(seperated,exit,save_file_num):
    npcs_dict=read_npcs()
    print(npcs_dict["npcs"][seperated[1]]["dialogue"])
    return(exit)

def item_stats(item,save_file_num):
    items_dict=read_items()
    for key,value in items_dict["items"][item].items():
        print(f"{key.replace("_"," ").capitalize()} - {value}")

def view_npc_inventory(save_file_num,seperated):
    save_file_dict=read_save_file(save_file_num)
    npcs_dict=read_npcs()
    if save_file_dict["save_file"]["npcs"][seperated[1]]["inventory"]!=None:
        items_dict=read_items()
        for item in save_file_dict["save_file"]["npcs"][seperated[1]]["inventory"]:
            print(item.replace("_"," ").capitalize())
            item_stats(item,save_file_num)
            print(f"{seperated[1].capitalize()} will sell this item for {round(items_dict["items"][item]["value"]*npcs_dict["npcs"][seperated[1]]["markup"])}")
            print()
        return(True)
    else:
        print("NPC inventory empty")
        return(False) 

def remove_item(item,save_file_num):
    save_file_dict=read_save_file(save_file_num)
    items_dict=read_items()
    save_file_dict["save_file"]["player"]["current_carry_weight"]-=items_dict["items"][item]["weight"]
    save_file_dict["save_file"]["player"]["inventory"].remove(item)
    update_save_file(save_file_dict,save_file_num)

def add_item(item,save_file_num):
    save_file_dict=read_save_file(save_file_num)
    items_dict=read_items()
    if weight_check(item,save_file_num):
        save_file_dict["save_file"]["player"]["current_carry_weight"]+=items_dict["items"][item]["weight"]
        save_file_dict["save_file"]["player"]["inventory"].insert(0,item)
        update_save_file(save_file_dict,save_file_num)
        return(True)
    return(False)

def weight_check(item,save_file_num):
    save_file_dict=read_save_file(save_file_num)
    items_dict=read_items()
    player_dict=read_player()
    if save_file_dict["save_file"]["player"]["current_carry_weight"]>=player_dict["player"]["carry_weight"]:
        print("Inventory Full")
        return(False)
    elif (save_file_dict["save_file"]["player"]["current_carry_weight"]+items_dict["items"][item]["weight"])>player_dict["player"]["carry_weight"]:
        print("You do not have the inventory space for this item")
        return(False)
    else:
        return(True)

def sell(seperated,exit,save_file_num):
    save_file_dict=read_save_file(save_file_num)
    print("Your coins:")
    print(save_file_dict["save_file"]["player"]["coins"])
    print(f"{seperated[1].capitalize()}s coins:")
    print(save_file_dict["save_file"]["npcs"][seperated[1]]["coins"])
    print()
    print("Player Items:")
    if not view_inventory_sell(save_file_num,seperated):
        return(exit)
    print("Enter item to sell")
    choice=input().lower().replace(" ", "_")
    print()
    if choice not in save_file_dict["save_file"]["player"]["inventory"]:
        print("You do not own this item")
    else:
        items_dict=read_items()
        if items_dict["items"][choice]["value"]<=save_file_dict["save_file"]["npcs"][seperated[1]]["coins"]:
            remove_item(choice,save_file_num)
            save_file_dict=read_save_file(save_file_num)
            save_file_dict["save_file"]["npcs"][seperated[1]]["inventory"].insert(0,choice)
            save_file_dict["save_file"]["player"]["coins"]+=items_dict["items"][choice]["value"]
            save_file_dict["save_file"]["npcs"][seperated[1]]["coins"]-=items_dict["items"][choice]["value"]
            update_save_file(save_file_dict,save_file_num)
            print(f"{choice.replace("_", " ")} bought for {items_dict["items"][choice]["value"]} and added to {seperated[1].capitalize()}s inventory...")
            print(f"You now have {save_file_dict["save_file"]["player"]["coins"]} coins")
            print(f"{seperated[1].capitalize()} now has {save_file_dict["save_file"]["npcs"][seperated[1]]["coins"]} coins")
        else:
            print(f"{seperated[1].capitalize()} cannot afford this item")
    return(exit)

def buy(seperated,exit,save_file_num):
    save_file_dict=read_save_file(save_file_num)
    print("Your coins:")
    print(save_file_dict["save_file"]["player"]["coins"])
    print(f"{seperated[1].capitalize()}s coins:")
    print(save_file_dict["save_file"]["npcs"][seperated[1]]["coins"])
    print()
    print(f"{seperated[1].capitalize()}s Items:")
    if not view_npc_inventory(save_file_num,seperated):
        return()
    print()
    print("Enter item to buy")
    choice=input().lower().replace(" ", "_")
    print()
    if choice not in save_file_dict["save_file"]["npcs"][seperated[1]]["inventory"]:
        print(f"{seperated[1].capitalize()} does not own this item")
    else:
        items_dict=read_items()
        npcs_dict=read_npcs()
        sell_value=round(items_dict["items"][choice]["value"]*npcs_dict["npcs"][seperated[1]]["markup"])
        if sell_value<=save_file_dict["save_file"]["player"]["coins"]:
            if add_item(choice,save_file_num):
                save_file_dict=read_save_file(save_file_num)
                save_file_dict["save_file"]["npcs"][seperated[1]]["inventory"].remove(choice) #Removing the item from the items dropped in the room #Adding the picked up item to the players inventory
                save_file_dict["save_file"]["player"]["coins"]-=sell_value
                save_file_dict["save_file"]["npcs"][seperated[1]]["coins"]+=sell_value
                update_save_file(save_file_dict,save_file_num)
                print(f"{choice.replace("_", " ")} bought for {sell_value} and added to inventory...")
                print(f"You now have {save_file_dict["save_file"]["player"]["coins"]} coins")
                print(f"{seperated[1].capitalize()} now has {save_file_dict["save_file"]["npcs"][seperated[1]]["coins"]} coins")
        else:
            print("You cannot afford this item")
    return(exit)

def trade(seperated,exit,save_file_num):
    npc_commands=["buy","sell","leave"]#So i don't have to call parse_valid_input() again.
    choice=""
    while choice!="leave":
        choice=""
        print()
        print("Buy")
        print("Sell")
        print("Leave")
        print()
        while choice not in npc_commands:
            choice=input().lower()
            if choice in npc_commands and choice!="leave":
                seperated.append(seperated[0])
                seperated[0]=choice
                exit=action(seperated,exit,save_file_num)
            elif choice=="leave":
                return(exit)
            else:
                print("Enter valid option")
    return(exit)

def reset_npc_health(seperated,save_file_num):
    save_file_dict=read_save_file(save_file_num)
    npcs_dict=read_npcs()
    if save_file_dict["save_file"]["npcs"][seperated[1]]["current_health"]>0:
        save_file_dict["save_file"]["npcs"][seperated[1]]["current_health"]=npcs_dict["npcs"][seperated[1]]["max_health"]
    update_save_file(save_file_dict,save_file_num)

def reset_player_health(save_file_num):
    save_file_dict=read_save_file(save_file_num)
    player_dict=read_player()
    save_file_dict["save_file"]["player"]["current_health"]=player_dict["player"]["max_health"]
    update_save_file(save_file_dict,save_file_num)

def fight_won(seperated,save_file_num):
    save_file_dict=read_save_file(save_file_num)
    npcs_dict=read_npcs()
    print(f"You killed {seperated[1].capitalize()}")
    print(npcs_dict["npcs"][seperated[1]]["death_dialogue"])
    for item_to_drop in save_file_dict["save_file"]["npcs"][seperated[1]]["inventory"]:
        save_file_dict["save_file"]["game_map"][save_file_dict["save_file"]["player"]["current_room"]]["room_inventory"].insert(0,item_to_drop)
    save_file_dict["save_file"]["game_map"][save_file_dict["save_file"]["player"]["current_room"]]["location_npcs"].remove(seperated[1])
    update_save_file(save_file_dict,save_file_num)
    npc_unlock(seperated,save_file_num)
    return("run")

def death(seperated,save_file_num):
    game_map_dict=read_game_map()
    print(f"You were killed by {seperated[1].capitalize()}!")
    print(game_map_dict["game_map"]["story"]["death_text"])
    reset_player_health(save_file_num)
    reset_npc_health(seperated,save_file_num)
    exit()

def player_turn(seperated,save_file_num):
    save_file_dict=read_save_file(save_file_num)
    item_dict=read_items()
    print("Players Turn")
    damage=random.randrange(item_dict["items"][save_file_dict["save_file"]["player"]["equipped_item"]]["damage"]-5,item_dict["items"][save_file_dict["save_file"]["player"]["equipped_item"]]["damage"]+5)
    if damage<0:
        damage=0
    if (save_file_dict["save_file"]["npcs"][seperated[1]]["current_health"]-damage)<1:
        return(damage)
    save_file_dict["save_file"]["npcs"][seperated[1]]["current_health"]-=damage
    print(f"You attack and deal {damage} points of damage")
    print(f"{seperated[1].capitalize()}s health:")
    print(f"{save_file_dict["save_file"]["npcs"][seperated[1]]["current_health"]}")
    print()
    update_save_file(save_file_dict,save_file_num)
    return(damage)

def npc_turn(seperated,save_file_num,move):
    save_file_dict=read_save_file(save_file_num)
    npcs_dict=read_npcs()
    npc_damage=random.randrange(npcs_dict["npcs"][seperated[1]]["damage"]-5,npcs_dict["npcs"][seperated[1]]["damage"]+5)
    if npc_damage<0:
        npc_damage=0
    if move=="block":
        npc_damage=block(seperated,npc_damage,save_file_num)
    print(f"{seperated[1].capitalize()}s turn")
    if save_file_dict["save_file"]["player"]["current_health"]-npc_damage<1:
        death(seperated,save_file_num)
    else:
        save_file_dict["save_file"]["player"]["current_health"]-=npc_damage
        update_save_file(save_file_dict,save_file_num)
        print(f"{seperated[1].capitalize()} attacks and deals {npc_damage} points of damage")
        print("Your health:")
        print(save_file_dict["save_file"]["player"]["current_health"])

def attack(seperated,exit,save_file_num):
    #remove durability each attack
    save_file_dict=read_save_file(save_file_num)
    damage=player_turn(seperated,save_file_num)
    npc_turn(seperated,save_file_num,"attack")
    if (save_file_dict["save_file"]["npcs"][seperated[1]]["current_health"]-damage)<1:
        return(fight_won(seperated,save_file_num))
    return("")

def block(seperated,npc_damage,save_file_num):
    if isinstance(npc_damage,int) and not isinstance(npc_damage,bool):
        block_percent=random.randrange(0,100,10)/100
        new_damage=npc_damage
        new_damage*=block_percent
        new_damage=round(new_damage)
        print(f"Player blocked {round((1-block_percent)*100)}% of {npc_damage}")
        print(f"New taken damage (rounded) - {new_damage}")
        return(new_damage)
    else:
        npc_turn(seperated,save_file_num,"block")
        return(False)

def view_weapons(save_file_num):
    save_file_dict=read_save_file(save_file_num)
    item_dict=read_items()
    weapons=[]
    if save_file_dict["save_file"]["player"]["inventory"]==None:
        print("You inventory is empty")
        print("Fists are equipped")
        print()
        save_file_dict["save_file"]["player"]["equipped_item"]="fists"
        return(False,weapons)
    else:
        for item in save_file_dict["save_file"]["player"]["inventory"]:
            if item_dict["items"][item]["damage"]>0:
                weapons.append(item)
                print(f"{item.replace("_", " ").capitalize()} - Damage: {item_dict["items"][item]["damage"]}")
        print()
        return(True,weapons)

def change(seperated,exit,save_file_num):
    save_file_dict=read_save_file(save_file_num)
    valid,weapons=view_weapons(save_file_num)
    if valid:
        print("Enter weapon to change with")
        choice=input().lower().replace(" ","_")
        if choice in weapons:
            save_file_dict["save_file"]["player"]["equipped_item"]=choice
        else:
            print("You do not have this item")
    update_save_file(save_file_dict,save_file_num)
    return("")

def equipped_weapon(save_file_num):
    save_file_dict=read_save_file(save_file_num)
    if save_file_dict["save_file"]["player"]["equipped_item"] not in save_file_dict["save_file"]["player"]["inventory"]:
        save_file_dict["save_file"]["player"]["equipped_item"]="fists"
    update_save_file(save_file_dict,save_file_num)

def fight(seperated,exit,save_file_num):
    npc_commands=["attack","block","run","change"]
    choice=""
    save_file_dict=read_save_file(save_file_num)
    save_file_dict["save_file"]["npcs"][seperated[1]]["aggressive"]=True
    update_save_file(save_file_dict,save_file_num)
    equipped_weapon(save_file_num)
    while choice!="run":
        while choice not in npc_commands:
            item_dict=read_items()
            npcs_dict=read_npcs()
            choice=""
            print()
            print("Attack")
            print("Block")
            print("Run")
            print(f"Equipped Weapon: {save_file_dict["save_file"]["player"]["equipped_item"].capitalize()} Damage - {item_dict["items"][save_file_dict["save_file"]["player"]["equipped_item"]]["damage"]}")
            print("Change")
            print()
            print(f"{seperated[1].capitalize()}s Damage - {npcs_dict["npcs"][seperated[1]]["damage"]}")
            print()
            choice=input().lower()
            if choice in npc_commands and choice!="run":
                seperated.append(seperated[0])
                seperated[0]=choice
                choice=action(seperated,exit,save_file_num)
                if save_file_dict["save_file"]["npcs"][seperated[1]]["current_health"]<1:
                    return("leave")
            elif choice=="run":
                return("")
            else:
                print("Enter valid option")
    return("")

def npc_unlock(seperated,save_file_num):
    save_file_dict=read_save_file(save_file_num)
    npcs_dict=read_npcs()
    if npcs_dict["npcs"][seperated[1]]["room_unlock"]!=None:
        print("rooms now accessible:")
        for room in npcs_dict["npcs"][seperated[1]]["room_unlock"]:
            save_file_dict["save_file"]["game_map"][room]["accessible"]=True
            print(room.replace("_"," "))
            update_save_file(save_file_dict,save_file_num) #Doesn't seem to be saving for some reason

def npc_interact(seperated,exit,save_file_num):
    npc_commands=["talk","trade","fight","leave"]#So i don't have to call parse_valid_input() again.
    choice=""
    while choice!="leave":
        choice=""
        while choice not in npc_commands:
            print()
            print("Talk")
            print("Trade")
            print("Fight")
            print("Leave")
            print()
            choice=input().lower()
            if choice in npc_commands and choice!="leave":
                seperated.append(seperated[0])
                seperated[0]=choice
                choice=action(seperated,exit,save_file_num)
            else:
                print("Enter valid option")
    reset_player_health(save_file_num)
    reset_npc_health(seperated,save_file_num)
    return(exit)

def view_inventory(save_file_num):
    save_file_dict=read_save_file(save_file_num)
    if save_file_dict["save_file"]["player"]["inventory"]==None:
        print("You inventory is empty")
        print()
        return(False)
    else:
        for item in save_file_dict["save_file"]["player"]["inventory"]:
            print(item.replace("_"," ").capitalize())
        print()
        return(True)
    
def view_inventory_sell(save_file_num,seperated):
    save_file_dict=read_save_file(save_file_num)
    if save_file_dict["save_file"]["player"]["inventory"]==None:
        print("You inventory is empty")
        print()
        return(False)
    else:
        items_dict=read_items()
        for item in save_file_dict["save_file"]["player"]["inventory"]:
            print(item.replace("_"," ").capitalize())
            item_stats(item,save_file_num)
            print(f"{seperated[1].capitalize()} will buy this item for {items_dict["items"][item]["value"]}")
            print()
        print()
        return(True)

def view(seperated,exit,save_file_num):
    if seperated[1]=="stats":
        save_file_dict=read_save_file(save_file_num)
        if save_file_dict["save_file"]["player"]["inventory"]==None:
            print("You inventory is empty")
            print()
            return(False)
        else:
            items_dict=read_items()
            for item in save_file_dict["save_file"]["player"]["inventory"]:
                print(item.replace("_"," ").capitalize())
                item_stats(item,save_file_num)
                print()
            print()
    return(exit)

def game_won():
    game_map_dict=read_game_map()
    print(game_map_dict["game_map"]["room_descriptions"][game_map_dict["game_map"]["room_properties"]["end_room"]])
    print(game_map_dict["game_map"]["story"]["end_text"])

def go(seperated,exit,save_file_num):
    game_map_dict=read_game_map()
    save_file_dict=read_save_file(save_file_num)
    current_room=save_file_dict["save_file"]["player"]["current_room"]
    print(f"You have moved {seperated[1]} into room: {game_map_dict["game_map"]["room_connections"][current_room][seperated[1]].replace("_", " ")}")
    current_room=game_map_dict["game_map"]["room_connections"][current_room][seperated[1]]
    if current_room==game_map_dict["game_map"]["room_properties"]["end_room"]:
        game_won()
        exit=True
    else:
        exit=False
        save_file_dict["save_file"]["player"]["current_room"]=current_room
        update_save_file(save_file_dict,save_file_num)
    return(exit)

def drop(seperated,exit,save_file_num):
    save_file_dict=read_save_file(save_file_num)
    if save_file_dict["save_file"]["player"]["inventory"]!=None: #Checking that the player has items in their inventory
        item_to_drop=seperated[1]
        if item_to_drop in save_file_dict["save_file"]["player"]["inventory"] and item_to_drop!="": #Checks if the given item to drop is in the players inventory
            remove_item(item_to_drop,save_file_num)#Removes the earliest of that item in the list from the players inventory
            save_file_dict=read_save_file(save_file_num)
            current_room=save_file_dict["save_file"]["player"]["current_room"]
            save_file_dict["save_file"]["game_map"][current_room]["room_inventory"].insert(0,item_to_drop) #Add the dropped item to the dropped items file for the current room the player is in
            update_save_file(save_file_dict,save_file_num)
            print(f"{item_to_drop.replace("_", " ").capitalize()} dropped in room: {current_room.replace("_", " ")}...")
        else:
            print("You do not have this item in your inventory")
            print()
    else:
        print("Your inventory is empty")
    return(exit)

def view_dropped_items(save_file_num):
    save_file_dict=read_save_file(save_file_num)
    current_room=save_file_dict["save_file"]["player"]["current_room"]
    if save_file_dict["save_file"]["game_map"][current_room]["room_inventory"]==None:
        print("This room has not dropped items...")
        print()
    else:
        for item in save_file_dict["save_file"]["game_map"][current_room]["room_inventory"]:
            print(item.replace("_", " ").capitalize())
        print()

def pickup(seperated,exit,save_file_num):
    save_file_dict=read_save_file(save_file_num)
    current_room=save_file_dict["save_file"]["player"]["current_room"]
    if save_file_dict["save_file"]["game_map"][current_room]["room_inventory"]!=None: #Checking that the current room has any items dropped in it
        item_to_pickup=seperated[1]
        if item_to_pickup in save_file_dict["save_file"]["game_map"][current_room]["room_inventory"] and item_to_pickup!="": #Checking if the given item to pickup is dropped in the current room
            if add_item(item_to_pickup,save_file_num):
                save_file_dict=read_save_file(save_file_num)
                save_file_dict["save_file"]["game_map"][current_room]["room_inventory"].remove(item_to_pickup) #Removing the item from the items dropped in the room
                update_save_file(save_file_dict,save_file_num)
                print(f"{item_to_pickup.replace("_", " ")} picked up and added to inventory...")
        else:
            print("Item is not dropped in this room")
            print()
    return(exit)

def help(seperated,exit,save_file_num):
    game_map_dict=read_game_map()
    print(f"The aim is to reach the end room to win which is - {game_map_dict["game_map"]["room_properties"]["end_room"]}")
    print()
    print("Go 'cardinal direction'")
    print("This is how you move between rooms")
    print()
    print("Drop 'item name'")
    print("Drops the specified item from your inventory in the room you are currently in")
    print()
    print("Pickup 'item name'")
    print("Picks up the specified item from the room into your inventory")
    print()
    print("'NPC name'")
    print("Interacts with the npc specified")
    print("Talk")
    print("The NPC will tell you something potentially interesting")
    print("Trade")
    print("Allows you to trade items for coins or coins for items with the NPC")
    print("Fight")
    print()
    print("Attack")
    print("Does damage to your opponent but you will also recieve damage")
    print("Block")
    print("Blocks a portion of the damage the opponent does to you")
    print("Lets you run away from the battle")
    print("Change")
    print("To change your currently equipped weapon")
    print()
    print("Starts a fight which you may win or lose")
    print("If you win the NPCs inventory will be dropped in the room and it may unlock certain doors")
    print("If you lose you will die and the game will be over")
    print()
    print("View Stats")
    print("Shows you the stats of each item in your inventory")
    print()
    print("Help")
    print("Displays how each command works")
    print()
    print("Quit")
    print("Exits the game")
    print()
    print("Commands are NOT case sensitive")
    print()
    return(exit)

def action(seperated,exit,save_file_num):
    function_name=seperated[0] #String of function name
    function=globals()[function_name] #Globals returns dictionary of global variables including functions
    exit=function(seperated,exit,save_file_num)
    return(exit)

def room_decision(exit,choice,verb_commands,noun_commands,save_file_num):
    valid,seperated=parse_validate_input(verb_commands,noun_commands,choice,save_file_num)
    if valid:
        exit=action(seperated,exit,save_file_num)
    else:
        print("Invalid command try again")
        print()
    return(exit)

def start_menu(): #Sets what room the player first starts off in when opening the game
    game_map_dict=read_game_map()
    print("1 - Start Game")
    print("2 - Load Game")
    print("3 - Quit")
    start_choice="0"
    while ord(start_choice)<49 or ord(start_choice)>51: #Keeps asking the user for an input until it is valid. The Ord value gets the ascii value. 49 in ascii is "1" and 50 in ascii is "2".
        start_choice=input()
        if start_choice=="1":
            save_file_num=saved_choice("overwrite")
            save_file_dict=read_save_file(save_file_num)
            print()
            print(game_map_dict["game_map"]["story"]["intro_text"])
        elif start_choice=="2":
            save_file_num=saved_choice("load")
        elif start_choice=="3":
            print("Exitting...")
            print("Exitted")
            return(True,"")
        else:
            start_choice="0"
            print("Please enter valid option")
    return(False,save_file_num)

def main():
    verb_commands,noun_commands,exit,save_file_num=__init__()
    while exit!=True:
        player_options(save_file_num)
        choice=input().lower()
        print()
        exit=room_decision(exit,choice,verb_commands,noun_commands,save_file_num)

main()