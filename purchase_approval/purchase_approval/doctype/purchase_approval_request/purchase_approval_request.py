# Copyright (c) 2026, Krushna Chandra Sahu and Krushnachsahu089@gmail
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _

class PurchaseApprovalRequest(Document):
    def validate(self):
        """Validation before saving"""
        # Check if justification is required and provided
        if self.total_amount and self.total_amount > 100000:
            if not self.justification or not self.justification.strip():
                frappe.throw(_("Justification is mandatory for amounts greater than 100,000"))
    
    def before_save(self):
        """Block editing after approval"""
        if self.has_value_changed("status") and self.status == "Approved":
            return  # Allow status change to Approved
        
        # Check if document was already approved
        if self.get_doc_before_save():
            old_status = self.get_doc_before_save().status
            if old_status == "Approved" and not self.has_value_changed("status"):
                frappe.throw(_("Cannot edit an approved Purchase Approval Request"))

    @frappe.whitelist()
    def approve_request(self):
        """Server method to approve the request"""
        # Check permission
        if not frappe.has_permission("Purchase Approval Request", "write", self.name):
            frappe.throw(_("You don't have permission to approve this request"))
        
        # Check if user has Purchase Manager role
        if "Purchase Manager" not in frappe.get_roles(frappe.session.user):
            frappe.throw(_("Only Purchase Managers can approve requests"))
        
        # Validate justification requirement
        if self.total_amount > 100000:
            if not self.justification or not self.justification.strip():
                frappe.throw(_("Justification is required for amounts greater than 100,000"))
        
        # Approve the request
        self.status = "Approved"
        self.approved_by = frappe.session.user
        self.approved_date = frappe.utils.now()
        self.save()
        
        frappe.msgprint(_("Purchase Approval Request has been approved successfully"))
        
        return self.name


def has_permission(doc, ptype, user):
    """Custom permission query"""
    if not doc:
        return True
    
    # Purchase Managers can see all records
    if "Purchase Manager" in frappe.get_roles(user):
        return True
    
    # Users can see their own records
    if doc.requester == user:
        return True
    
    # Check if user is assigned to this document
    assignments = frappe.get_all(
        "_Assignment",
        filters={
            "reference_type": "Purchase Approval Request",
            "reference_name": doc.name,
            "allocated_to": user
        }
    )
    
    if assignments:
        return True
    
    return False


def get_permission_query_conditions(user):
    """Return SQL conditions for list view filtering"""
    if not user:
        user = frappe.session.user
    
    # Purchase Managers can see all records
    if "Purchase Manager" in frappe.get_roles(user):
        return None
    
    # Build conditions for own records and assigned records
    return f"""(
        `tabPurchase Approval Request`.requester = {frappe.db.escape(user)}
        OR `tabPurchase Approval Request`.name IN (
            SELECT reference_name 
            FROM `tab_Assignment` 
            WHERE reference_type = 'Purchase Approval Request' 
            AND allocated_to = {frappe.db.escape(user)}
        )
    )"""