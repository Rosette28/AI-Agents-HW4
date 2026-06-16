class Instrumentation:
    def __init__(self) -> None:
        self.tokens_used = 0
        self.files_read = 0
        self.iterations = 0

    def log_file(self) -> None:
        self.files_read += 1

    def log_iteration(self) -> None:
        self.iterations += 1

    def summary(self) -> dict:
        return {
            "tokens_used": self.tokens_used,
            "files_read": self.files_read,
            "iterations": self.iterations,
        }