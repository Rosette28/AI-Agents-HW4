class Instrumentation:
    def __init__(self) -> None:
        self.tokens_used = 0
        self.files_read = 0
        self.iterations = 0
        self.llm_calls = 0

    def log_llm_call(self) -> None:
        self.llm_calls += 1

    def log_file_read(self) -> None:
        self.files_read += 1

    def log_iteration(self) -> None:
        self.iterations += 1

    def add_tokens(self, amount: int) -> None:
        self.tokens_used += amount

    def finalize(self) -> dict:
        return {
            "tokens_used": self.tokens_used,
            "files_read": self.files_read,
            "iterations": self.iterations,
            "llm_calls": self.llm_calls,
        }