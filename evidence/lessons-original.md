To implement `solve(api, request)` correctly, follow these procedural steps:

1.  **Fetch Data**: Retrieve all items from the "invoices" and "events" resources by calling `api.page(resource, cursor)` in a loop. Continue fetching until `next_cursor` is `None`. Do not assume page size or item count.

2.  **Deduplicate Events**: Process the fetched events to resolve versioning. For each unique event ID, identify the entry with the highest `revision` integer. If multiple entries share the same ID and the highest revision, they are identical duplicates; retain only one instance. This deduplication must occur before any other filtering.

3.  **Filter Events**: From the deduplicated events, select only those where `status` is "posted" and `date` is less than or equal to the `cutoff` date provided in the request. Ignore events referencing invoice IDs that do not exist in the invoice list.

4.  **Select Invoices**: Filter the fetched invoices to include only those where `status` is "open", `customer` is in the `customers` list from the request, and `due` date is less than or equal to the `cutoff`.

5.  **Calculate Balances**: For each selected invoice:
    *   Initialize the balance using the invoice's `amount`. Convert the decimal string to integer cents to avoid floating-point errors (e.g., "123.45" becomes 12345).
    *   Iterate through the filtered events. For each event matching the invoice ID:
        *   Skip the event if its `currency` does not match the invoice's `currency`.
        *   If the event `kind` is "payment", subtract the event's amount (in cents) from the balance.
        *   If the event `kind` is "refund", add the event's amount (in cents) to the balance.
    *   Clamp the final balance to zero if it is negative.
    *   Include the invoice in the results only if the final balance is strictly positive.

6.  **Format Output**:
    *   Construct a list of row dictionaries containing `invoice_id`, `customer`, `currency`, and `outstanding_cents`.
    *   Sort the rows by `customer`, then `currency`, then `invoice_id`.
    *   Calculate `totals` by summing `outstanding_cents` for each currency present in the rows. Omit currencies with no positive balances.
    *   Return a dictionary with keys `rows` and `totals`.

7.  **Edge Cases**:
    *   If no invoices or events are fetched, or if no invoices meet the selection criteria, return empty lists and an empty totals dictionary.
    *   Ensure exact integer arithmetic for all monetary calculations.
    *   Handle orphaned events (referencing missing invoices) by ignoring them during balance calculation.