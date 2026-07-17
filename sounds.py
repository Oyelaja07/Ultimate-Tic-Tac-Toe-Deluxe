try:
    import winsound
except ImportError:
    winsound = None


def _beep(frequency, duration, enabled=True):
    if not enabled or winsound is None:
        return

    try:
        winsound.Beep(frequency, duration)
    except RuntimeError:
        pass


def play_click(enabled=True):
    _beep(700, 50, enabled)


def play_win(enabled=True):
    for frequency, duration in ((800, 90), (1000, 90), (1200, 140)):
        _beep(frequency, duration, enabled)


def play_draw(enabled=True):
    _beep(500, 100, enabled)
    _beep(400, 130, enabled)
