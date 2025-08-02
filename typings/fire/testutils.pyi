import contextlib
import unittest
from _typeshed import Incomplete
from collections.abc import Generator
from fire import core as core, trace as trace

class BaseTestCase(unittest.TestCase):
    @contextlib.contextmanager
    def assertOutputMatches(self, stdout: str = '.*', stderr: str = '.*', capture: bool = True) -> Generator[None]: ...
    @contextlib.contextmanager
    def assertRaisesFireExit(self, code, regexp: str = '.*') -> Generator[None]: ...

@contextlib.contextmanager
def ChangeDirectory(directory) -> Generator[Incomplete]: ...

main: Incomplete
skip = unittest.skip
skipIf = unittest.skipIf
