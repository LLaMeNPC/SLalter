# SLalter: Small Language alterations

# Table of contents

* [Setup (linux)](#setup-linux)
  * [Set up a virtual enviorenment for python packages (optional)](#set-up-a-virtual-enviorenment-for-python-packages-optional)
  * [Download requirements](#download-requirements)
  * [Setup automatic venv switching (optional)](#setup-automatic-venv-switching-optional)
* [Run](#run)
  * [Selecting Input Rewrite](#selecting-input-rewrite)
  * [Selecting Batch Rewrite](#selecting-batch-rewrite)
* [Config](#config)

# Setup (linux)

## Set up a virtual enviorenment for python packages (optional)

Run the following in root of project. (You might need to install something before it works...)
```
$ python -m venv .venv
```

Activate it by running:
```
$ source .venv/bin/activate
```

Deactivate it by running:
```
$ deactivate
```

Check out [python docs venv](https://docs.python.org/3/library/venv.html) for more info.

## Download requirements

Go to the root directory of the project, enable virtual enviorenment (optinal) and run the following.
```
$ pip install -r requirements.txt
```

## Setup automatic venv switching (optional)

Make a file somewhere and call it something like `cdmod.sh`:
```bash
function cd() {
  builtin cd "$@"

  if [[ -z "$VIRTUAL_ENV" ]] ; then
    ## If env folder is found then activate the vitualenv
      if [[ -d ./.venv ]] ; then
        source ./.venv/bin/activate
      fi
  else
    ## check the current folder belong to earlier VIRTUAL_ENV folder
    # if yes then do nothing
    # else deactivate
      parentdir="$(dirname "$VIRTUAL_ENV")"
      if [[ "$PWD"/ != "$parentdir"/* ]] ; then
        deactivate
      fi
  fi
}
```

Run
```
$ chmod +x cdmod.sh
```

Add this line to your `.bashrc` or `.zshrc`:
```bash
...
source <path>/cdmod.sh
```

# Run

Before running SLalter make sure that `ollama` is running. Check that `ollama` runs using:
```
$ ollama ps
```

If it isn't running run it using:
```
$ ollama serve
```

Now, run SLalter using:
```
$ python src/main.py
```

This should show a list of the available models.

```
Which model would you like to use?
  0) smollm2:135m
  1) smollm2:360m
  2) smollm2:1.7b
  3) smollm2:1.7b-instruct-fp16
  4) deepseek-r1:1.5b
  5) deepseek-r1:7b
  6) llama3.2:1b
  7) llama3.2
  8) gemma3:1b
  9) nemotron-mini:4b-instruct-fp16
  10) gemma3:27b-it-q8_0
Please select an option:
```

When selecting a model it might take a while to download. Especicially if selecting a big model like `gemma3:27b-it-q8_0`.

Afterwards you get an option to select either `Input rewrite` or `Batch rewrite`.

## Selecting `Input rewrite`

You are now able to write an "original" piece of dialogue and the language model will generate a rewritten piece of dialogue.

You can then:
* Write `again` to generate a new dialogue piece from the "original" one you wrote.
* Write `continue` to generate a new dialogue piece from the previous generated dialogue piece.
* Write a new original dialogue piece.

Everything generated will be saved in the `logs/` directory.

## Selecting `Batch rewrite`

`Batch rewrite` will make many generated pieces of dialogue...

You will then be asked to select a batch file from the list of files in the `batches/` directory. It then asks you how many generated pieces of dialogue you want per batch entry. It then asks you to select `auto`, `prompt` or `rewrite`.

* `prompt` will use the key `prompt` for every batch entry and utilize instruction-based generation, and ignore batch entries without it.
* `rewrite` will use the key `original` for every batch entry and utilize rewrite-based generation, and ignore batch entries without it.
* `auto` will use either `prompt` or `original` for every batch entry and utilize the according generation method.

The dialogue generation process will then begin and show a progess bar. Then finished it will save the results to the `output/` directory.

# Config

The temperature and role can be configured in `config.json`:
```json
{
    "temperature": 1.0,
    "role": "user"
}
```

Models can be added to or removed from the list in `main.py`. They will only be downloaded when selecting them when running SLalter:
```python
models = [
    "smollm2:135m",
    "smollm2:360m",
    ...
]
```

Batches can be added to, changed or removed from the `batches/` directory

All dialogue generation prompts are stored in the `config/` directory.
* The prompts used for rewrite-based generation are `rewrite_prompt.txt` and `rewrite_system_prompt.txt`.
* The prompts used for instruction-based generation are `prompt_prompt.txt` and `prompt_system_prompt.txt`.
* The prompt for context addition is `context_addition.txt`.

