from textual.app import App, ComposeResult
from textual.containers import Horizontal, VerticalScroll
from textual.widgets import Button, Static
from model import Dictionary


class MainMenu(App[str]):
    CSS_PATH = "css/button.tcss"

    def __init__(self, dict_manager: Dictionary):
        super().__init__()
        self.dict_manager = dict_manager

    def compose(self) -> ComposeResult:
        yield Horizontal(
            VerticalScroll(
                Static("Menu", classes="header"),
                Button("Manage", id="manage"),
                Button("Review", id="review"),
                Button("Random", id="random"),
                Button("Play", id="play"),
                Button("Exit", id="exit"),
            )
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Event handler called when a button is pressed."""
        if event.button.id == "manage":
            self.manager.show("manage")
        elif event.button.id == "review":
            self.manager.show("review")
        elif event.button.id == "random":
            self.manager.show("random")
        elif event.button.id == "play":
            self.manager.show("play")
        elif event.button.id == "exit":
            self.exit(str(event.button))
