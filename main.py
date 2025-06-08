from langchain_ollama import ChatOllama
from langchain.tools import StructuredTool
from pydantic import BaseModel, Field
from langchain_core.messages import ToolMessage, HumanMessage, AIMessage, SystemMessage
import subprocess
from prompts import SYSTEM_PROMPT
from rich.console import Console
from rich.markdown import Markdown

# ----------- Initialize Console for Rich Rendering -----------
console = Console()

# ----------- Initialize the Chat Model -----------
chat_model = ChatOllama(model="qwen3:4b")


# ----------- Tool 1: Identify Memory Image OS -----------

class IdentifyMemoryOSInput(BaseModel):
    file_path: str = Field(..., description="File path where the memory image is located.")


def identify_memory_image_os(file_path: str) -> str:
    try:
        result = subprocess.run(["file", file_path], capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"Error identifying OS: {e.stderr.strip()}"


identify_memory_tool = StructuredTool.from_function(
    func=identify_memory_image_os,
    name="MemoryOSIdentifier",
    description="Identifies the operating system of a memory image using the `file` command.",
    args_schema=IdentifyMemoryOSInput
)


# ----------- Tool 2: Run Volatility Command -----------

class VolatilityInput(BaseModel):
    plugin: str = Field(..., description="Necessary plugin for the memory image.")
    filePath: str = Field(..., description="File path where the memory image is located.")


def run_volatility_command(plugin: str, filePath: str) -> str:
    try:
        result = subprocess.run(["vol", "-f", filePath, plugin], capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"Volatility command failed: {e.stderr.strip()}"


volatility_tool = StructuredTool.from_function(
    func=run_volatility_command,
    name="Volatility3",
    description="Executes a Volatility3 command to perform memory forensics.",
    args_schema=VolatilityInput
)


# ----------- Bind Tools to Chat Model -----------

chat_model_with_tools = chat_model.bind_tools([identify_memory_tool, volatility_tool])


# ----------- Forensics Workflow -----------

def run_forensics_workflow(memory_image_path: str):
    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=f"Hello, I want to do memory forensics on this file {memory_image_path}")
    ]

    console.print("\n========================= Initial Query =========================", style="bold white")
    console.print("Human > " + messages[-1].content, style="green")

    response = chat_model_with_tools.invoke(messages)
    console.print(Markdown(response.content), style="bold blue")

    messages.append(response)

    if response.tool_calls:
        os_identification_result = identify_memory_tool.invoke(response.tool_calls[0])
        messages.append(os_identification_result)

        console.print("\n===================== Tool: OS Identifier =====================", style="bold yellow")
        console.print("Tool called > ", style="yellow")
        console.print(response.tool_calls, style="yellow")

        response = chat_model_with_tools.invoke(messages)
        messages.append(response)

        console.print(Markdown(response.content), style="bold blue")

    while True:
        console.print("\n======================= Follow-Up Query ========================", style="bold white")
        follow_up = console.input("[green]Human > [/green]")

        if follow_up.strip().lower() == "exit":
            console.print("Exiting memory forensics session.", style="red")
            break

        messages.append(HumanMessage(content=follow_up))

        response = chat_model_with_tools.invoke(messages)
        messages.append(response)

        if response.tool_calls:
            for tool_call in response.tool_calls:
                if tool_call["name"] == "Volatility3":
                    tool_result = volatility_tool.invoke(tool_call)
                    messages.append(tool_result)

                    console.print("\n===================== Tool: Volatility3 =====================", style="bold yellow")
                    console.print("Tool called > ", style="yellow")
                    console.print(tool_call, style="yellow")

                    response = chat_model_with_tools.invoke(messages)
                    messages.append(response)

        console.print(Markdown(response.content), style="bold blue")


# ----------- Entry Point -----------

if __name__ == "__main__":
    memory_image_path = input("Please give absolute path to your memory image _> ")
    run_forensics_workflow(memory_image_path)
