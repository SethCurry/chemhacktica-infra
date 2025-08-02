from fire import parser as parser, testutils as testutils

class ParserFuzzTest(testutils.BaseTestCase):
    def testDefaultParseValueFuzz(self, value) -> None: ...
