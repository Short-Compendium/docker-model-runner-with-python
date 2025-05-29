# Baby steps in Generative AI with Docker Model Runner, Python and LiteLLM

I've been telling myself for quite some time now that I need to seriously get into Python. That moment is today!
And I couldn't settle for a simple "👋 hello world 🌍". Given my current passions, my job, and my curious nature, what could be more "natural" than taking my first real steps in Python with the "hello world" of Generative AI.

So for me, the "hello world" of Generative AI is asking an LLM "Who is James T. Kirk's best friend?" 🖖.
> Ref: [https://en.wikipedia.org/wiki/Star_Trek](https://en.wikipedia.org/wiki/Star_Trek)

This blog post will be short. The objective is to gently start a series of experiments with **[Docker Model Runner](https://docs.docker.com/model-runner/)** and Python.

## Prerequisites

### Development Environment

Of course, you need a Python development environment. Personally, I use VSCode with [Dev Containers](https://containers.dev/), Python `3.9.22` (you'll find my configuration in the repository related to this article: [.devcontainer](https://github.com/Short-Compendium/docker-model-runner-with-python/tree/main/.devcontainer))

### Libraries, frameworks, ...

I'll obviously use **[Docker Model Runner](https://docs.docker.com/model-runner/)** (I wrote an introduction to Docker Model Runner with Golang: [First Contact with Docker Model Runner in Golang](https://k33g.hashnode.dev/first-contact-with-docker-model-runner-in-golang)) and to interact in Python with **Docker Model Runner**, I'm going to use the **[LiteLLM Python SDK](https://www.litellm.ai/)**.

### Virtual Environment Setup

First, create a Python virtual environment:
```bash
python -m venv discovery
```
> you can of course name it something other than `discovery`

Then, activate the environment:
```bash
source discovery/bin/activate
```
> to deactivate the environment, just use the `deactivate` command

Next, create a `requirements.txt` file with the following content:
```requirements
litellm
```

And install the dependencies with the following command:

```bash
pip install -r requirements.txt
```

>✋ **Disclaimer**: I'm not a Python developer at all, I gladly accept all improvement suggestions.

### Loading the Models

We're going to use `ai/qwen2.5:latest`, so don't forget to run the following command if you don't already have this model on your machine:

```bash
docker model pull ai/qwen2.5:latest
```

And now we're ready for our first Generative AI program in Python 🚀.

## Chat completion

You'll see, it's extremely simple:
```python
import os
from litellm import completion

response = completion(
    model="openai/ai/qwen2.5:latest", 
    api_key="tada",
    api_base=f"{os.environ.get('DMR_BASE_URL')}/engines/llama.cpp/v1",
    messages=[
        {
            "role": "user", 
            "content": "Who is James T. Kirk's best friend?"
        }
    ],
)
# Display the result of the completion
print(response.choices[0].message.content)
```

What's important to know:

- To use the OpenAI API with LiteLLM and a local LLM, you must prefix the **model name** with `openai/`
- Regarding the **OpenAI API key**, you can't leave it empty, it needs to "contain" something (but the content doesn't matter).
- For the `api_base` field, since I'm running my application from inside a container, I use this value: `http://model-runner.docker.internal/engines/llama.cpp/v1`. If you're working "outside" of a container, use `http://localhost:12434/engines/llama.cpp/v1`.

> In my case, I have an environment variable that's defined when loading the Dev Container (`DMR_BASE_URL=http://model-runner.docker.internal`).

I then defined my list of messages to send to the LLM:
```python
messages=[
    {
        "role": "user", 
        "content": "Who is James T. Kirk's best friend?"
    }
],
```

And to run the program, use the following command:
```bash
python main.py 
```

And after a few seconds, you'll get text like this:
```raw
James T. Kirk's best friend in the Star Trek universe is usually considered to be his first officer, Mr. Spock. Despite their differences in background and philosophy (Kirk is human and Spock is half-Vulcan), their friendship is a central part of their dynamic in the original Star Trek series and many subsequent Star Trek productions.
```

You see, nothing simpler. Now, before I let you go, let's look at the "streaming" version of this program.

## Streaming Chat completion

The code isn't much more complicated than the previous one:
```python
import os
from litellm import completion

response = completion(
    model="openai/ai/qwen2.5:latest", 
    api_key="tada",
    api_base=f"{os.environ.get('DMR_BASE_URL')}/engines/llama.cpp/v1",
    messages=[
        {
            "role": "user", 
            "content": "Who is James T. Kirk's best friend?"
        }
    ],
    stream=True,
)

# Stream the answer
for chunk in response:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end='', flush=True)

```
So you just need to add `stream=True` to the parameters of the `completion` function and create a loop to call the completion progressively.

Here too, to run the program, use the following command:
```bash
python main.py 
```

And this time the completion result will display in your terminal progressively.

There you have it, that's all for this article. See you very soon for the continuation.

> You can find the source code examples here:
> - [https://github.com/Short-Compendium/docker-model-runner-with-python/blob/main/01-litellm-completion/main.py](https://github.com/Short-Compendium/docker-model-runner-with-python/blob/main/01-litellm-completion/main.py)
> - [https://github.com/Short-Compendium/docker-model-runner-with-python/blob/main/02-litellm-stream-completion/main.py](https://github.com/Short-Compendium/docker-model-runner-with-python/blob/main/02-litellm-stream-completion/main.py)