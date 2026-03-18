import threading
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Input, RichLog

from transcript import fetch_transcript
from ai import run_action


class VoxApp(App):
    """The vox interactive terminal UI."""
    CSS = """
    Screen {
        layout: vertical;
    }

    RichLog {
        height: 1fr;
        border: solid green;
        padding: 1;
    }

    Input {
        dock: bottom;
    }
    """
    BINDINGS = [("escape", "quit", "Quit")]

    def __init__(self):
        super().__init__()
        self.current_transcript = ""
        self.current_url = ""

    def compose(self) -> ComposeResult:
        yield Header()
        yield RichLog(id="output", markup=True, wrap=True)
        yield Input(placeholder="Type a command... /load /summary /notes /quiz /ask /quit", id="cmd-input")
        yield Footer()

    def on_mount(self) -> None:
        self.query_one(RichLog).write("[bold green]Welcome to Vox![/bold green]")
        self.query_one(RichLog).write("Commands: /load <url> — /summary — /notes — /quiz — /ask <question> — /quit")
        self.query_one(Input).focus()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        command = event.value.strip()
        event.input.clear()
        if not command:
            return
        self.handle_command(command)    
     
    def handle_command(self, command: str) -> None:
        log = self.query_one(RichLog)

        if command.startswith("/load"):
            parts = command.split(" ", 1)
            if len(parts) < 2:
                log.write("[red]Usage: /load <url>[/red]")
                return
            url = parts[1].strip()
            self.load_video(url)

        elif command == "/summary":
            self.run_action_threaded("summary")

        elif command == "/notes":
            self.run_action_threaded("notes")

        elif command == "/quiz":
            self.run_action_threaded("quiz")

        elif command == "/keypoints":
            self.run_action_threaded("keypoints")

        elif command.startswith("/ask"):
            parts = command.split(" ", 1)
            if len(parts) < 2:
                log.write("[red]Usage: /ask <question>[/red]")
                return
            question = parts[1].strip()
            self.run_action_threaded("ask", question=question)

        elif command == "/quit":
            self.exit()

        else:
            log.write(f"[red]Unknown command: {command}[/red]")


    def load_video(self, url: str) -> None:
        log = self.query_one(RichLog)
        log.write(f"[cyan]Loading transcript for {url}...[/cyan]")

        def worker():
            try:
                transcript, _ = fetch_transcript(url)
                self.current_transcript = transcript
                self.current_url = url
                word_count = len(transcript.split())
                self.call_from_thread(
                    log.write,
                    f"[green]✓ Loaded! {word_count} words. Now try /summary /notes /quiz[/green]"
                )
            except RuntimeError as e:
                self.call_from_thread(log.write, f"[red]Error: {e}[/red]")

        threading.Thread(target=worker, daemon=True).start()


    def load_video(self, url: str) -> None:
        log = self.query_one(RichLog)
        log.write(f"[cyan]Loading transcript for {url}...[/cyan]")

        def worker():
            try:
                transcript, _ = fetch_transcript(url)
                self.current_transcript = transcript
                self.current_url = url
                word_count = len(transcript.split())
                self.call_from_thread(
                    log.write,
                    f"[green]✓ Loaded! {word_count} words. Now try /summary /notes /quiz[/green]"
                )
            except RuntimeError as e:
                self.call_from_thread(log.write, f"[red]Error: {e}[/red]")

        threading.Thread(target=worker, daemon=True).start()
    
    def run_action_threaded(self, action: str, question: str = "") -> None:
        log = self.query_one(RichLog)

        if not self.current_transcript:
            log.write("[red]No video loaded. Use /load <url> first.[/red]")
            return

        log.write(f"[cyan]Running {action}...[/cyan]")

        def worker():
            try:
                result = run_action(action, self.current_transcript, question=question)
                self.call_from_thread(log.write, result)
            except RuntimeError as e:
                self.call_from_thread(log.write, f"[red]Error: {e}[/red]")

        threading.Thread(target=worker, daemon=True).start()
       
        def on_key(self, event) -> None:
            if event.key == "space":
             input_widget = self.query_one("#cmd-input", Input)
             input_widget.insert_text_at_cursor(" ")
             event.prevent_default()
def launch_ui():
    app = VoxApp()
    app.run()


if __name__ == "__main__":
    launch_ui()        

        
