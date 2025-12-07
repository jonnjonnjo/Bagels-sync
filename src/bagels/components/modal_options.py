from textual.app import ComposeResult
from textual.containers import Vertical
from textual.screen import ModalScreen
from textual.widgets import Label, OptionList
from textual.widgets.option_list import Option


class ModalOptions(ModalScreen):
    BINDINGS = [
        ("escape", "dismiss", "Cancel"),
    ]

    def __init__(self, message: str, options: list[str]) -> None:
        """
        Args:
            message: The message/question to display
            options: List of option strings to choose from
        """
        super().__init__()
        self.message = message
        self.options = options

    def compose(self) -> ComposeResult:
        with Vertical(id="dialog"):
            yield Label(self.message, id="question")
            yield OptionList(*[Option(opt) for opt in self.options], id="options")

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        """Handle when user selects an option."""
        self.dismiss(event.option.prompt)

    def action_dismiss(self) -> None:
        self.dismiss(None)
