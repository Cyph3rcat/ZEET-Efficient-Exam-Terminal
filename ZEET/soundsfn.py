import pygame
import threading
import sys
from pathlib import Path

# Directory for sounds
ROOT = Path.cwd()
SOUNDS_DIR = ROOT / "sounds"
SOUNDS_DIR.mkdir(exist_ok=True)

# Default sound files
SOUND_KEYS = {
    "SWITCH": SOUNDS_DIR / "switch.mp3",
    "BUTTON": SOUNDS_DIR / "button.mp3",
    "GRADE": SOUNDS_DIR / "grade.mp3",
}

# Sound player class
class SoundPlayer:
    def __init__(self, enabled=True):
        self.enabled = enabled
        self.cache = {}
        self.lock = threading.Lock()
        if self.enabled:
            try:
                pygame.mixer.init()
            except Exception:
                self.enabled = False
                print("Warning: pygame mixer init failed; sound disabled.", file=sys.stderr)

    def load(self, path: Path):
        if not self.enabled or not path.exists():
            return None
        if str(path) in self.cache:
            return self.cache[str(path)]
        try:
            snd = pygame.mixer.Sound(str(path))
            self.cache[str(path)] = snd
            return snd
        except Exception:
            return None

    def play(self, path: Path):
        if not self.enabled:
            return
        s = self.load(path)
        if s is None:
            return
        def _p():
            with self.lock:
                s.play()
        threading.Thread(target=_p, daemon=True).start()

    def set_enabled(self, flag: bool):
        self.enabled = flag


# single global instance
_player = SoundPlayer(enabled=True)

# simple API for other modules
def set_enabled(flag: bool):
    _player.set_enabled(flag)

def play(name: str):
    path = SOUND_KEYS.get(name.upper())
    if path:
        _player.play(path)

def register(name: str, path: Path):
    SOUND_KEYS[name.upper()] = path
