from fire import docstrings as docstrings, testutils as testutils

class DocstringsFuzzTest(testutils.BaseTestCase):
    def test_fuzz_parse(self, value) -> None: ...
