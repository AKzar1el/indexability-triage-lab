import unittest
from itertools import product
from dataclasses import replace
from triage import CASES, assess, Case

class TestTriage(unittest.TestCase):
    def test_reference_cases(self):
        expected = ['Technical candidate', 'Crawl blocked', 'Noindex observed', 'Canonical review needed', 'Redirect: inspect destination', 'Client error', 'Temporary availability issue', 'Temporary availability issue', 'Content review needed', 'Evidence missing']
        for c, e in zip(CASES, expected):
            with self.subTest(case=c.name): self.assertEqual(assess(c).state, e)
    def test_blocked_noindex_not_confirmed(self):
        self.assertEqual(assess(replace(CASES[0], crawl='Blocked', directive='Noindex')).state, 'Crawl blocked')
    def test_canonical_not_overriding_noindex(self):
        self.assertEqual(assess(replace(CASES[0], canonical='Other', directive='Noindex')).state, 'Noindex observed')
    def test_unknown_directive(self):
        self.assertEqual(assess(replace(CASES[0], directive='Unknown')).state, 'Evidence missing')
    def test_unknown_canonical(self):
        self.assertEqual(assess(replace(CASES[0], canonical='Unknown')).state, 'Evidence missing')
    def test_unknown_content(self):
        self.assertEqual(assess(replace(CASES[0], content='Unknown')).state, 'Evidence missing')
    def test_204_not_ordinary_200(self):
        self.assertEqual(assess(replace(CASES[0], status=204)).state, 'Other HTTP response')
    def test_candidate_invariant(self):
        count = 0
        for status, crawl, directive, canonical, content in product([None,200,204,301,302,401,403,404,410,429,500,503], ['Allowed','Blocked','Unknown'], ['Absent','Noindex','Unknown'], ['Self','Other','Unknown'], ['Substantive','Thin or error-like','Unknown']):
            c = Case('combination', status,crawl,directive,canonical,content)
            f = assess(c)
            self.assertTrue(f.explanation and f.next_step)
            self.assertEqual(f.state == 'Technical candidate', (status,crawl,directive,canonical,content)==(200,'Allowed','Absent','Self','Substantive'))
            count += 1
        self.assertEqual(count, 972)

if __name__ == '__main__': unittest.main()
