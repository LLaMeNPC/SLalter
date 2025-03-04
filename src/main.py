import os
from rewriter import Rewriter



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
    print(f"\n{rewriter.rewrite(sentence)}\n")


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
        cls()
        while True:
            if _user_input == "" or _user_input == "new":
                user_input = input(f"Please input sentence to be rewritten by {selected_model}: ")
                generate(user_input, rewriter)
            elif _user_input == "again":
                generate(user_input, rewriter)
            else:
                print(f"\"{_user_input}\" not recognized")
            _user_input = input("Input \"new\" to write a new sentence, or \"again\" to regenerate from the same sentence: ")
