import click
from rich.console import Console
from rich.markdown import Markdown

from transcript import fetch_transcript
from ai import run_action

console = Console()


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    """vox — turn any YouTube video into study material."""
    if ctx.invoked_subcommand is None:
        from tui import launch_ui
        launch_ui()

def run_and_print(action, url, question=""):
    with console.status("[cyan]Fetching transcript...[/cyan]"):
        try:
            transcript, _ = fetch_transcript(url)
        except RuntimeError as e:
            console.print("[red]Error:[/red] " + str(e))
            return


    with console.status("[cyan]Thinking...[/cyan]"):
        try:
            result = run_action(action, transcript, question=question)
        except RuntimeError as e:
            console.print("[red]Error:[/red] " + str(e))
            return

    console.print(Markdown(result))        


@cli.command()
@click.argument("url")
def summarize(url):
    """Summarize a YouTube video."""
    run_and_print("summary", url)

@cli.command()
@click.argument("url")
def notes(url):
    """Generate study notes from a YouTube video."""
    run_and_print("notes", url)


@cli.command()
@click.argument("url")
def quiz(url):
    """Create quiz questions from a YouTube video."""
    run_and_print("quiz", url)


@cli.command()
@click.argument("url")
def keypoints(url):
    """Extract key points from a YouTube video."""
    run_and_print("keypoints", url)


@cli.command()
@click.argument("url")
@click.argument("question")
def ask(url, question):
    """Ask a question about a YouTube video."""
    run_and_print("ask", url, question=question)



def main():
    cli()

if __name__ == "__main__":
    main()


