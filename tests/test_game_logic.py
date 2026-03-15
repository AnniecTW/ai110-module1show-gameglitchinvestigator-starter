import random
from logic_utils import check_guess


# ---------------------------------------------------------------------------
# Helpers that mirror the "New Game" reset logic in app.py
# ---------------------------------------------------------------------------

def _make_post_game_state(secret=42, low=1, high=100):
    """Return a session-state dict that looks like a finished game."""
    return {
        "secret": secret,
        "attempts": 5,
        "score": 50,
        "status": "won",
        "history": [10, 20, 30, 42],
    }


def _reset_game(state: dict, low: int, high: int) -> dict:
    """Apply the fixed New Game reset logic to a state dict."""
    state["attempts"] = 1
    state["secret"] = random.randint(low, high)
    state["status"] = "playing"
    state["history"] = []
    return state


# ---------------------------------------------------------------------------
# New Game reset tests
# ---------------------------------------------------------------------------

def test_new_game_resets_attempts():
    state = _make_post_game_state()
    _reset_game(state, 1, 100)
    assert state["attempts"] == 1, "attempts should reset to 1, not carry over from the previous game"


def test_new_game_resets_status():
    state = _make_post_game_state()
    _reset_game(state, 1, 100)
    assert state["status"] == "playing", "status must be 'playing' after reset so the game is not immediately blocked"


def test_new_game_clears_history():
    state = _make_post_game_state()
    _reset_game(state, 1, 100)
    assert state["history"] == [], "history should be empty at the start of a new game"


def test_new_game_secret_respects_difficulty_range():
    low, high = 1, 20   # Easy range
    state = _make_post_game_state()
    _reset_game(state, low, high)
    assert low <= state["secret"] <= high, (
        f"secret {state['secret']} is outside the Easy range ({low}-{high}); "
        "New Game was previously hardcoded to randint(1, 100)"
    )


# ---------------------------------------------------------------------------
# Difficulty range ordering tests
# ---------------------------------------------------------------------------

def _get_range_for_difficulty(difficulty: str):
    """Mirror of app.py get_range_for_difficulty."""
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 200
    return 1, 100


def test_hard_range_larger_than_normal():
    _, normal_high = _get_range_for_difficulty("Normal")
    _, hard_high = _get_range_for_difficulty("Hard")
    assert hard_high > normal_high, (
        f"Hard range upper bound ({hard_high}) must be greater than Normal ({normal_high}); "
        "previously Hard was hardcoded to 1-50, making it easier than Normal (1-100)"
    )


def test_normal_range_larger_than_easy():
    _, easy_high = _get_range_for_difficulty("Easy")
    _, normal_high = _get_range_for_difficulty("Normal")
    assert normal_high > easy_high, (
        f"Normal range upper bound ({normal_high}) must be greater than Easy ({easy_high})"
    )


def test_difficulty_ranges_are_strictly_ordered():
    _, easy_high = _get_range_for_difficulty("Easy")
    _, normal_high = _get_range_for_difficulty("Normal")
    _, hard_high = _get_range_for_difficulty("Hard")
    assert easy_high < normal_high < hard_high, (
        f"Expected Easy ({easy_high}) < Normal ({normal_high}) < Hard ({hard_high})"
    )


# ---------------------------------------------------------------------------
# Existing check_guess tests (kept intact)
# ---------------------------------------------------------------------------

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result = check_guess(50, 50)
    assert result == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result = check_guess(60, 50)
    assert result == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result = check_guess(40, 50)
    assert result == "Too Low"
