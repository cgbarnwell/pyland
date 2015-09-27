#commence save-data set-up
world_name = "world1"
level_name = "level4"
map_name = "main"

engine.update_world_text("1")
engine.update_level_text("4")

player_data.load(engine.get_player_name())
player_data.set_map(world_name, level_name = level_name, map_name = map_name)
#end save-data set_up

import random

reached_arith = False

#setting player's starting position
if player_data.previous_exit_is(world_name, level_name = level_name, map_name = map_name, info = "reached_arith_help"):
    x, y = challenge_arith.get_position()
    player_one.move_to((x,y), callback = lambda: myla.move_to((x-1, y), callback = reached_arith_fun))
else:
    pass
    #do nothing as we have not got the checkpoint

def go_to_world(player_object):
    player_data.complete_level_and_save()
    player_data.save_and_exit("/world1")

exit_level_start.player_walked_on = lambda player_object: player_data.save_and_exit("/world1")

exit_level_end.player_walked_on = go_to_world

player_one.focus()
myla.follow(player_one)

engine.play_music("world_1_jungle")
engine.set_ui_colours((200,255,200),(215,255,215)) #TODO: save these colours in the config.
engine.set_py_tabs(2)

def no_thanks(player_object):
    engine.run_callback_list_sequence([
        lambda callback: engine.show_dialogue("Myla: All right then!", callback = callback),
        lambda callback: player_object.set_busy(False)
    ])
17
def for_help(player_object):
    engine.run_callback_list_sequence([
        lambda callback: engine.clear_scripter(callback = callback),
        lambda callback: engine.insert_to_scripter("#Code to move 25 times to the east using a loop", callback = callback),
        lambda callback: engine.insert_to_scripter("\nfor i in range(25):", callback = callback),
        lambda callback: engine.insert_to_scripter("\n\tmove_east()", callback = callback),
        lambda callback: player_object.set_busy(False)
    ])

def help_with_for(player_object):
    engine.run_callback_list_sequence([
        lambda callback: player_object.set_busy(True, callback = callback),
        lambda callback: engine.show_dialogue("There are three guardians here, solve their challenges to prove your worth...", callback = callback),
        lambda callback: engine.show_dialogue("They will pose riddles a plenty, can you achieve this?", callback = callback),
        lambda callback: myla.start_animating(speed = 0.1, loop = False, forward = False, callback = callback)
    ], callback = lambda: engine.show_dialogue_with_options(
        "Myla: Do you want me to help you with that?",
        {
            "Yes": lambda: for_help(player_object),
            "No": lambda: no_thanks(player_object)
        }))

def reached_arith_fun():
    player_data.save_checkpoint("reached_arith_help")
    global reached_arith
    if not reached_arith:
        reached_arith = True
        engine.run_callback_list_sequence([
            lambda callback: player_one.set_busy(True, callback = callback),
            lambda callback: engine.show_dialogue("Myla: Looks like we need to get past these guardians. I've heard of them before, Anindya, Maenan and Alexander.", callback = callback),
            lambda callback: engine.show_dialogue("They have a reputation for testing adventurers on their way to cross the jungle.", callback = callback),
            lambda callback: engine.show_dialogue("But they actually just want their chores done for them.", callback = callback),
            lambda callback : player_one.set_busy(False, callback = callback)
        ])

challenge_arith.player_walked_on = lambda player_object: reached_arith_fun()

def myla_speak(player_object):
    engine.run_callback_list_sequence([
        lambda callback: player_one.set_busy(True, callback = callback),
        lambda callback: engine.show_dialogue("Read the sign if you get stuck.", callback = callback),
        lambda callback: player_one.set_busy(False, callback = callback)]
    )

myla.player_action = myla_speak

