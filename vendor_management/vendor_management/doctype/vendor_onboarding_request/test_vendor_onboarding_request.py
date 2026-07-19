# Copyright (c) 2026, developer and Contributors
# See license.txt

import frappe
from frappe.exceptions import ValidationError
from frappe.tests.utils import FrappeTestCase


class TestVendorOnboardingRequest(FrappeTestCase):

    def make_request(self, **kwargs):
        data = {
            "doctype": "Vendor Onboarding Request",
            "vendor_name": "Test Vendor",
            "vendor_type": "Contractor",
            "contact_person": "John Doe",
            "email": "john@test.com",
            "phone": "9876543210",
            "gst_number": "32ABCDE1234F1Z5",
            "annual_turnover": 100000,
            "documents_submitted": 1,
            "workflow_state": "Draft",
            "status": "Draft",
        }

        data.update(kwargs)
        return frappe.get_doc(data)

    def tearDown(self):
        frappe.db.rollback()

    def test_invalid_email(self):
        doc = self.make_request(email="invalid-email")

        with self.assertRaises(ValidationError):
            doc.insert()

    def test_invalid_gst(self):
        doc = self.make_request(gst_number="12345")

        with self.assertRaises(ValidationError):
            doc.insert()

    def test_negative_turnover(self):
        doc = self.make_request(annual_turnover=-100)

        with self.assertRaises(ValidationError):
            doc.insert()

    def test_missing_document_submission(self):
        doc = self.make_request(
            workflow_state="Submitted",
            documents_submitted=0
        )

        with self.assertRaises(ValidationError):
            doc.insert()

    def test_successful_request_creation(self):
        doc = self.make_request()

        doc.insert()

        self.assertTrue(doc.name)
        self.assertEqual(doc.vendor_name, "Test Vendor")

    def test_successful_approval_flow(self):
        doc = self.make_request()

        doc.insert()

        doc.db_set("workflow_state", "Approved")
        doc.db_set("status", "Approved")
        doc.reload()

        self.assertEqual(doc.status, "Approved")

    def test_supplier_creation_after_approval(self):

        doc = self.make_request(
            vendor_name="Supplier Test Vendor"
        )

        doc.insert()

        doc.db_set("workflow_state", "Approved")
        doc.db_set("status", "Approved")
        doc.reload()

        doc.create_supplier()

        supplier = frappe.db.exists(
            "Supplier",
            {"supplier_name": "Supplier Test Vendor"}
        )


    def test_duplicate_supplier_prevention(self):

        frappe.get_doc({
            "doctype": "Supplier",
            "supplier_name": "Duplicate Vendor",
            "supplier_group": "All Supplier Groups",
            "supplier_type": "Company"
        }).insert(ignore_permissions=True)

        doc = self.make_request(
            vendor_name="Duplicate Vendor"
        )

        doc.insert()

        doc.db_set("workflow_state", "Approved")
        doc.db_set("status", "Approved")
        doc.reload()

        doc.create_supplier()

        suppliers = frappe.get_all(
            "Supplier",
            filters={"supplier_name": "Duplicate Vendor"}
        )

        self.assertEqual(len(suppliers), 1)
        
# bench run-tests --app vendor_management