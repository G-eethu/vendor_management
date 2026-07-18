# Copyright (c) 2026, developer and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
    columns = get_columns()
    data = get_data()

    return columns, data


def get_columns():
    return [
        {
            "label": "Vendor Type",
            "fieldname": "vendor_type",
            "fieldtype": "Data",
            "width": 180,
        },
        {
            "label": "Total",
            "fieldname": "total",
            "fieldtype": "Int",
            "width": 120,
        },
        {
            "label": "Approved",
            "fieldname": "approved",
            "fieldtype": "Int",
            "width": 120,
        },
        {
            "label": "Rejected",
            "fieldname": "rejected",
            "fieldtype": "Int",
            "width": 120,
        },
        {
            "label": "Pending",
            "fieldname": "pending",
            "fieldtype": "Int",
            "width": 120,
        },
    ]


def get_data():

    return frappe.db.sql(
        """
        SELECT
            vendor_type,

            COUNT(*) AS total,

            SUM(
                CASE
                    WHEN workflow_state='Approved'
                    THEN 1 ELSE 0
                END
            ) AS approved,

            SUM(
                CASE
                    WHEN workflow_state='Rejected'
                    THEN 1 ELSE 0
                END
            ) AS rejected,

            SUM(
                CASE
                    WHEN workflow_state IN ('Pending', 'Under Review')
                    THEN 1 ELSE 0
                END
            ) AS pending

        FROM `tabVendor Onboarding Request`

        GROUP BY vendor_type

        ORDER BY vendor_type
        """,
        as_dict=True,
    )
