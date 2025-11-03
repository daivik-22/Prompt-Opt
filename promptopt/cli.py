from dotenv import load_dotenv

load_dotenv()

from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
import json
from promptopt import prompt_optimizer, prompt_scorer, storage, utils

def show_welcome_screen(console):
    logo = """
    ██████╗ ██████╗  ██████╗ ███╗   ███╗ ██████╗ ████████╗
    ██╔══██╗██╔══██╗██╔═══██╗████╗ ████║██╔═══██╗╚══██╔══╝
    ██████╔╝██████╔╝██║   ██║██╔████╔██║██║   ██║   ██║   
    ██╔═══╝ ██╔══██╗██║   ██║██║╚██╔╝██║██║   ██║   ██║   
    ██║     ██║  ██║╚██████╔╝██║ ╚═╝ ██║╚██████╔╝   ██║   
    ╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚═╝ ╚═════╝    ╚═╝   
    """
    console.print(f"[bold magenta]{logo}[/bold magenta]")
    console.print("\n[bold green]Welcome to PromptOpt! ✨[/bold green]")
    console.print("I'm here to help you optimize your prompts.")
    console.print("\n[bold]Tips for getting started:[/bold]")
    console.print("1. Enter a prompt you want to improve.")
    console.print("2. I will provide an analysis and generate improved variants.")
    console.print("3. Type 'exit' or 'quit' to leave the application.")

def main():
    storage.init_db()
    console = Console()
    show_welcome_screen(console)

    engine = Prompt.ask("\n[bold]Choose an engine[/bold]", choices=["local", "openai"], default="local")

    while True:
        prompt = Prompt.ask("\n[bold]Enter a prompt[/bold]")

        if prompt.lower() in ["exit", "quit"]:
            break

        with console.status("[bold green]Optimizing your prompt...[/bold green]"):
            res = prompt_optimizer.optimize_prompt(prompt, engine=engine, n=3)
        
        variants = res["variants"]
        console.print("\n[bold green]✅ Analysis:[/bold green]")
        console.print(res["analysis"])

        table = Table(title="Generated Variants")
        table.add_column("Tag/Style")
        table.add_column("Prompt")
        table.add_column("Rationale", overflow="fold")
        for v in variants:
            table.add_row(v.get("style","-"), v.get("prompt","-"), v.get("rationale","-"))
        console.print(table)

        scored = prompt_scorer.score_variants(variants, prompt)
        console.print("\n[bold blue]Scores:[/bold blue]")
        console.print(scored)
        
        storage.save_history(prompt, json.dumps(scored))

if __name__ == "__main__":
    main()
