from datetime import datetime
import ollama, json
from config_getter import get_config
from console_utils import print_progress_bar
from rewriter import Rewriter 

"""
BATCH FILE STRUCTURE

{
    TITLE: {
        "prompt": PROMPT,
        "original": ORIGINAL_SENTENCE,
        "context": CONTEXT,
        "description": DESCRIPTION
    },
    ...
}

LEGEND:

- TITLE: A title representing the sentence generation. Will be used in graph titles.
- PROMPT: Prompt to be rewritten. If not present, prompt based generation will be unavailable. 
- ORIGINAL_SENTENCE: Sentence to be rewritten. If not present, sentence rewriting will not be available.
- CONTEXT (optional): Context given to the LM. Is added to the prompt during generation.
- DESCRIPTION (optional): Description of the given generation dict.

"""

class Mode:
    auto = 1
    prompt = 2
    rewrite = 3

class Generator:

    def __init__(self, model_string) -> None:
        self.config = get_config()
        self.client = ollama.Client()
        self.client.create(
            model='Generator',
            from_=model_string,
            system=self.config["prompt_system_prompt"]
        )        
        self.client.create(
            model='Rewriter',
            from_=model_string,
            system=self.config["rewrite_system_prompt"]
        )

        self.rewriter = Rewriter(model_string)

    def get_context_addition(self, context):
        if context != "":
            return f"\n\n{self.config["context_addition"].format(context = context)}"
        return ""

    def get_rewrite_prompt(self, sentence, context = ""):
        return f"{self.config["rewrite_prompt"].format(sentence = sentence)}{self.get_context_addition(context)}"

    def get_prompt_prompt(self, prompt, context = ""):
        return f"{self.config["prompt_prompt"].format(prompt = prompt)}{self.get_context_addition(context)}"
    

    def _generate(self, prompt, _model):
        return ollama.chat(
            model=_model,
            options={"temperature": self.config["temperature"]},
            messages=[{"role": self.config["role"], "content": prompt}]
        )["message"]["content"]

    def prompt_generate(self, generation_dict):
        prompt = self.get_prompt_prompt(
            generation_dict["prompt"], 
            generation_dict["context"]
        )
        return (prompt, self._generate(prompt, "Generator"))

    def rewrite_generate(self, generation_dict):
        prompt = self.get_rewrite_prompt(
            generation_dict["original"],
            generation_dict["context"]
        )
        return (
            prompt,
            self._generate(prompt,"Rewriter")
        )

    def generate(self, generation_dict, mode = Mode.auto):
        match mode:
            case Mode.auto:
                if "prompt" in generation_dict.keys():
                    return self.prompt_generate(generation_dict)
                return self.rewrite_generate(generation_dict)
            case Mode.prompt:
                return self.prompt_generate(generation_dict) 
            case Mode.rewrite:
                return self.rewrite_generate(generation_dict)
        return (None,None)

    def batch_generate(self, batch_name, alteration_count, model_name, mode_name, mode = Mode.auto):
        with open(f"batches/{batch_name}") as batch_data:
            batch_json = json.load(batch_data)
            date_and_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            
            output_filename = f"{batch_name.removesuffix(".json")}({model_name})({mode_name}-{alteration_count})-{date_and_time}"
            output_filename = output_filename.replace(":", "_")
            info = {
                "date_and_time": date_and_time,
                "batch_name": batch_name,
                "model_name": model_name,
                "alteration_count": alteration_count,
                "mode": mode_name,
            }
            file_path = f"output/{output_filename}.json"
            output = {"config": self.config, "info": info, "self_file_name": output_filename, "output": {}}
            print("Rewriting sentences...")
            progress = 0.0
            print_progress_bar(progress)

            for title, generation_dict in batch_json.items():
                if "context" not in generation_dict:
                    generation_dict["context"] = ""
                output["output"][title] = {}
                out_dict = output["output"][title]

                out_dict["prompt"] = ""
                out_dict["generations"] = []
                generations = out_dict["generations"]
                for _ in range(alteration_count):
                    prompt, generation = self.generate(generation_dict, mode)
                    generations.append(generation)
                    out_dict["prompt"] = prompt
                    progress += 1.0 / (len(batch_json) * alteration_count)
                    print_progress_bar(progress)
                with open(file_path, "w") as f:
                    f.write(json.dumps(output))
            print(f"Done! Wrote output to {file_path}")
            
