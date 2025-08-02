from _typeshed import Incomplete
from fire.console import console_attr_os as console_attr_os, text as text

class BoxLineCharacters: ...

class BoxLineCharactersUnicode(BoxLineCharacters):
    dl: str
    dr: str
    h: str
    hd: str
    hu: str
    ul: str
    ur: str
    v: str
    vh: str
    vl: str
    vr: str
    d_dl: str
    d_dr: str
    d_h: str
    d_hd: str
    d_hu: str
    d_ul: str
    d_ur: str
    d_v: str
    d_vh: str
    d_vl: str
    d_vr: str

class BoxLineCharactersAscii(BoxLineCharacters):
    dl: str
    dr: str
    h: str
    hd: str
    hu: str
    ul: str
    ur: str
    v: str
    vh: str
    vl: str
    vr: str
    d_dl: str
    d_dr: str
    d_h: str
    d_hd: str
    d_hu: str
    d_ul: str
    d_ur: str
    d_v: str
    d_vh: str
    d_vl: str
    d_vr: str

class BoxLineCharactersScreenReader(BoxLineCharactersAscii):
    dl: str
    dr: str
    hd: str
    hu: str
    ul: str
    ur: str
    vh: str
    vl: str
    vr: str

class ProgressTrackerSymbols: ...

class ProgressTrackerSymbolsUnicode(ProgressTrackerSymbols):
    @property
    def spin_marks(self): ...
    success: Incomplete
    failed: Incomplete
    interrupted: str
    not_started: str
    prefix_length: int

class ProgressTrackerSymbolsAscii(ProgressTrackerSymbols):
    @property
    def spin_marks(self): ...
    success: str
    failed: str
    interrupted: str
    not_started: str
    prefix_length: int

class ConsoleAttr:
    def __init__(self, encoding=None, suppress_output: bool = False) -> None: ...
    def Colorize(self, string, color, justify=None): ...
    def ConvertOutputToUnicode(self, buf): ...
    def GetBoxLineCharacters(self): ...
    def GetBullets(self): ...
    def GetProgressTrackerSymbols(self): ...
    def GetControlSequenceIndicator(self): ...
    def GetControlSequenceLen(self, buf): ...
    def GetEncoding(self): ...
    def GetFontCode(self, bold: bool = False, italic: bool = False): ...
    def GetRawKey(self): ...
    def GetTermIdentifier(self): ...
    def GetTermSize(self): ...
    def DisplayWidth(self, buf): ...
    def SplitIntoNormalAndControl(self, buf): ...
    def SplitLine(self, line, width): ...
    def SupportsAnsi(self): ...

class Colorizer:
    def __init__(self, string, color, justify=None) -> None: ...
    def __eq__(self, other): ...
    def __ne__(self, other): ...
    def __gt__(self, other): ...
    def __lt__(self, other): ...
    def __ge__(self, other): ...
    def __le__(self, other): ...
    def __len__(self) -> int: ...
    def Render(self, stream, justify=None) -> None: ...

def GetConsoleAttr(encoding=None, reset: bool = False): ...
def ResetConsoleAttr(encoding=None): ...
def GetCharacterDisplayWidth(char): ...
def SafeText(data, encoding=None, escape: bool = True): ...
def EncodeToBytes(data): ...
def Decode(data, encoding=None): ...
