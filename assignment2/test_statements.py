import unittest
from statements import Lexicon, FactBase, verb_stem

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

class VerbStemTestCase(unittest.TestCase):
    def test_verb_stem_ends_in_anything_except_sxyzchsh_or_vowel_then_add_s(self):
        self.assertEqual(verb_stem("eats"), "eat")
        self.assertEqual(verb_stem("tells"), "tell")
        self.assertEqual(verb_stem("shows"), "show")

    def test_verb_stem_ends_in_y_preceded_by_a_vowel(self):
        self.assertEqual(verb_stem("pays"), "pay")
        self.assertEqual(verb_stem("buys"), "buy")

    def test_verb_stem_ends_in_y_preceded_by_a_vowel_and_has_at_least_three_letters(self):
        self.assertEqual(verb_stem("flies"), "fly")
        self.assertEqual(verb_stem("tries"), "try")
        self.assertEqual(verb_stem("unifies"), "unify")

    def test_verb_stem_form_Xie(self):
        self.assertEqual(verb_stem("dies"), "die")
        self.assertEqual(verb_stem("lies"), "lie")
        self.assertEqual(verb_stem("ties"), "tie")
        self.assertNotEqual(verb_stem("unties"), "untie")

    def test_verb_stem_ends_in_o_x_ch_sh_ss_zz(self):
        self.assertEqual(verb_stem("goes"), "go")
        self.assertEqual(verb_stem("boxes"), "box")
        self.assertEqual(verb_stem("attaches"), "attach")
        self.assertEqual(verb_stem("washes"), "wash")
        self.assertEqual(verb_stem("dresses"), "dress")
        self.assertEqual(verb_stem("fizzes"), "fizz")

    def test_verb_stem_ends_in_se_ze_but_not_sse_zze(self):
        self.assertEqual(verb_stem("loses"), "lose")
        self.assertEqual(verb_stem("dazes"), "daze")
        self.assertEqual(verb_stem("lapses"), "lapse")
        self.assertEqual(verb_stem("analyses"), "analyse")
        self.assertEqual(verb_stem("analyzes"), "analyze")

    def test_verb_stem_ends_in_e_not_preceded_by_i_o_s_x_z_ch_sh(self):
        self.assertEqual(verb_stem("likes"), "like")
        self.assertEqual(verb_stem("hates"), "hate")
        self.assertEqual(verb_stem("bathes"), "bathe")



if __name__ == '__main__':
    unittest.main()
