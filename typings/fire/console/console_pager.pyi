from _typeshed import Incomplete
from fire.console import console_attr as console_attr

class Pager:
    HELP_TEXT: str
    PREV_POS_NXT_REPRINT: Incomplete
    def __init__(self, contents, out=None, prompt=None) -> None: ...
    def Run(self) -> None: ...
