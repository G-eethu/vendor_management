import frappe
from frappe import _
from frappe.utils import cint

# create a new Vendor Onboarding Request
@frappe.whitelist(allow_guest=True)
def create_request():
    data = frappe.local.form_dict

    doc = frappe.get_doc({
        "doctype": "Vendor Onboarding Request",
        "vendor_name": data.get("vendor_name"),
        "contact_person": data.get("contact_person"),
        "email": data.get("email"),
        "phone": data.get("phone") or '',
        "gst_number": data.get("gst_number") or '',
        "annual_turnover": cint(data.get("annual_turnover")),
        "vendor_type": data.get("vendor_type")
    })
    doc.insert(ignore_permissions=True)
    return {"name": doc.name, "message": _("Vendor Onboarding Request created successfully")}


# create a new Vendor Onboarding Request
@frappe.whitelist(allow_guest=True)
def get_request(name):

    if not frappe.db.exists("Vendor Onboarding Request", name):
        frappe.throw(_("Vendor Request not found"))

    doc = frappe.get_doc("Vendor Onboarding Request", name)

    return {
        "name": doc.name,
        "vendor_name": doc.vendor_name,
        "vendor_type": doc.vendor_type,
        "contact_person": doc.contact_person,
        "email": doc.email,
        "phone": doc.phone,
        "gst_number": doc.gst_number,
        "annual_turnover": doc.annual_turnover,
        "workflow_state": doc.workflow_state,
        "documents_submitted": doc.documents_submitted
    }

@frappe.whitelist(allow_guest=True)
def get_all_requests():
    requests = frappe.get_all(
        "Vendor Onboarding Request",
        fields=[
            "name",
            "vendor_name",
            "vendor_type",
            "contact_person",
            "email",
            "phone",
            "gst_number",
            "annual_turnover",
            "workflow_state",
            "documents_submitted"
        ],
        order_by="creation desc"
    )

    return requests
