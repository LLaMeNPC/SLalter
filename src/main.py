import os, json, datetime, sys, math
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


def delete_last_line():
    "Deletes the last line in the STDOUT"
    # cursor up one line
    sys.stdout.write('\x1b[1A')
    # delete last line
    sys.stdout.write('\x1b[2K')

def print_progress(progress : float):
    #    if progress < 0 or progress > 1:
    #    raise Exception("Invalid progress given")
    progress_string = "█" * math.floor(progress * 50) + "-" * math.ceil((1-progress) * 50) + f"| {progress * 100:.2f}%"
    print(progress_string)

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
        log(f"Model {selected_model} selected with mode {selected_mode}. Config:", rewriter.config)
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
    elif selected_mode == modes[1]:
        cls()
        while True:
            print("Which batch would you like to generate alterations on?")
            batches = os.listdir("batches")
            batch_name = get_element_from_choice(choice(batches), batches)
            if batch_name != None:
                cls()
                num_alterations = int(input("How many alterations would you like to generate per sentence? "))
                with open(f"batches/{batch_name}") as batch_data:
                    batch_json = json.load(batch_data)
                    date_and_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    output_filename = f"{batch_name}-alteration-{date_and_time}"
                    output = {}
                    print("Rewriting sentences...")
                    progress = 0.0
                    print_progress(progress)
                    for sentence in batch_json:
                        output[sentence] = []
                        for _ in range(num_alterations):
                            output[sentence].append(rewriter.rewrite(sentence))
                            progress += 1.0 / (len(batch_json) * num_alterations)
                            delete_last_line()
                            print_progress(progress)
                        with open(f"output/{output_filename}.json", "w") as f:
                            f.write(json.dumps(output))
                    print(f"Done! Wrote output to output/{output_filename}.json")
            else:
                print("Batch not recognized")


