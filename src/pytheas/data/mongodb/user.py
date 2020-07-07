from dataclasses import dataclass
import persistent


@dataclass
class User(persistent.Persistent):
    name: str