def arithmetic_help(player_object):
    engine.run_callback_list_sequence([
        lambda callback: engine.clear_scripter(callback = callback),
        lambda callback: engine.insert_to_scripter("#The symbol * is used to multiply numbers\n", callback = callback),
        lambda callback: engine.insert_to_scripter("#The symbol + is used to add numbers\n", callback = callback),
        lambda callback: engine.insert_to_scripter("#The symbol - is used to subtract one number from another\n", callback = callback),
        lambda callback: engine.insert_to_scripter("#The symbol / is used to divide one number by another\n", callback = callback),
        lambda callback: engine.insert_to_scripter("#Try and help the guard solve the problem by printing out an answer for him using \nprint()\n", callback = callback),
        lambda callback: player_one.set_busy(False, callback = callback),
        lambda callback: player_object.set_busy(False)
    ])

def help_with_arithmetic(player_object):
    engine.run_callback_list_sequence([
        lambda callback: player_object.set_busy(True, callback = callback),
        lambda callback: engine.show_dialogue("There are three guardians here, solve their challenges to prove your worth...", callback = callback),
        lambda callback: engine.show_dialogue("They will pose riddles a plenty, can you achieve this?", callback = callback),
        lambda callback: myla.start_animating(speed = 0.1, loop = False, forward = False, callback = callback)
    ], callback = lambda: engine.show_dialogue_with_options(
        "Myla: Do you want me to help you with that?",
        {
            "Yes": lambda: arithmetic_help(player_object),
            "No": lambda: no_thanks(player_object)
        }))

###
### Random helper dude
###

sign_one.player_action = help_with_for
sign_two.player_action = help_with_arithmetic

def helper_one_action(player_object):
    if(player_object.is_facing_south()):
        helper_one.face_north()
    elif(player_object.is_facing_east()):
        helper_one.face_west()
    elif(player_object.is_facing_north()):
        helper_one.face_south()
    else:
        helper_one.face_east()
    engine.run_callback_list_sequence([
        lambda callback: player_one.set_busy(True, callback = callback),
        lambda callback: engine.show_dialogue("Ying: Don't look at me, I'm new and still an apprentice guardian!", callback = callback),
        lambda callback: engine.show_dialogue("These three have told me I need to learn how to use sphinx for them because it confuses them...", callback = callback),
        lambda callback: engine.show_dialogue("... but I thought they were the ones that were meant to be good at riddles!", callback = callback),
        lambda callback: player_one.set_busy(False, callback = callback),
    ])

helper_one.player_action = helper_one_action

def no_help(name):
    engine.run_callback_list_sequence([
        lambda callback: player_one.set_busy(True, callback = callback),
        lambda callback: engine.show_dialogue(name + ": That's fair enough, mate.", callback = callback),
        lambda callback: player_one.set_busy(False, callback = callback)
    ])

def cancel_script():
    engine.run_callback_list_sequence([
        lambda callback: player_one.set_busy(False, callback = callback)
    ])

def puzzle_wrong(name):
    engine.run_callback_list_sequence([
        lambda callback: player_one.set_busy(True, callback = callback),
        lambda callback: engine.show_dialogue(name + ": What's that? That doesn't seem to be right!", callback = callback),
        lambda callback: player_one.set_busy(False, callback = callback),
    ])

def solved_puzzle(name, callback = lambda: None):
    engine.run_callback_list_sequence([
        lambda callback: player_one.set_busy(True, callback = callback),
        lambda callback: engine.show_dialogue(name + ": Thanks chum!", callback = callback),
        lambda callback: player_one.set_busy(False, callback = callback),
    ], callback = callback)

def being_smart():
    engine.run_callback_list_sequence([
        lambda callback: player_one.set_busy(True, callback = callback),
        lambda callback: engine.show_dialogue("Myla: Oooh that's smart! Using the scripter to move them instead of helping them. Good idea!", callback = callback),
        lambda callback: player_one.set_busy(False, callback = callback),
    ])

"""
*** *** *** Start security one
"""
puzzle_one_solved = False
security_one.face_south()
security_one_org_posn = security_one.get_position()

puzzle_one_a = random.randint(11,25)
puzzle_one_b = random.randint(190, 430)

