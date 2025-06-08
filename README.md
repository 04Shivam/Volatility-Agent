# Memory Forensics Assistant using LangChain and Volatility

This project is a command-line memory forensics assistant that leverages natural language processing via LangChain and Ollama to help analysts investigate memory images. It integrates Volatility3 for advanced memory analysis and uses real system tools to create a seamless, AI-driven workflow.

![Demo](demo.gif) <!-- Replace 'demo.gif' with your actual file path or URL -->

## Features

- Interactive assistant for memory forensics powered by a large language model (LLM)
- Automatic operating system detection of memory images using the `file` command
- Integration with Volatility3 to run forensic plugins on memory dumps
- Conversational interface that understands natural language input
- Rich terminal output using `rich` for better readability and markdown rendering

## Requirements

Ensure the following are installed on your system:

- **Python** 3.8 or later
- **Ollama** with the `qwen3:4b` model installed  
  [Install Ollama](https://ollama.com)
- **Volatility3** installed and accessible via the `vol` command  
  [Volatility3 GitHub](https://github.com/volatilityfoundation/volatility3)
- **file** utility (comes preinstalled on most Unix systems)

## Install Python dependencies with:

```bash
$ pip3 install langchain langchain-core langchain-ollama pydantic rich
```

## Pull ollama model

```bash
$ ollama pull qwen3:4b
```

## How It Works

1. **Identify the Operating System**  
   The assistant uses the file command to determine the OS type of the provided memory image.

2. **Volatility3 Plugin Execution**  
   The assistant can execute user-requested Volatility3 plugins on the memory image and summarize or explain results.

3. **Chat-Based Interaction**  
   The entire interaction is done via natural language. You can ask follow-up questions or request plugin execution in plain English.
