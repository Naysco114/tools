class Stream:
    """Redirects console output to text widget."""

    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, text):
        self.text_widget.append(text)

    def flush(self):
        pass  # No-op for flush
