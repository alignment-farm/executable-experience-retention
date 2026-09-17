def solve(api, request):
    customers = set(request.get("customers", []))
    cutoff = request.get("cutoff", "")
    
    # Fetch all invoices
    invoices = []
    cursor = None
    while True:
        page = api.page("invoices", cursor)
        invoices.extend(page["items"])
        cursor = page.get("next_cursor")
        if cursor is None:
            break
    
    # Fetch all events
    events = []
    cursor = None
    while True:
        page = api.page("events", cursor)
        events.extend(page["items"])
        cursor = page.get("next_cursor")
        if cursor is None:
            break
    
    # Deduplicate events: for each event ID, keep only the highest revision
    # If multiple events have the same ID and same highest revision, count once
    best_by_id = {}
    for ev in events:
        eid = ev["id"]
        rev = ev["revision"]
        if eid not in best_by_id or rev > best_by_id[eid]["revision"]:
            best_by_id[eid] = ev
        elif rev == best_by_id[eid]["revision"]:
            # Identical duplicates; keep one (they're identical per problem statement)
            pass
    
    # Now filter: only posted, date <= cutoff
    valid_events = []
    for eid, ev in best_by_id.items():
        if ev["status"] == "posted" and ev["date"] <= cutoff:
            valid_events.append(ev)
    
    # Build invoice lookup
    invoice_map = {}
    for inv in invoices:
        invoice_map[inv["id"]] = inv
    
    # Select open invoices for requested customers with due <= cutoff
    selected_invoices = []
    for inv in invoices:
        if inv["status"] == "open" and inv["customer"] in customers and inv["due"] <= cutoff:
            selected_invoices.append(inv)
    
    # Helper: convert decimal string to integer cents
    def to_cents(amount_str):
        # amount_str is like "123.45"
        if "." in amount_str:
            whole, frac = amount_str.split(".")
            # frac should be exactly 2 digits
            return int(whole) * 100 + int(frac)
        else:
            return int(amount_str) * 100
    
    # For each selected invoice, compute outstanding balance
    rows = []
    for inv in selected_invoices:
        inv_id = inv["id"]
        inv_currency = inv["currency"]
        balance = to_cents(inv["amount"])
        
        # Apply valid events for this invoice
        for ev in valid_events:
            if ev["invoice_id"] != inv_id:
                continue
            if ev["currency"] != inv_currency:
                continue
            amt = to_cents(ev["amount"])
            if ev["kind"] == "payment":
                balance -= amt
            elif ev["kind"] == "refund":
                balance += amt
        
        # Clamp to zero
        if balance < 0:
            balance = 0
        
        # Include only positive balances
        if balance > 0:
            rows.append({
                "invoice_id": inv_id,
                "customer": inv["customer"],
                "currency": inv_currency,
                "outstanding_cents": balance
            })
    
    # Sort rows by (customer, currency, invoice_id)
    rows.sort(key=lambda r: (r["customer"], r["currency"], r["invoice_id"]))
    
    # Compute totals
    totals = {}
    for r in rows:
        cur = r["currency"]
        totals[cur] = totals.get(cur, 0) + r["outstanding_cents"]
    
    return {"rows": rows, "totals": totals}
