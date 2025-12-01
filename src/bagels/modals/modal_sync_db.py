from textual.widgets import OptionList
from bagels.components.modal_options import ModalOptions


class ModalDBSync(ModalOptions):
    """Modal specifically for database sync confirmation."""

    def __init__(self) -> None:
        super().__init__(
            message="Database Synchronization",
            options=[
                "Download from remote (pull)",
                "Upload to remote (push)",
            ],
        )

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        """Handle DB sync specific selection."""
        selected = event.option.prompt

        if "Download" in selected or "pull" in selected:
            self.dismiss("pull")
        elif "Upload" in selected or "push" in selected:
            self.dismiss("push")
        else:
            self.dismiss("cancel")
