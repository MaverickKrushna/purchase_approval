// Copyright (c) 2026, Krushna Chandra Sahu and Krushnachsahu089@gmail
// For license information, please see license.txt

frappe.query_reports["Approved High-Value Purchases"] = {
    "filters": [
        {
            "fieldname": "minimum_amount",
            "label": __("Minimum Amount"),
            "fieldtype": "Currency",
            "default": 0
        }
    ]
};