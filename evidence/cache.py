def solve(api, request):
    customers = set(request["customers"])
    cutoff = request["cutoff"]

    def fetch_all(resource):
        items = []
        cursor = None
        while True:
            page = api.page(resource, cursor)
            items.extend(page["items"])
            cursor = page.get("next_cursor")
            if cursor is None:
                break
        return items

    invoices = fetch_all("invoices")
    events = fetch_all("events")

    # Deduplicate events: for each event id, keep highest revision; identical duplicates count once
    best = {}
    for ev in events:
        eid = ev["id"]
        rev = ev["revision"]
        if eid not in best:
            best[eid] = ev
        else:
            cur = best[eid]
            if rev > cur["revision"]:
                best[eid] = ev
            elif rev == cur["revision"]:
                # identical duplicates; keep one (they are identical per spec)
                pass
    deduped = list(best.values())

    # Filter events: posted, date <= cutoff
    filtered_events = []
    for ev in deduped:
        if ev["status"] != "posted":
            continue
        if ev["date"] > cutoff:
            continue
        filtered_events.append(ev)

    # Build set of valid invoice ids
    invoice_ids = set(inv["id"] for inv in invoices)

    # Select invoices: open, customer in customers, due <= cutoff
    selected = []
    for inv in invoices:
        if inv["status"] != "open":
            continue
        if inv["customer"] not in customers:
            continue
        if inv["due"] > cutoff:
            continue
        selected.append(inv)

    def to_cents(amount_str):
        # amount_str is like "123.45"
        parts = amount_str.split(".")
        whole = int(parts[0])
        frac = int(parts[1]) if len(parts) > 1 else 0
        return whole * 100 + frac

    # Group filtered events by invoice_id
    events_by_invoice = {}
    for ev in filtered_events:
        iid = ev["invoice_id"]
        if iid not in invoice_ids:
            continue
        if iid not in events_by_invoice:
            events_by_invoice[iid] = []
        events_by_invoice[iid].append(ev)

    rows = []
    for inv in selected:
        iid = inv["id"]
        currency = inv["currency"]
        balance = to_cents(inv["amount"])
        for ev in events_by_invoice.get(iid, []):
            if ev["currency"] != currency:
                continue
            amt = to_cents(ev["amount"])
            if ev["kind"] == "payment":
                balance -= amt
            elif ev["kind"] == "refund":
                balance += amt
        if balance < 0:
            balance = 0
        if balance > 0:
            rows.append({
                "invoice_id": iid,
                "customer": inv["customer"],
                "currency": currency,
                "outstanding_cents": balance
            })

    rows.sort(key=lambda r: (r["customer"], r["currency"], r["invoice_id"]))

    totals = {}
    for r in rows:
        cur = r["currency"]
        totals[cur] = totals.get(cur, 0) + r["outstanding_cents"]

    return {"rows": rows, "totals": totals}
