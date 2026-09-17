import unittest
from workload import oracle, dev_cases, fixture
from experiment import execute, check

class HarnessTests(unittest.TestCase):
    def test_reference_known_answer_and_latest_before_filter(self):
        invoice=dict(id='a',customer='x',currency='USD',amount='0.30',due='2026-01-01',status='open')
        base=dict(id='p',revision=1,invoice_id='a',currency='USD',amount='0.10',kind='payment',status='posted',date='2026-01-01')
        case=dict(data={'invoices':[invoice],'events':[base,dict(base)]},request={'customers':['x'],'cutoff':'2026-01-02'})
        self.assertEqual(oracle(case),{'rows':[dict(invoice_id='a',customer='x',currency='USD',outstanding_cents=20)],'totals':{'USD':20}})
        case['data']['events'].append({**base,'revision':2,'status':'pending'})
        self.assertEqual(oracle(case)['totals'],{'USD':30})
        case['data']['events'].append({**base,'revision':3,'date':'2026-01-03'})
        self.assertEqual(oracle(case)['totals'],{'USD':30})
        case['data']['events'].append({**base,'revision':4,'amount':'1.00'})
        self.assertEqual(oracle(case),{'rows':[],'totals':{}})
    def test_container_calls_and_failure_detection(self):
        source='def solve(api, request):\n    api.page("invoices")\n    return {"rows":[],"totals":{}}\n'
        batch=execute(source,dev_cases())
        self.assertEqual(len(batch['results']),5)
        self.assertTrue(check(batch,dev_cases()))
        self.assertEqual(len(batch['results'][0]['api_calls']),1)
    def test_oracle_order_invariant(self):
        c=fixture(104,20);expected=oracle(c)
        c['data']['invoices'].reverse();c['data']['events'].reverse()
        self.assertEqual(oracle(c),expected)

if __name__=='__main__':unittest.main()
