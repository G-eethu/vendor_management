import re
import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import validate_email_address

GST_PATTERN = r'^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z][1-9A-Z]Z[0-9A-Z]$'


class VendorOnboardingRequest(Document):

    def validate(self):
        self.validate_email()
        self.validate_gst()
        self.validate_annual_turnover()
        self.validate_documents_before_submission()

    def on_update(self):
        self.create_supplier()

    def validate_email(self):
        if not self.email:
            frappe.throw(_("Email is required"))

        validate_email_address(self.email.strip(), True)

    def validate_gst(self):
        if not self.gst_number:
            return

        gstin = self.gst_number.strip().upper()

        if not re.match(GST_PATTERN, gstin):
            frappe.throw(_("Invalid GSTIN"))

    def validate_annual_turnover(self):
        if self.annual_turnover < 0:
            frappe.throw(_("Annual Turnover cannot be negative"))

    def validate_documents_before_submission(self):
        if (
            self.workflow_state == "Submitted"
            and not self.documents_submitted
        ):
            frappe.throw(
                _("Documents Submitted must be checked before submission.")
            )

    def create_supplier(self):

        # Only create after approval
        if self.workflow_state != "Approved":
            return

        # Already linked
        if self.get("supplier"):
            return

        # Duplicate by GSTIN
        if self.gst_number:
            supplier = frappe.db.exists(
                "Supplier",
                {"gstin": self.gst_number}
            )

            if supplier:
                self.db_set("supplier", supplier)
                return

        # Duplicate by Name
        supplier = frappe.db.exists(
            "Supplier",
            {"supplier_name": self.contact_person}
        )

        if supplier:
            self.db_set("supplier", supplier)
            return

        supplier = frappe.get_doc({
            "doctype": "Supplier",
            "supplier_name": self.contact_person,
            "supplier_group": "All Supplier Groups",
            "supplier_type": self.vendor_type,
            "gstin": self.gst_number
        })

        supplier.insert(ignore_permissions=True)

        self.db_set("supplier", supplier.name)

        frappe.msgprint(
            _("Supplier <b>{0}</b> created successfully.").format(supplier.name)
        )