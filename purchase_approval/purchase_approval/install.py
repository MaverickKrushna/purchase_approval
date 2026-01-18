import frappe
from frappe import _

def after_install():
    """Create dummy data after installation"""
    print("Setting up Purchase Approval app...")
    
    # Create dummy Purchase Approval Requests
    create_dummy_data()
    
    print("Purchase Approval app installed successfully!")

def create_dummy_data():
    """Create dummy Purchase Approval Request records"""
    
    # Check if dummy data already exists
    if frappe.db.exists("Purchase Approval Request", "PAR-0001"):
        print("Dummy data already exists, skipping...")
        return
    
    dummy_records = [
        {
            "doctype": "Purchase Approval Request",
            "requester": "Administrator",
            "total_amount": 50000,
            "priority": "Low",
            "justification": "Regular office supplies for Q1",
            "status": "Draft"
        },
        {
            "doctype": "Purchase Approval Request",
            "requester": "Administrator",
            "total_amount": 150000,
            "priority": "High",
            "justification": "New server equipment for data center expansion",
            "status": "Approved",
            "approved_by": "Administrator",
            "approved_date": "2024-01-10 14:30:00"
        },
        {
            "doctype": "Purchase Approval Request",
            "requester": "Administrator",
            "total_amount": 250000,
            "priority": "High",
            "justification": "Software licenses for entire development team",
            "status": "Approved",
            "approved_by": "Administrator",
            "approved_date": "2024-01-12 10:15:00"
        },
        {
            "doctype": "Purchase Approval Request",
            "requester": "Administrator",
            "total_amount": 75000,
            "priority": "Low",
            "justification": "Marketing materials for upcoming campaign",
            "status": "Draft"
        },
        {
            "doctype": "Purchase Approval Request",
            "requester": "Administrator",
            "total_amount": 180000,
            "priority": "High",
            "justification": "Cloud infrastructure upgrade for better performance",
            "status": "Approved",
            "approved_by": "Administrator",
            "approved_date": "2024-01-14 16:45:00"
        }
    ]
    
    for record in dummy_records:
        try:
            doc = frappe.get_doc(record)
            doc.insert(ignore_permissions=True)
            print(f"Created: {doc.name}")
        except Exception as e:
            print(f"Error creating dummy record: {str(e)}")
    
    frappe.db.commit()
    print(f"Created {len(dummy_records)} dummy Purchase Approval Request records")