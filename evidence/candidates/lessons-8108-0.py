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
    
    # Deduplicate events: for each event ID, keep the one with highest revision
    # If multiple have same highest revision, they are identical; keep one
    best_by_id = {}
    for ev in events:
        eid = ev["id"]
        rev = ev["revision"]
        if eid not in best_by_id:
            best_by_id[eid] = ev
        else:
            existing = best_by_id[eid]
            if rev > existing["revision"]:
                best_by_id[eid] = ev
            # If rev == existing["revision"], they are identical duplicates; keep existing
    
    deduped_events = list(best_by_id.values())
    
    # Filter events: status == "posted" and date <= cutoff
    filtered_events = []
    for ev in deduped_events:
        if ev["status"] == "posted" and ev["date"] <= cutoff:
            filtered_events.append(ev)
    
    # Build set of valid invoice IDs
    invoice_ids = set(inv["id"] for inv in invoices)
    
    # Filter events to only those referencing existing invoices
    valid_events = [ev for ev in filtered_events if ev["invoice_id"] in invoice_ids]
    
    # Select invoices: status == "open", customer in customers, due <= cutoff
    selected_invoices = []
    for inv in invoices:
        if inv["status"] == "open" and inv["customer"] in customers and inv["due"] <= cutoff:
            selected_invoices.append(inv)
    
    # Helper to convert decimal string to integer cents
    def to_cents(amount_str):
        # amount_str is like "123.45"
        if "." in amount_str:
            whole, frac = amount_str.split(".")
            # Ensure frac is exactly 2 digits
            frac = frac[:2].ljust(2, "0")
            return int(whole) * 100 + int(frac)
        else:
            return int(amount_str) * 100
    
    # Calculate balances
    rows = []
    for inv in selected_invoices:
        inv_id = inv["id"]
        inv_currency = inv["currency"]
        balance = to_cents(inv["amount"])
        
        for ev in valid_events:
            if ev["invoice_id"] != inv_id:
                continue
            if ev["currency"] != inv_currency:
                continue
            ev_cents = to_cents(ev["amount"])
            if ev["kind"] == "payment":
                balance -= ev_cents
            elif ev["kind"] == "refund":
                balance += ev_cents
        
        # Clamp to zero
        if balance < 0:
            balance = 0
        
        # Include only if positive
        if balance > 0:
            rows.append({
                "invoice_id": inv_id,
                "customer": inv["customer"],
                "currency": inv_currency,
                "outstanding_cents": balance
            })
    
    # Sort rows by (customer, currency, invoice_id)
    rows.sort(key=lambda r: (r["customer"], r["currency"], r["invoice_id"]))
    
    # Calculate totals
    totals = {}
    for row in rows:
        cur = row["currency"]
        totals[cur] = totals.get(cur, 0) + row["outstanding_cents"]
    
    return {"rows": rows, "totals": totals}
