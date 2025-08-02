import enum
from _typeshed import Incomplete
from typing import NamedTuple

class DocstringInfo(NamedTuple('DocstringInfo', [('summary', Incomplete), ('description', Incomplete), ('args', Incomplete), ('returns', Incomplete), ('yields', Incomplete), ('raises', Incomplete)])): ...
class ArgInfo(NamedTuple('ArgInfo', [('name', Incomplete), ('type', Incomplete), ('description', Incomplete)])): ...
class KwargInfo(ArgInfo): ...

class Namespace(dict):
    def __getattr__(self, key): ...
    def __setattr__(self, key, value) -> None: ...
    def __delattr__(self, key) -> None: ...

class Sections(enum.Enum):
    ARGS = 0
    RETURNS = 1
    YIELDS = 2
    RAISES = 3
    TYPE = 4

class Formats(enum.Enum):
    GOOGLE = 0
    NUMPY = 1
    RST = 2

SECTION_TITLES: Incomplete

def parse(docstring): ...
