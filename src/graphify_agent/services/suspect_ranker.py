def rank(candidates: list[str]) -> list[str]:
    scores = {
        "httpie.sessions": 10,
        "httpie.downloads": 8,
        "httpie.client": 7,
    }

    return sorted(
        candidates,
        key=lambda item: scores.get(item, 0),
        reverse=True,
    )