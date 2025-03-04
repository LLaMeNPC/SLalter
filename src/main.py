import os
import datetime
from rewriter import Rewriter

log_file_path = "logs/{}.txt"

models = [
    "smollm2:135m",
    "smollm2:360m",
    "smollm2:1.7b"
]

modes = [
    "Input rewrite",
    "Batch rewrite"
]

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def choice(ls):
    for i, le in enumerate(ls):
        print(f"  {i}) {le}")
    return input("Please select an option: ")

def get_element_from_choice(choice, ls):
    for i, le in enumerate(ls):
        if choice == str(i) or choice == le:
            return le
        elif i == len(ls) - 1:
            cls()
            print(f"Option \"{choice}\" not recognized")
            return None

def generate(sentence, rewriter):
    print("Generating alteration...")
    output = rewriter.rewrite(sentence)
    print(f"\n{output}\n")
    return output

def log(command, output=None):
    date = datetime.datetime.now().date()
    time = datetime.datetime.now().time().strftime('%H:%M:%S')

    current_log_file_path = log_file_path.format(date)
    with open(current_log_file_path, 'a') as file:
        file.write(f"{time} {command}\n\n")
        if output is not None:
            file.write(f"\t{output}\n\n")

selected_model = None
selected_mode = None
_user_input = ""

cls()
while True:
    if selected_model == None:
        print("Which model would you like to use?")
        user_input = choice(models)
        selected_model = get_element_from_choice(user_input, models)
    elif selected_mode == None:
        cls()
        print(f"Model {selected_model} selected, what would you like to do with it?")
        user_input = choice(modes)
        selected_mode = get_element_from_choice(user_input, modes)
        rewriter = Rewriter(selected_model)
    elif selected_mode == modes[0]:
        log(f"Model {selected_model} selected with mode {selected_mode}.")
        cls()
        while True:
            if _user_input == "" or _user_input == "new":
                user_input = input(f"Please input sentence to be rewritten by {selected_model}: ")
                previous_output = generate(user_input, rewriter)
                log(f"Input: {user_input}", previous_output)
            elif _user_input == "again":
                previous_output = generate(user_input, rewriter)
                log("Again", previous_output)
            elif _user_input == "continue":
                previous_output = generate(previous_output, rewriter)
                log("Continue", previous_output)
            else:
                print(f"\"{_user_input}\" not recognized")
            _user_input = input("Input \"new\" to write a new sentence, \"again\" to regenerate from the same sentence, or \"continue\" to regenerate from the previous output: ")
