# Purchase Approval - ERPNext Custom App

A custom Frappe/ERPNext application for managing high-value purchase approval requests with role-based permissions and automated workflows.

## Features

### 1. Purchase Approval Request DocType
- **Fields**: Requester, Material Request, Total Amount, Priority, Justification, Status, Approved By, Approved Date
- **Automated Priority Setting**: Automatically sets priority to "High" when:
  - Total Amount > 100,000
  - Material Request has more than 5 items
- **Status Management**: Draft → Approved workflow
- **Read-only Fields**: Approved By and Approved Date are auto-populated on approval

### 2. Client-Side Automation (JavaScript)
- Auto-set Priority to High for amounts > 100,000
- Mandatory Justification field
- Fetch total amount from linked Material Request items
- Auto-set Priority to High if Material Request has > 5 items
- Disable all fields once Status = Approved
- Approve button visible only to Purchase Managers

### 3. Server-Side Validation (Python)
- Prevent approval if Justification is empty when Total Amount > 100,000
- Block approval via API without proper permissions
- Block editing after approval
- Role-based approval restrictions

### 4. Role-Based Permissions
- **Users**: Can see only their own records or records they're assigned to
- **Purchase Managers**: Can see all records and approve requests
- Custom permission query implementation

### 5. SQL Report
**"Approved High-Value Purchases"** displays:
- PAR Name
- Requester
- Total Amount
- Approved By
- Approved Date
- Filter by Minimum Amount

### 6. Dummy Data
Automatically creates 5 sample Purchase Approval Request records on installation

## Requirements

- Frappe Framework (v14 or v15)
- ERPNext (v14 or v15)
- Python 3.10+
- MariaDB/MySQL

## Installation

### Method 1: Fresh Installation

```bash
# Navigate to your Frappe bench
cd ~/frappe-bench

# Get the app from GitHub
bench get-app https://github.com/yourusername/purchase_approval.git

# Install on your site
bench --site your-site.local install-app purchase_approval

# Migrate
bench --site your-site.local migrate

# Clear cache
bench --site your-site.local clear-cache

# Restart bench
bench restart
```

### Method 2: Manual Installation

```bash
# Navigate to apps directory
cd ~/frappe-bench/apps

# Clone the repository
git clone https://github.com/yourusername/purchase_approval.git

# Navigate to bench root
cd ~/frappe-bench

# Install the app
bench --site your-site.local install-app purchase_approval

# Migrate
bench --site your-site.local migrate

# Clear cache and restart
bench --site your-site.local clear-cache
bench restart
```

## Post-Installation Setup

### 1. Verify Installation
After installation, the app automatically:
- Creates the Purchase Approval Request DocType
- Sets up permissions
- Creates the SQL report
- Generates 5 dummy records

### 2. Role Setup
Ensure users have appropriate roles:

**For Purchase Managers:**
- Assign "Purchase Manager" role to users who should approve requests

**For Regular Users:**
- Assign "Purchase User" role for creating requests

```bash
# Assign roles via bench console
bench --site your-site.local console

# In Python console:
user = frappe.get_doc("User", "user@example.com")
user.add_roles("Purchase Manager")  # or "Purchase User"
user.save()
```

### 3. Access the Features

**Create a Purchase Approval Request:**
1. Go to: Purchase Approval → Purchase Approval Request → New
2. Fill in the required fields
3. Link to a Material Request (optional)
4. Save

**Approve a Request:**
1. Open an existing Purchase Approval Request
2. Click the "Approve" button (visible only to Purchase Managers)
3. The system validates and updates the approval details

**View Report:**
1. Go to: Reports → Approved High-Value Purchases
2. Set minimum amount filter
3. View and export results

## Testing the Features

### Test Auto-Priority Setting
```javascript
// Create a PAR with amount > 100,000
// Priority should automatically be set to "High"
```

### Test Justification Validation
```javascript
// Try to save a PAR with amount > 100,000 without justification
// Should show error: "Justification is mandatory for amounts greater than 100,000"
```

### Test Material Request Integration
```javascript
// Select a Material Request with items
// Total Amount should auto-calculate from item amounts
// If > 5 items, Priority should be set to "High"
```

### Test Approval Workflow
```javascript
// As Purchase Manager, click "Approve" button
// Status changes to "Approved"
// All fields become read-only
// Approved By and Approved Date are populated
```

### Test Permission Query
```javascript
// As regular user, create a PAR
// You should only see your own records
// As Purchase Manager, you should see all records
```

## File Structure

```
purchase_approval/
├── purchase_approval/
│   ├── purchase_approval/
│   │   ├── doctype/
│   │   │   └── purchase_approval_request/
│   │   │       ├── purchase_approval_request.json
│   │   │       ├── purchase_approval_request.py
│   │   │       ├── purchase_approval_request.js
│   │   │       └── purchase_approval_request_list.js
│   │   ├── report/
│   │   │   └── approved_high_value_purchases/
│   │   │       ├── approved_high_value_purchases.json
│   │   │       ├── approved_high_value_purchases.py
│   │   │       └── approved_high_value_purchases.js
│   │   └── install.py
│   ├── hooks.py
│   └── __init__.py
├── README.md
├── license.txt
└── requirements.txt
```

## Troubleshooting

### App not showing after installation
```bash
bench --site your-site.local clear-cache
bench restart
```

### Permissions not working
```bash
# Check if permission hooks are loaded
bench --site your-site.local console

# In console:
import frappe
print(frappe.get_hooks("permission_query_conditions"))
print(frappe.get_hooks("has_permission"))
```

### Dummy data not created
```bash
# Run installation script manually
bench --site your-site.local console

# In console:
from purchase_approval.install import after_install
after_install()
```

### Report not visible
- Check if user has appropriate role (Purchase Manager, Purchase User, or System Manager)
- Clear cache: `bench --site your-site.local clear-cache`

## Development

### Running in Development Mode
```bash
bench --site your-site.local set-config developer_mode 1
bench restart
```

### Making Changes
After modifying code:
```bash
bench --site your-site.local migrate
bench --site your-site.local clear-cache
bench restart
```

## API Usage

### Approve Request via API
```python
import frappe

# Get document
doc = frappe.get_doc("Purchase Approval Request", "PAR-0001")

# Call approval method
doc.approve_request()
```

### Query with Permissions
```python
# This respects permission queries
records = frappe.get_all(
    "Purchase Approval Request",
    fields=["name", "requester", "total_amount", "status"]
)
```

## License

MIT License

## Support

For issues and questions:
- GitHub Issues: https://github.com/yourusername/purchase_approval/issues
- Email: your@email.com

## Contributors

- Your Name (your@email.com)

---

**Note**: This app is designed for ERPNext v14/v15. For other versions, adjustments may be required.