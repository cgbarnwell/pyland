import sys
import json

sys.path.insert(1, engine.get_config()['files']['script_running_location'])
from script_state_container import ScriptStateContainer

camera.focus()
engine.hide_bag()
config = engine.get_config()

c1 = (210, 210, 210)
c2 = (190, 190, 190)
engine.set_ui_colours(c1, c2)
engine.play_music("calm")
engine.show_py_scripter()

player_name = "???"

name_parsed = False

engine.clear_scripter()
engine.set_py_tabs(1)
engine.disable_py_scripter()

def name_parser(name, callback):
    global name_parsed
    global player_name
    name = str(name)
    engine.print_terminal(name)
    if not name_parsed:
        name_parsed = True
        player_name = name
        if(engine.save_exists(name)):
            engine.print_terminal("A save with the name: " + name + " already exists!") #TODO: handle this a lot more cleverly!
        engine.set_player_name(name)
        engine.disable_py_scripter()
        engine.flush_input_callback_list(engine.INPUT_RUN)
        engine.flush_input_callback_list(engine.INPUT_HALT)
        callback()



#stc.run_script(script_api, engine, callback = handle_run)


def handle_run():
    global name_parsed
    engine.close_external_script_help()
    if not name_parsed:
        engine.run_callback_list_sequence(name_wrong_sequence)


def get_player_name(callback):
    global name_parsed
    name_parsed = False
    engine.clear_scripter()
    engine.insert_to_scripter("print(\"" + engine.get_dialogue(level_name, "print_name_string") + "\")")
    engine.enable_py_scripter()
    script_api = {
        "print" : lambda text: name_parser(text, callback)
    }

    stc = ScriptStateContainer()

    stc.set_script_name("Monty")
    engine.register_input_callback(engine.INPUT_RUN, lambda: stc.run_script(script_api, engine, callback = lambda: handle_run()))
    engine.register_input_callback(engine.INPUT_HALT, stc.halt_script)


level_name = "/world1/intro"
introduction_sequence = [
    lambda callback: engine.show_dialogue(engine.get_dialogue(level_name, "monty_coming_now"), callback = callback),
    lambda callback: camera.move_by((0, -11), 2.2, callback = callback),
    lambda callback: camera.wait(0.2, callback = callback),
    lambda callback: engine.show_dialogue(engine.get_dialogue(level_name, "im_monty_the_snake"), callback = callback),
    lambda callback: engine.show_dialogue(engine.get_dialogue(level_name, "monty_doesnt_know_name"), callback = callback),
    lambda callback: engine.show_dialogue(engine.get_dialogue(level_name, "big_white_box"), callback = callback),
    lambda callback: engine.show_external_script_help(engine.get_dialogue(level_name, "scripting"), callback = callback),
    lambda callback: get_player_name(callback = callback),
]

def confirm_name():
    engine.show_dialogue_with_options(
        engine.get_dialogue(level_name, "confirm_player_name", {"player_name": player_name}),
        {
            engine.get_dialogue("shared", "yes"): lambda: engine.run_callback_list_sequence(name_confirmed_sequence, start_game), #change the level once the intro has finished
            engine.get_dialogue("shared", "no") : lambda: engine.run_callback_list_sequence(name_wrong_sequence, confirm_name)
        }
    )

engine.run_callback_list_sequence(introduction_sequence, callback = confirm_name)

name_wrong_sequence = [
    lambda callback: engine.show_dialogue(engine.get_dialogue(level_name, "player_name_wrong"), callback = callback),
    lambda callback: engine.show_external_script_help(engine.get_dialogue(level_name, "scripting"), callback = callback),
    lambda callback: get_player_name(callback = callback)
]

name_confirmed_sequence = [
    lambda callback: engine.show_dialogue(engine.get_dialogue(level_name, "wrote_first_program", {"player_name": player_name}), callback = callback),
    lambda callback: engine.show_dialogue(engine.get_dialogue(level_name, "console_output"), callback = callback),
    lambda callback: engine.show_dialogue("Now we can use print function to select who you will be in Pyland (TODO)", callback = callback),
    lambda callback: engine.show_dialogue(engine.get_dialogue(level_name, "go_enjoy_pyland", {"player_name": player_name}), callback = callback),
]

def start_game():
    """Save the player's game and start the game!"""
    player_data.create(engine.get_player_name())
    engine.change_map("/world1/level1/player_house")

