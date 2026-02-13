from dataclasses import dataclass, field
import time


@dataclass
class AppState:
    output_text: str = ""
    spoken_text: str = ""
    last_letter: str = ""
    last_time: float = field(default_factory=time.time)
    delay: float = 1.0

    def reset(self) -> None:
        self.output_text = ""
        self.spoken_text = ""
        self.last_letter = ""
        self.last_time = time.time()
