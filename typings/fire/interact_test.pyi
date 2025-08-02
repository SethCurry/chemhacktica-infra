from fire import interact as interact, testutils as testutils

INTERACT_METHOD: str

class InteractTest(testutils.BaseTestCase):
    def testInteract(self, mock_interact_method) -> None: ...
    def testInteractVariables(self, mock_interact_method) -> None: ...
