from _typeshed import Incomplete
from fire import completion as completion, custom_descriptions as custom_descriptions, decorators as decorators, docstrings as docstrings, formatting as formatting, inspectutils as inspectutils, value_types as value_types

LINE_LENGTH: int
SECTION_INDENTATION: int
SUBSECTION_INDENTATION: int

def HelpText(component, trace=None, verbose: bool = False): ...
def UsageText(component, trace=None, verbose: bool = False): ...

class ActionGroup:
    name: Incomplete
    plural: Incomplete
    names: Incomplete
    members: Incomplete
    def __init__(self, name, plural) -> None: ...
    def Add(self, name, member=None) -> None: ...
    def GetItems(self): ...
