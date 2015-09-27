from random import randint

#commence save-data set-up
world_name = "world1"
level_name = "level5"
map_name = "main"

engine.update_world_text("1")
engine.update_level_text("5")

player_data.load(engine.get_player_name())
player_data.set_map(world_name, level_name = level_name, map_name = map_name) #change the map and save that the map has changed
#end save-data set-up

engine.enable_py_scripter()
player_one.focus()
engine.play_music("world_1_jungle")

def check_croc1(player_object):
    player_data.save_checkpoint("croc1")

def check_croc2(player_object):
    player_data.save_checkpoint("croc2")

check1.player_walked_on = check_croc1
check2.player_walked_on = check_croc2

start_from_beg = False

if player_data.previous_exit_is(world_name = world_name, level_name = level_name, map_name = map_name, info = "croc1"):
    x,y = check1.get_position()
    player_one.move_to((x,y), callback = lambda: door1.set_solidity(False, callback = lambda: door2.set_solidity(True)))
elif player_data.previous_exit_is(world_name = world_name, level_name = level_name, map_name = map_name, info = "croc2"):
    x,y = check2.get_position()
    player_one.move_to((x,y), callback = lambda: door2.set_solidity(False, callback = lambda: door1.set_solidity(True)))
else:
    start_from_beg = True

if(start_from_beg):
    engine.run_callback_list_sequence([
        lambda callback: player_one.set_busy(True, callback = callback),
        lambda callback: player_one.turn_to_face(myla, callback = callback),
        lambda callback: myla.turn_to_face(player_one, callback = callback),
        lambda callback: engine.show_dialogue("There are scrolls lying all over in this region! They usually contain riddles.", callback = callback),
        lambda callback: engine.clear_scripter(callback = callback),
        lambda callback: engine.insert_to_scripter("print(scan())", callback = callback),
        lambda callback: engine.show_dialogue("Here is a script to read them:", callback = callback),
        lambda callback: engine.show_dialogue("The command scan() extract the messages from the place in front of you.", callback = callback),
        lambda callback: engine.show_dialogue("Print then displays the text returned by scan() to the PyConsole.", callback = callback),
        lambda callback: engine.show_dialogue("Try and read from the scroll, so we can find our way out of here!", callback = callback),
        lambda callback: player_one.set_busy(False, callback = callback),
        lambda callback: myla.follow(player_one, callback = callback)
    ])

def go_next(player_object):
    player_data.save_and_exit("/world1")

end_level.player_walked_on = go_next

def leave_beg(player_object):
    player_data.save_and_exit("/world1")

exit_level_start.player_walked_on = leave_beg

scroll1.set_message("The second boulder from the left is an illusion.")
scroll2.set_message("If the scroll to my left contains an odd number,\nthe middle tree stumps to the north are what you desire.\nElse, the tree stumps to the west are what you seek.")

rand_block = randint(0,999)

scroll3.set_message("Number: " + str(rand_block))

def do_nothing(player_object):
    pass

block1.player_walked_on = do_nothing
block2.player_walked_on = do_nothing

if(rand_block % 2 == 0):
    block1.set_solidity(True)
else:
    block2.set_solidity(True)

### Setting up next chamber
ans = [1, 1, 1, 1]

rand_block = randint(1,16)
magic_message = ""

def add_magic_message():
    global rand_block
    global magic_message
    if(rand_block % 2 == 0):
        magic_message += " odd number of times\n"
        rand_block //= 2
        return 1
    else:
        magic_message += "even number of times\n"
        rand_block //= 2
        return 0

magic_message += "Top-right grass tile: "
ans[0] = add_magic_message()
magic_message += "Bottom-right grass tile: "
ans[1] = add_magic_message()
magic_message += "Bottom-left grass tile: "
ans[2] = add_magic_message()
magic_message += "Top-left grass tile: "
ans[3] = add_magic_message()

###### Top chamber
centre1.player_walked_on = do_nothing

#start from topright and go clockwise
count1 = [0, 0, 0, 0]

door1.player_walked_on = do_nothing
door1.set_solidity(True)

