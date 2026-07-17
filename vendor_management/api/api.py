import frappe
from frappe import _
from frappe.utils import cint


@frappe.whitelist(allow_guest=False)
def create_request():
    """
    Create Vendor Onboarding Request
    """

    data = frappe.local.form_dict

    vendor = frappe.get_doc({
        "doctype": "Vendor Onboarding Request",
        "vendor_name": data.get("vendor_name"),
        "vendor_type": data.get("vendor_type"),
        "contact_person": data.get("contact_person"),
        "email": data.get("email"),
        "phone": data.get("phone"),
        "gst_number": data.get("gst_number"),
        "annual_turnover": data.get("annual_turnover") or 0,
        "documents_submitted": cint(data.get("documents_submitted", 0))
    })

    vendor.insert(ignore_permissions=True)
    frappe.db.commit()

    return {
        "success": True,
        "message": "Vendor Request Created",
        "data": {
            "name": vendor.name,
            "workflow_state": vendor.workflow_state,
            "vendor_name": vendor.vendor_name
        }
    }


@frappe.whitelist(allow_guest=False)
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