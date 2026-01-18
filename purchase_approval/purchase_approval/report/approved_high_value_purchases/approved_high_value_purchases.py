# Copyright (c) 2026, Krushna Chandra Sahu and Krushnachsahu089@gmail
# For license information, please see license.txt
import frappe
from frappe import _

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    """Define report columns"""
    return [
        {
            "fieldname": "name",
            "label": _("PAR Name"),
            "fieldtype": "Link",
            "options": "Purchase Approval Request",
            "width": 150
        },
        {
            "fieldname": "requester",
            "label": _("Requester"),
            "fieldtype": "Link",
            "options": "User",
            "width": 180
        },
        {
            "fieldname": "total_amount",
            "label": _("Total Amount"),
            "fieldtype": "Currency",
            "width": 150
        },
        {
            "fieldname": "approved_by",
            "label": _("Approved By"),
            "fieldtype": "Link",
            "options": "User",
            "width": 180
        },
        {
            "fieldname": "approved_date",
            "label": _("Approved Date"),
            "fieldtype": "Datetime",
            "width": 180
        }
    ]

def get_data(filters):
    """Fetch data using SQL query"""
    conditions = ["status = 'Approved'"]
    
    # Add minimum amount filter
    if filters and filters.get("minimum_amount"):
        conditions.append(f"total_amount >= {frappe.db.escape(filters.get('minimum_amount'))}")
    
    where_clause = " AND ".join(conditions)
    
    query = f"""
        SELECT
            name,
            requester,
            total_amount,
            approved_by,
            approved_date
        FROM
            `tabPurchase Approval Request`
        WHERE
            {where_clause}
        ORDER BY
            approved_date DESC
    """
    
    data = frappe.db.sql(query, as_dict=1)
    return data