scroll1a.set_message("The man who lives here is a wizard and must stand\ on the central magical leaves to harness his powers.")
scroll1b.set_message("Once the wizard starts using magic, you need\nto step on as many magical leaves as indicated on the next scroll.")
scroll1c.set_message(magic_message)
scroll1d.set_message("The magic the wizard performs lets you walk through the \nnorth-most log of wood on the east wall.")

tiles1 = [topright1, bottomright1, bottomleft1, topleft1]

def check1():
    for i in range(4):
        if(ans[i]%2 != count1[i]%2):
            door1.set_solidity(True)
            return
    door1.set_solidity(False)

def add1(i):
    if pete.get_position() == centre1.get_position():
        count1[i] += 1
        check1()

tiles1[0].player_walked_on = lambda player_object: add1(0)
tiles1[1].player_walked_on = lambda player_object: add1(1)
tiles1[2].player_walked_on = lambda player_object: add1(2)
tiles1[3].player_walked_on = lambda player_object: add1(3)

def pete_speak():
    if(pete.get_position() == centre1.get_position()):
        engine.run_callback_list_sequence([
            lambda callback: player_one.set_busy(True, callback = callback),
            lambda callback: pete.turn_to_face(player_one, callback = callback),
            lambda callback: engine.show_dialogue("I am performing my magic. Please follow the scroll's instructions for harnessing the magic.", callback = callback),
            lambda callback: engine.show_dialogue("You have walked these many times on the magic leaves:", callback = callback),
            lambda callback: engine.show_dialogue("Top-right:"+str(count1[0])+", Bottom-right:"+str(count1[1])+", Bottom-left:"+str(count1[2])+", Top-left:"+str(count1[3]), callback = callback),
            lambda callback: player_one.set_busy(False, callback =callback)
        ])
    else:
        engine.run_callback_list_sequence([
        lambda callback: pete.set_busy(False, callback = callback),
        lambda callback: pete.turn_to_face(player_one, callback = callback),
        lambda callback: engine.show_external_script(
            confirm_callback = lambda: engine.run_callback_list_sequence([
                lambda callback: player_one.set_busy(False, callback = callback),
                lambda callback: pete.run_script(script_to_run = 10)]),
            cancel_callback = lambda: player_one.set_busy(False),
            external_dialogue = "You can edit my script and I will run it!",
            script_init = lambda: engine.insert_to_scripter(""),
            character_object = pete
        )
    ])

pete.player_action = lambda player_object: pete_speak()

###### Right chamber
centre2.player_walked_on = do_nothing

#start from topright and go clockwise
count2 = [0, 0, 0, 0]

door2.player_walked_on = do_nothing
door2.set_solidity(True)

scroll2a.set_message("The lady who lives here is a witch and she must be\non the central magical leaves to harness her powers.")
scroll2b.set_message("Once the witch starts her magic, you need\nto step on as many grass tiles as indicated on the next scroll.")
scroll2c.set_message(magic_message)
scroll2d.set_message("The magic the witch performs allows you to walk through the \nwest-most log of wood on the north wall.")

tiles2 = [topright2, bottomright2, bottomleft2, topleft2]

def check2():
    for i in range(4):
        if(ans[i]%2 != count2[i]%2):
            door2.set_solidity(True)
            return
    door2.set_solidity(False)

def add2(i):
    if maddie.get_position() == centre2.get_position():
        count2[i] += 1
        check2()

tiles2[0].player_walked_on = lambda player_object: add2(0)
tiles2[1].player_walked_on = lambda player_object: add2(1)
tiles2[2].player_walked_on = lambda player_object: add2(2)
tiles2[3].player_walked_on = lambda player_object: add2(3)

