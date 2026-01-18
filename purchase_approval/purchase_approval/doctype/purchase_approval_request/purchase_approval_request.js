// Copyright (c) 2026, Krushna Chandra Sahu and Krushnachsahu089@gmail
// For license information, please see license.txt


frappe.ui.form.on('Purchase Approval Request', {
    refresh: function(frm) {
        // Make justification mandatory
        frm.set_df_property('justification', 'reqd', 1);
        
        // Disable all fields if status is Approved
        if (frm.doc.status === 'Approved') {
            frm.disable_form();
        }
        
        // Add Approve button for Purchase Managers
        if (frm.doc.status !== 'Approved' && !frm.is_new()) {
            // Check if user has Purchase Manager role
            if (frappe.user_roles.includes('Purchase Manager')) {
                frm.add_custom_button(__('Approve'), function() {
                    frappe.call({
                        method: 'approve_request',
                        doc: frm.doc,
                        callback: function(r) {
                            if (!r.exc) {
                                frm.reload_doc();
                            }
                        }
                    });
                }).addClass('btn-primary');
            }
        }
    },
    
    total_amount: function(frm) {
        // Auto-set Priority to High if Total Amount > 100,000
        if (frm.doc.total_amount > 100000) {
            frm.set_value('priority', 'High');
        }
    },
    
    material_request: function(frm) {
        if (frm.doc.material_request) {
            // Fetch total amount from Material Request items
            frappe.call({
                method: 'frappe.client.get',
                args: {
                    doctype: 'Material Request',
                    name: frm.doc.material_request
                },
                callback: function(r) {
                    if (r.message) {
                        let material_request = r.message;
                        let total = 0;
                        let item_count = 0;
                        
                        // Calculate total amount from items
                        if (material_request.items) {
                            material_request.items.forEach(function(item) {
                                total += (item.amount || 0);
                                item_count++;
                            });
                        }
                        
                        // Set total amount
                        frm.set_value('total_amount', total);
                        
                        // If more than 5 items, set Priority to High
                        if (item_count > 5) {
                            frm.set_value('priority', 'High');
                        }
                    }
                }
            });
        }
    },
    
    before_save: function(frm) {
        // Ensure justification is provided when required
        if (frm.doc.total_amount > 100000) {
            if (!frm.doc.justification || !frm.doc.justification.trim()) {
                frappe.throw(__('Justification is mandatory for amounts greater than 100,000'));
            }
        }
    }
});