def security_one_action(player_object):
    global puzzle_one_solved
    security_one.turn_to_face(player_object)
    if(not puzzle_one_solved):
        engine.run_callback_list_sequence([
            lambda callback: player_one.set_busy(True, callback = callback),
            lambda callback: engine.show_dialogue("Anindya: I am Anindya! I will let you pass if you help me.", callback = callback),
            lambda callback: engine.show_dialogue("I need to know the total cost of building my snake cages in pounds.", callback = callback)
        ],
        callback = lambda: engine.show_dialogue_with_options(
            "Can you help me?",
            options = {
                "Yes": lambda: security_one_problem(),
                "No" : lambda: no_help("Anindya")
            })
        )

    else:
        engine.run_callback_list_sequence([
                lambda callback: solved_puzzle("Anindya", callback = callback),
            ],
            callback = lambda: engine.show_external_script(
                confirm_callback = lambda: security_one.run_script(script_to_run = 10),
                cancel_callback = cancel_script(),
                external_dialogue = "I love running your scripts, give me another!",
                script_init = lambda: engine.insert_to_scripter("")
            )
        )


def security_one_problem():
    engine.run_callback_list_sequence([
        lambda callback: player_one.set_busy(True, callback = callback),
        lambda callback: engine.show_dialogue("Thank you! Help me run a script!",  callback = callback),
        lambda callback: engine.show_external_script(
            confirm_callback = lambda: engine.run_callback_list_sequence(try_security_one),
            cancel_callback = lambda: cancel_script(),
            external_dialogue = "I need to know the cost of building " + str(puzzle_one_a) + " cages, each costing £" + str(puzzle_one_b) + ".",
            script_init = lambda: engine.insert_to_scripter("print(1 + 2)")
        )
    ])

try_security_one = [
    lambda callback: engine.show_dialogue("Thank you! I'll try running it now.", callback = callback),
    lambda callback: player_one.set_busy(False, callback = callback),
    lambda callback: security_one.run_script(script_to_run = 10, callback = lambda: check_security_one())
]

def check_security_one():
    global puzzle_one_solved
    global security_one_org_posn

    #we are using 1 and not 0 because the last thing to be printed is something like "security_one's script has ended"
    if(engine.get_terminal_text(1) == str(puzzle_one_a * puzzle_one_b)):
        puzzle_one_solved = True
        puzzle_one_right()
    else:
        puzzle_wrong("Anindya")

    if(security_one.get_position() != security_one_org_posn):
        security_one_org_posn = security_one.get_position()
        being_smart()

def puzzle_one_right():
    engine.run_callback_list_sequence([
        lambda callback: player_one.set_busy(True, callback = callback),
        lambda callback: engine.show_dialogue("What's that? Oh Thank You! Let me go buy the cages now!", callback = callback),
        lambda callback: engine.show_dialogue("To thank you, I will let you pass!", callback = callback),
        lambda callback: security_one.move_north(callback = callback),
        lambda callback: security_one.move_east(callback = callback),
        lambda callback: player_one.set_busy(False, callback = callback),
    ])

security_one.player_action = security_one_action


"""
*** *** *** Start security two
"""
puzzle_two_solved = False
security_two.face_north()
security_two_org_posn = security_two.get_position()

puzzle_two_a = random.randint(1,59)
puzzle_two_b = random.randint(2,10)

def security_two_action(player_object):
    global puzzle_two_solved
    security_two.turn_to_face(player_object)
    if(not puzzle_two_solved):
        engine.run_callback_list_sequence([
            lambda callback: player_one.set_busy(True, callback = callback),
            lambda callback: engine.show_dialogue("Maenan: I am Maenan! I will let you pass if you help me.", callback = callback),
            lambda callback: engine.show_dialogue("I need to know how many minutes I have left before meeting my bosses", callback = callback)
        ],
        callback = lambda: engine.show_dialogue_with_options(
            "Maenan: Can you help me?",
            options = {
                "Yes": lambda: security_two_problem(),
                "No" : lambda: no_help("Maenan")
            })
        )

    else:
        engine.run_callback_list_sequence([
            lambda callback: solved_puzzle("Maenan", callback = callback)
        ], callback = lambda: engine.show_external_script(
                confirm_callback = lambda: security_two.run_script(script_to_run = 10),
                cancel_callback = cancel_script(),
                external_dialogue = "I'm hungry for more scripts!",
                script_init = lambda: engine.insert_to_scripter("")
            )
        )

