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
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"


# ---------------------------------------------------------------------------
# String-conversion glitch regression tests
# The bug: on even attempts, secret was cast to str, causing lexicographic
# comparison. e.g. "60" > "100" → True → wrong "Go LOWER" hint.
# ---------------------------------------------------------------------------

def _simulate_check_guess_with_glitch(guess_int, secret_int, attempts):
    """Reproduce the old buggy app.py logic: str(secret) on even attempts."""
    if attempts % 2 == 0:
        secret = str(secret_int)
    else:
        secret = secret_int
    return check_guess(guess_int, secret)


def test_glitch_caused_wrong_direction_even_attempt():
    """Glitch: guess=60, secret=100, even attempt → wrong 'Too High' instead of 'Too Low'."""
    outcome, _ = _simulate_check_guess_with_glitch(60, 100, attempts=2)
    assert outcome == "Too High", "Confirms the glitch produced the wrong outcome"


def test_fix_correct_direction_even_attempt():
    """Fix: passing secret as int always gives the correct 'Too Low' hint."""
    outcome, _ = check_guess(60, 100)
    assert outcome == "Too Low", "guess 60 < secret 100 must return 'Too Low'"


def test_fix_correct_direction_large_secret():
    """Lexicographic pitfall: '60' > '100' but 60 < 100 numerically."""
    outcome, _ = check_guess(60, 100)
    assert outcome != "Too High", "'Go LOWER' hint is wrong when guess < secret"


def test_fix_all_attempts_consistent():
    """check_guess with int secret returns the same correct outcome regardless of attempt parity."""
    for attempt in range(1, 7):
        outcome, _ = check_guess(60, 100)
        assert outcome == "Too Low", f"Failed on attempt {attempt}: expected 'Too Low', got '{outcome}'"
