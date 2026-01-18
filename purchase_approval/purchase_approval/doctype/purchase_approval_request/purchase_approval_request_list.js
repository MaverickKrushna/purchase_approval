// Copyright (c) 2026, Krushna Chandra Sahu and Krushnachsahu089@gmail
// For license information, please see license.txt

frappe.listview_settings['Purchase Approval Request'] = {
    get_indicator: function(doc) {
        if (doc.status === 'Approved') {
            return [__('Approved'), 'green', 'status,=,Approved'];
        } else {
            return [__('Draft'), 'gray', 'status,=,Draft'];
        }
    }
};