import unittest
from point_math import score_m1,score_m2,score_m5,score_m8,score_m11
class PointMathTests(unittest.TestCase):
    def test_same_source_band_not_interval(self):
        self.assertEqual(score_m5([3,4]),3);self.assertIsNone(score_m5([4,5]));self.assertEqual(score_m5([6,7,9]),5)
    def test_no_silent_deletion_of_unknown_document(self):
        docs=[{'id':'a','status':'scored','score':4},{'id':'b','status':'needs_review','score':None}]
        self.assertIsNone(score_m2(docs,source_inventory_resolved=True))
        docs[1].update(status='scored',score=5)
        self.assertEqual(score_m2(docs,source_inventory_resolved=True),4.5)
        self.assertIsNone(score_m2(docs))
    def test_first_hit_and_missing_history(self):
        self.assertIsNone(score_m1(2,1));self.assertEqual(score_m1(2,1,decisive_records_verified=True),3)
        self.assertIsNone(score_m1(decisive_records_verified=True));self.assertEqual(score_m1(decisive_records_verified=True,budget_exhausted=True),1)
        with self.assertRaises(ValueError):score_m1(1,6,decisive_records_verified=True)
    def test_no_zero_call_reward(self):
        self.assertIsNone(score_m8(0,0,valid_complete_run=True));self.assertEqual(score_m8(4,8,valid_complete_run=True),1)
    def test_formula_and_missing_saturation(self):
        metrics={f'M{i}':{'status':'scored','score':5} for i in range(1,11)}
        self.assertAlmostEqual(score_m11(metrics)['score'],100)
        metrics['M6']={'status':'unscorable','score':None}
        self.assertEqual(score_m11(metrics)['status'],'unscorable')
        self.assertIsNone(score_m11(metrics)['score'])
    def test_exceptions_need_explicit_basis(self):
        metrics={f'M{i}':{'status':'scored','score':5} for i in range(1,9)}
        metrics['M4']={'status':'not_applicable','score':None}
        self.assertIsNone(score_m11(metrics)['score']);self.assertEqual(score_m11(metrics,m4_not_applicable=True)['score'],100)
        metrics['M6']={'status':'not_applicable','score':None}
        with self.assertRaises(ValueError):score_m11(metrics,confirmed_unavailable={'third_party':{'status':'confirmed_unavailable'}},m4_not_applicable=True)
        self.assertEqual(score_m11(metrics,confirmed_unavailable={'third_party':{'status':'confirmed_unavailable','reason':'adjudicated absence','evidence':['run-event']}},m4_not_applicable=True)['score'],100)
    def test_outcomes_do_not_enter_m11(self):
        metrics={f'M{i}':{'status':'scored','score':3} for i in range(1,9)}
        # Independent hand calculation: OFF=.216, SEC=.36, OWN=.6, K=.799296.
        self.assertAlmostEqual(score_m11(metrics)['score'],100*.799296*.88*.96)
        metrics['M9']={'status':'unscorable','score':None};self.assertEqual(score_m11(metrics)['status'],'scored')
if __name__=='__main__':unittest.main()
