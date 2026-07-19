import frappe
from frappe import _

@frappe.whitelist(allow_guest=False)
def get_dashboard_stats():
    vendor_type_data = frappe.db.get_all(
        "Vendor Onboarding Request",
        fields=["vendor_type", "count(name) as count"],
        group_by="vendor_type"
    )

    workflow_state_data = frappe.db.get_all(
        "Vendor Onboarding Request",
        fields=["workflow_state", "count(name) as count"],
        group_by="workflow_state"
    )

    return {
        "vendor_type": vendor_type_data,
        "workflow_state": workflow_state_data
    }


@frappe.whitelist(allow_guest=False)
def get_approved_rejected_stats():
    data = frappe.db.get_all(
        "Vendor Onboarding Request",
        filters={"workflow_state": ["in", ["Approved", "Rejected"]]},
        fields=["workflow_state", "count(name) as count"],
        group_by="workflow_state"
    )

    result = {"Approved": 0, "Rejected": 0}
    for row in data:
        result[row.workflow_state] = row.count

    return result


@frappe.whitelist(allow_guest=False)
def get_vendor_requests_list():
    return frappe.get_all(
        "Vendor Onboarding Request",
        fields=[
            "name",
            "vendor_name",
            "vendor_type",
            "contact_person",
            "email",
            "workflow_state",
            "creation"
        ],
        order_by="creation desc"
    )