def maddie_speak():
    if(maddie.get_position() == centre2.get_position()):
        engine.run_callback_list_sequence([
            lambda callback: player_one.set_busy(True, callback = callback),
            lambda callback: maddie.turn_to_face(player_one, callback = callback),
            lambda callback: engine.show_dialogue("I am performing my magic. Please follow the scroll's instructions for harnessing the magic.", callback = callback),
            lambda callback: engine.show_dialogue("You have walked these many times on the magic leaves:", callback = callback),
            lambda callback: engine.show_dialogue("Top-right:"+str(count2[0])+", Bottom-right:"+str(count2[1])+", Bottom-left:"+str(count2[2])+", Top-left:"+str(count2[3]), callback = callback),
            lambda callback: player_one.set_busy(False, callback =callback)
        ])
    else:
        engine.run_callback_list_sequence([
        lambda callback: maddie.set_busy(False, callback = callback),
        lambda callback: maddie.turn_to_face(player_one, callback = callback),
        lambda callback: engine.show_external_script(
            confirm_callback = lambda: engine.run_callback_list_sequence([
                lambda callback: player_one.set_busy(False, callback = callback),
                lambda callback: maddie.run_script(script_to_run = 10)]),
            cancel_callback = lambda: player_one.set_busy(False),
            external_dialogue = "You can edit my script and I will run it!",
            script_init = lambda: engine.insert_to_scripter(""),
            character_object = maddie
        )
    ])

maddie.player_action = lambda player_object: maddie_speak()

###croc chamber
hor_crocs = [croc1, croc2, croc3]
ver_crocs = [croc4, croc5]

for croc in hor_crocs:
    croc.killable = [player_one,myla]
    croc.move_horizontal()

for croc in ver_crocs:
    croc.killable = [player_one,myla]
    croc.move_vertical()

###final chamber

scroll4.set_message("The boulder will give way when you come close to it,\nbut only if you don't walk on any grass patches.\n In case you do, reset the boulder by standing on the leaves\nin the north part of this chamber.")

def bob_speak():
    engine.run_callback_list_sequence([
        lambda callback: bob.set_busy(False, callback = callback),
        lambda callback: bob.turn_to_face(player_one, callback = callback),
        lambda callback: engine.show_external_script(
            confirm_callback = lambda: engine.run_callback_list_sequence([
                lambda callback: player_one.set_busy(False, callback = callback),
                lambda callback: bob.run_script(script_to_run = 10)]),
            cancel_callback = lambda: player_one.set_busy(False),
            external_dialogue = "You can edit my script and I will run it! I wish I could scan the scroll over here!",
            script_init = lambda: engine.insert_to_scripter(""),
            character_object = bob
            )
    ])

bob.player_action = lambda player_object: bob_speak()

steps = False

def walked_on_switch():
    global steps
    steps = True

switches = [switch1, switch2, switch3, switch4, switch5]

for sw in switches:
    sw.player_walked_on = lambda player_object: walked_on_switch()

def reset_switches():
    global steps
    steps = False

reset.player_walked_on = lambda player_object: reset_switches()

def reached():
    global steps
    if steps:
        pass
    else:
        boulder1.move_west()

reached1.player_walked_on = lambda player_object: reached()


again = [
    lambda callback: engine.show_dialogue("Here you go!", callback = callback),
    lambda callback: engine.clear_scripter(callback = callback),
    lambda callback: engine.insert_to_scripter("print(scan())", callback = callback),
    lambda callback: engine.show_dialogue("Remember to run your script when you're facing a scroll. Talking to it won't help!", callback = callback),
    lambda callback: player_one.set_busy(False, callback = callback)
]

not_again = [
    lambda callback: engine.show_dialogue("Remember to run your script when you're facing a scroll. Talking to it won't help!", callback = callback),
    lambda callback: player_one.set_busy(False, callback = callback)
]

myla_sequence = [
    lambda callback: player_one.set_busy(True, callback = callback),
    lambda callback: myla.turn_to_face(player_one, callback = callback),

    lambda callback: engine.show_dialogue_with_options(
        "Would you like the scan script again?",
        {
            "Yes": lambda: engine.run_callback_list_sequence(again),
            "No" : lambda: engine.run_callback_list_sequence(not_again)
        }
    )

]

myla.player_action = lambda player_object: engine.run_callback_list_sequence(myla_sequence)
