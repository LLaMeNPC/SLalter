import os, json, datetime
from rewriter import Rewriter
from generator import Generator, Mode
from log import log, log_program_start
from console_utils import print_progress_bar

models = [
    "smollm2:135m",
    "smollm2:360m",
    "smollm2:1.7b",
    "smollm2:1.7b-instruct-q5_K_M",
    "deepseek-r1:1.5b",
    "deepseek-r1:7b",
    "llama3.2:1b",
    "llama3.2",
    "gemma3:1b",
    "nemotron-mini:4b-instruct-fp16",
    "gemma3:27b-it-q8_0"
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

selected_model = None
selected_mode = None
_user_input = ""

log_program_start()

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
        generator = Generator(selected_model)
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
            batches.remove("old_format")
            batch_name = get_element_from_choice(choice(batches), batches)
            if batch_name != None:
                cls()
                num_alterations = int(input("How many alterations would you like to generate per sentence? "))
                
                cls()
                print("Please select a generation type")
                generation_types = ["auto", "prompt", "rewrite"]
                user_input = choice(generation_types)
                generation_type = get_element_from_choice(user_input, generation_types)

                mode = Mode.auto

                if generation_type == "auto":
                    mode = Mode.auto
                elif generation_type == "prompt":
                    mode = Mode.prompt
                elif generation_type == "rewrite":
                    mode = Mode.rewrite

                generator.batch_generate(batch_name, num_alterations, selected_model, generation_type, mode)
                """
                with open(f"batches/{batch_name}") as batch_data:
                    batch_json = json.load(batch_data)
                    date_and_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    output_filename = f"{batch_name}-alteration-{date_and_time}"
                    output = {"config": rewriter.config, "output": {}}
                    print("Rewriting sentences...")
                    progress = 0.0
                    print_progress_bar(progress)
                    for sentence in batch_json:
                        title = sentence
                        output["output"][title] = {}
                        prompt = rewriter.config["rewrite_prompt"].format(sentence = sentence)
                        output["output"][title]["prompt"] = prompt
                        output["output"][title]["generations"] = []
                        for _ in range(num_alterations):
                            output["output"][title]["generations"].append(rewriter.rewrite(sentence))
                            progress += 1.0 / (len(batch_json) * num_alterations)
                            print_progress_bar(progress)
                        with open(f"output/{output_filename}.json", "w") as f:
                            f.write(json.dumps(output))
                    print(f"Done! Wrote output to output/{output_filename}.json")
                """

            else:
                print("Batch not recognized")


