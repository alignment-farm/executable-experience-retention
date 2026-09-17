"""Original deterministic synthetic invoice reconciliation workload."""
import random
from decimal import Decimal

CONTRACT = '''Implement solve(api, request) returning a JSON-compatible dict.
request = {customers: list[str], cutoff: YYYY-MM-DD}. API: api.page(resource, cursor=None)
returns {items: list[dict], next_cursor: str|null}; resources are "invoices" and "events".
Fetch all pages until next_cursor is None (do not rely on page length). No mutations.
Invoices have id, customer, currency, amount (nonnegative decimal string with exactly
2 decimal places), due (ISO date), status (open|void). Invoice IDs are unique.
Events have id, revision (integer), invoice_id, currency, amount (nonnegative two-place
decimal string), kind (payment|refund), status (posted|pending), date (ISO date).
Repeated event IDs are versions: FIRST select highest revision globally, BEFORE any
other event filtering. Identical duplicates of the highest revision may occur; count
once. Ties are identical. Events referencing missing invoices can occur.
Only latest events with status posted and date <= cutoff count. Payments reduce
balance; refunds increase it. Ignore events with currency different from invoice.
Select open invoices for requested customers with due <= cutoff. Start balance at
invoice amount, subtract counted payments, add counted refunds; clamp each balance
to zero. Include only positive balances. Use exact integer cents, never round float.
Return {rows: [{invoice_id, customer, currency, outstanding_cents}], totals: {currency:
summed positive outstanding cents}}. Sort rows by (customer, currency, invoice_id).
Totals omit currencies without positive balances. Empty input/selection => empty rows
and totals. Do not print. The function must generalize to unseen datasets and request
values; use only Python standard library. All current data is available via the API.'''

def fixture(seed, n=None):
    rng = random.Random(seed)
    n = n if n is not None else rng.choice([0, 9, 17, 31, 52])
    money = lambda cents: f'{cents//100}.{cents%100:02d}'
    invoices=[]; events=[]
    for i in range(n):
        invoice = dict(id=f'i{i:03}',customer=rng.choice(['alfa','beta','gamma']),
                       currency=rng.choice(['USD','EUR','GBP']), amount=money(rng.randrange(0,20001)),
                       due=f'2026-09-{rng.randint(1,28):02}', status=rng.choice(['open']*4+['void']))
        invoices.append(invoice)
        for j in range(rng.randrange(5)):
            event = dict(id=f'e{i:03}-{j}',revision=1,invoice_id=invoice['id'],
                         currency=rng.choice([invoice['currency']]*5+['JPY']),
                         amount=money(rng.randrange(0,15001)),kind=rng.choice(['payment']*3+['refund']),
                         status=rng.choice(['posted']*3+['pending']),date=f'2026-09-{rng.randint(1,28):02}')
            events.append(event)
            if rng.random()<.5:
                revised={**event,'revision':2,'status':rng.choice(['posted','pending']),
                         'date':f'2026-09-{rng.randint(1,28):02}', 'amount':money(rng.randrange(15001))}
                events.extend([revised,dict(revised)])
    # Every nonempty dataset includes adversarial latest-revision/filter-order and cents cases.
    if n:
        invoices.append(dict(id='edge',customer='alfa',currency='USD',amount='0.30',due='2026-09-01',status='open'))
        events.extend([
            dict(id='edgepay',revision=1,invoice_id='edge',currency='USD',amount='0.10',kind='payment',status='posted',date='2026-09-01'),
            dict(id='edgepay',revision=2,invoice_id='edge',currency='USD',amount='0.20',kind='payment',status='pending',date='2026-09-01'),
            dict(id='orphan',revision=1,invoice_id='absent',currency='USD',amount='2.00',kind='refund',status='posted',date='2026-09-01')])
    rng.shuffle(invoices); rng.shuffle(events)
    return dict(seed=seed, data={'invoices':invoices,'events':events},
                request={'customers':rng.choice([['alfa'],['alfa','beta'],['alfa','beta','gamma'],[]]),
                         'cutoff':f'2026-09-{rng.choice([7,15,22,28]):02}'}, page_size=rng.choice([1,3,7]))

def oracle(case):
    """Declarative reference, independent of acquired code."""
    data=case['data']; req=case['request']; rows=[]
    latest={e['id']:max(x['revision'] for x in data['events'] if x['id']==e['id']) for e in data['events']}
    selected={e['id']:e for e in data['events'] if e['revision']==latest[e['id']]}
    for inv in data['invoices']:
        if not (inv['status']=='open' and inv['customer'] in req['customers'] and inv['due']<=req['cutoff']): continue
        effects=[Decimal(e['amount'])*(1 if e['kind']=='refund' else -1) for e in selected.values()
                 if e['invoice_id']==inv['id'] and e['currency']==inv['currency'] and e['status']=='posted' and e['date']<=req['cutoff']]
        cents=int(max(Decimal(0), Decimal(inv['amount'])+sum(effects))*100)
        if cents: rows.append(dict(invoice_id=inv['id'],customer=inv['customer'],currency=inv['currency'],outstanding_cents=cents))
    rows.sort(key=lambda x:(x['customer'],x['currency'],x['invoice_id']))
    return {'rows':rows,'totals':{c:sum(x['outstanding_cents'] for x in rows if x['currency']==c) for c in sorted({x['currency'] for x in rows})}}

def dev_cases():
    cases=[fixture(101,3),fixture(102,4),fixture(103,0),fixture(104,5),fixture(105,2)]
    for c in cases: c['request']['customers']=['alfa','beta','gamma']
    return cases
