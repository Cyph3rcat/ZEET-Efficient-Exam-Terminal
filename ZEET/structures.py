
# Standard‑library imports
import json                     # for saving / loading JSON files
from pathlib import Path        # Path objects used in `save` / `load`

# Dataclass utilities
from dataclasses import dataclass, field

# Type‑hints for the data structures
from typing import List, Optional, Dict


# Essential question Data structures
@dataclass
class QuestionState:
    id: int # question number
    type: str
    stem: str
    options: List[str] = field(default_factory=list) #for different types of Qs e.g. mcq
    answer: Optional[str] = None  # canonical answer (for auto-grade)
    user_response: Optional[str] = None #sometimes the answer would still be empty
    score: Optional[float] = None
    points: float = 1.0 # flexible non-integer points system

#
@dataclass
class Session:
    title: str
    questions: List[QuestionState]
    current_index: int = 0
    metadata: Dict = field(default_factory=dict) #default_factory is goofy but necessary

    def save(self, session): # note to self: don't forget to pass in session parameter. SESSIONS_DIR FOR zeet.py
        fn = session / f"{self.title.replace(' ', '_')}.json"
        data = {
            "title": self.title,
            "current_index": self.current_index,
            "metadata": self.metadata,
            "questions": [q.__dict__ for q in self.questions],
        }
        fn.write_text(json.dumps(data, indent=2, ensure_ascii=False))
        return fn

    @staticmethod # methods can be called outside of class instance
    def load(path: Path):
        data = json.loads(path.read_text(encoding="utf-8"))
        qs = [QuestionState(**q) for q in data["questions"]]
        return Session(title=data["title"], questions=qs, current_index=data.get("current_index", 0), metadata=data.get("metadata", {}))
