SELECT po_id,SUM(quantity_received) AS total quantity received
FROM grn_items
WHERE po_id='PO-2024-001'
GROUP BY po_id;