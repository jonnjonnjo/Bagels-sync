from textual.widgets import OptionList
from bagels.components.modal_options import ModalOptions


class ModalDBSync(ModalOptions):
    """Modal specifically for database sync confirmation."""

    def __init__(self) -> None:
        super().__init__(
            message="Are you sure you want to sync the database?",
            options=["Yes, sync now", "No, cancel sync"],
        )

    # Optional: Override if you need specific behavior
    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        """Handle DB sync specific selection."""
        selected = event.option.prompt
        if "Yes" in selected:
            self.dismiss("sync")
        else:
            self.dismiss("cancel")