def security_two_problem():
    engine.run_callback_list_sequence([
        lambda callback: player_one.set_busy(True, callback = callback),
        lambda callback: engine.show_dialogue("Thank you! Help me run a script!",  callback = callback),
        lambda callback: engine.show_external_script(
            confirm_callback = lambda: engine.run_callback_list_sequence(try_security_two),
            cancel_callback = lambda: cancel_script(),
            external_dialogue = str(puzzle_two_a) + " minutes ago my bosses said come in " + str(puzzle_two_b) + " hours. How minutes do I have left until I meet them?",
            script_init = lambda: engine.insert_to_scripter("print(1 + 2)")
        )
    ])

try_security_two = [
    lambda callback: engine.show_dialogue("Thank you! I'll try running it now.", callback = callback),
    lambda callback: player_one.set_busy(False, callback = callback),
    lambda callback: security_two.run_script(script_to_run = 10, callback = lambda: check_security_two())
]

def check_security_two():
    global puzzle_two_solved
    global security_two_org_posn

    #we are using 1 and not 0 because the last thing to be printed is something like "security_one's script has ended"
    if(engine.get_terminal_text(1) == str(puzzle_two_b * 60 - puzzle_two_a)):
        puzzle_two_solved = True
        puzzle_two_right()
    else:
        puzzle_wrong("Maenan")

    if(security_two.get_position() != security_two_org_posn):
        security_two_org_posn = security_two.get_position()
        being_smart()

def puzzle_two_right():
    engine.run_callback_list_sequence([
        lambda callback: player_one.set_busy(True, callback = callback),
        lambda callback: engine.show_dialogue("What's that? Oh Thank You! Let me wait till then", callback = callback),
        lambda callback: engine.show_dialogue("To thank you, I will let you pass!", callback = callback),
        lambda callback: security_two.move_south(callback = callback),
        lambda callback: security_two.move_west(callback = callback),
        lambda callback: player_one.set_busy(False, callback = callback),
    ])

security_two.player_action = security_two_action

"""
*** *** *** Start security three
"""
puzzle_three_solved = False
security_three.face_west()

def security_three_action(player_object):
    global puzzle_three_solved

    if(not puzzle_three_solved):
        engine.run_callback_list_sequence([
            lambda callback: player_one.set_busy(True, callback = callback),
            lambda callback: engine.show_dialogue("Alexander: I am Alexander! I will let you pass if you help me.", callback = callback),
            lambda callback: engine.show_dialogue("I need to find the 2 keys that I lost around here", callback = callback),
            lambda callback: engine.show_dialogue("Can you find them and give them to me?", callback = callback),
            lambda callback: engine.show_dialogue("The other two guardians always hide them from me.", callback = callback),
            lambda callback: check_security_three(player_object)
        ])
    else:
        solved_puzzle("Alexander")


def check_security_three(player_object):
    if player_object.get_keys() >= 2:
        puzzle_three_solved = True
        player_object.add_keys(-2)
        engine.run_callback_list_sequence([
            lambda callback: player_one.set_busy(True, callback = callback),
            lambda callback: engine.show_dialogue("Alexander: What's that? You have two keys? Oh Thank You! ", callback = callback),
            lambda callback: engine.show_dialogue("To thank you, I will let you pass!", callback = callback),
            lambda callback: engine.show_dialogue("I bet the other two were hiding them...", callback = callback),
            lambda callback: security_three.move_east(callback = callback),
            lambda callback: security_three.move_north(callback = callback),
            lambda callback: player_one.set_busy(False, callback = callback)
        ])
    else:
        engine.run_callback_list_sequence([
            lambda callback: player_one.set_busy(True, callback = callback),
            lambda callback: engine.show_dialogue("Alexander: You have don't have 2 keys? Oh never mind.", callback = callback),
            lambda callback: player_one.set_busy(False, callback = callback)
        ])

security_three.player_action = security_three_action


