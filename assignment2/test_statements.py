import unittest
from statements import Lexicon, FactBase

class LexiconTestCase(unittest.TestCase):
    def test_lexicon_add(self):
        lx = Lexicon()
        lx.add("John", "P")
        lx.add("Mary", "P")
        self.assertEqual(lx.stemCatPairs, [("John", "P"), ("Mary", "P")])

    def test_lexicon_add_should_allow_duplicate(self):
        lx = Lexicon()
        lx.add("John", "P")
        lx.add("John", "P")
        self.assertEqual(lx.stemCatPairs, [("John", "P"), ("John", "P")])

    def test_lexicon_getAll(self):
        lx = Lexicon()
        lx.add("John", "P")
        lx.add("Mary", "P")
        self.assertEqual(sorted(lx.getAll("P")), sorted(["John", "Mary"]))

    def test_lexicon_getAll_should_return_without_repetitions(self):
        lx = Lexicon()
        lx.add("John", "P")
        lx.add("John", "P")
        self.assertEqual(lx.getAll("P"), ["John"])

class FactBaseTestCase(unittest.TestCase):
    def test_FactBase_addUnary(self):
        fb = FactBase()
        fb.addUnary("duck", "John")
        fb.addUnary("bird", "pigeon")
        self.assertEqual(
            fb.unaryFacts,
            set([("duck", "John"), ("bird", "pigeon")])
        )

    def test_FactBase_queryUnary(self):
        fb = FactBase()
        fb.addUnary("duck", "John")
        fb.addUnary("bird", "pigeon")
        self.assertTrue(fb.queryUnary("duck", "John"))
        self.assertFalse(fb.queryUnary("bird", "retriever"))

    def test_FactBase_addBinary(self):
        fb = FactBase()
        fb.addBinary("love", "WJ", "AN")
        fb.addBinary("play", "WJ", "tennis")
        self.assertEqual(
            fb.binaryFacts,
            set([("love", "WJ", "AN"), ("play", "WJ", "tennis")])
        )

    def test_FactBase_queryBinary(self):
        fb = FactBase()
        fb.addBinary("love", "WJ", "AN")
        fb.addBinary("play", "WJ", "tennis")
        self.assertTrue(fb.queryBinary("love", "WJ", "AN"))
        self.assertTrue(fb.queryBinary("play", "WJ", "tennis"))
        self.assertFalse(fb.queryBinary("play", "tennis", "WJ"))


if __name__ == '__main__':
    unittest.main()
