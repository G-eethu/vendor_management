// Override description: Redirect "Vendor Dashboard" workspace to the vendor-dash page

frappe.provide("frappe.views");

frappe.views.Workspace = class CustomWorkspace extends frappe.views.Workspace {
	constructor(wrapper) {
		super(wrapper);
	}

	async show_page(page) {
		if (page && page.name === "Vendor Dashboard") {
			frappe.set_route("vendor-dash");
			return;
		}

		return super.show_page(page);
	}
};