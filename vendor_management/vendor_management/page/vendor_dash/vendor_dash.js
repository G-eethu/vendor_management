frappe.pages['vendor-dash'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Vendor Dash',
		single_column: true
	});

	// Charts container
	let $charts = $(`
		<div class="vendor-dash-charts" style="display: flex; flex-wrap: wrap; gap: 24px; padding: 20px;">
			<div id="vendor-type-chart" style="flex: 1; min-width: 400px;"></div>
			<div id="workflow-state-chart" style="flex: 1; min-width: 400px;"></div>
			<div id="approved-rejected-chart" style="flex: 1; min-width: 400px;"></div>
		</div>
	`).appendTo(page.body);

	// List container
	let $listSection = $(`
		<div style="padding: 0 20px 20px 20px;">
			<div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px;">
				<h4 style="margin: 0;">Vendor Onboarding Requests</h4>
				<button class="btn btn-xs btn-default" id="clear-filter-btn" style="display: none;">
					Clear Filter
				</button>
			</div>
			<div id="active-filter-label" style="margin-bottom: 8px; font-size: 12px; color: #616161; display: none;"></div>
			<table class="table table-bordered" id="vendor-request-table">
				<thead>
					<tr style="background-color: #616161ff; color: #000000ff;">
						<th>ID</th>
						<th>Vendor Name</th>
						<th>Vendor Type</th>
						<th>Contact Person</th>
						<th>Email</th>
						<th>Workflow State</th>
						<th>Created</th>
					</tr>
				</thead>
				<tbody></tbody>
			</table>
		</div>
	`).appendTo(page.body);

	let all_requests = [];

	load_dashboard_charts();
	load_vendor_requests_list();

	$("#clear-filter-btn").on("click", function() {
		render_table_rows(all_requests);
		$("#clear-filter-btn").hide();
		$("#active-filter-label").hide();
	});

	function load_dashboard_charts() {
		frappe.call({
			method: "vendor_management.vendor_management.page.vendor_dash.vendor_dash.get_dashboard_stats",
			callback: function(r) {
				if (!r.message) return;

				render_bar_chart(
					"vendor-type-chart",
					"Vendor Type Distribution",
					r.message.vendor_type,
					"vendor_type"
				);

				render_bar_chart(
					"workflow-state-chart",
					"Workflow State Distribution",
					r.message.workflow_state,
					"workflow_state"
				);

				render_approved_rejected_chart(
					"approved-rejected-chart",
					"Approved vs Rejected Vendors",
					r.message.workflow_state
				);
			}
		});
	}

	function render_bar_chart(container_id, title, data, key) {
		let labels = data.map(d => d[key] || "Not Set");
		let values = data.map(d => d.count);

		new frappe.Chart(`#${container_id}`, {
			title: title,
			data: {
				labels: labels,
				datasets: [
					{
						name: title,
						values: values
					}
				]
			},
			type: "bar",
			height: 300,
			colors: ["#f39ff3ff"],
			barOptions: {
				spaceRatio: 0.5
			}
		});
	}

	function render_approved_rejected_chart(container_id, title, workflow_state_data) {
		let approved_count = 0;
		let rejected_count = 0;

		workflow_state_data.forEach(function(d) {
			if (d.workflow_state === "Approved") {
				approved_count = d.count;
			} else if (d.workflow_state === "Rejected") {
				rejected_count = d.count;
			}
		});

		let labels = ["Approved", "Rejected"];
		let values = [approved_count, rejected_count];

		let chart = new frappe.Chart(`#${container_id}`, {
			title: title,
			data: {
				labels: labels,
				datasets: [
					{
						name: title,
						values: values
					}
				]
			},
			type: "pie",
			height: 300,
			colors: ["#4CAF50", "#E53935"]
		});

		// frappe.Chart fires this custom event on slice/bar click, passing the index
		$(`#${container_id}`).on("click", ".chart-container", function() {});

		chart.parent.addEventListener("data-select", function(e) {
			let index = e.index;
			if (index === undefined || index === null) return;

			let selected_label = labels[index];
			filter_table_by_workflow_state(selected_label);
		});
	}

	function filter_table_by_workflow_state(state) {
		let filtered = all_requests.filter(row => row.workflow_state === state);
		render_table_rows(filtered);

		$("#clear-filter-btn").show();
		$("#active-filter-label")
			.text(`Showing ${filtered.length} request(s) with status: ${state}`)
			.show();
	}

	function load_vendor_requests_list() {
		frappe.call({
			method: "vendor_management.vendor_management.page.vendor_dash.vendor_dash.get_vendor_requests_list",
			callback: function(r) {
				if (!r.message) return;

				all_requests = r.message;
				render_table_rows(all_requests);
			}
		});
	}

	function render_table_rows(rows) {
		let $tbody = $("#vendor-request-table tbody");
		$tbody.empty();

		if (!rows.length) {
			$tbody.append(`<tr><td colspan="7" style="text-align: center; color: #999;">No records found</td></tr>`);
			return;
		}

		rows.forEach(function(row) {
			let $tr = $(`
				<tr style="cursor: pointer;">
					<td><a href="#" class="vendor-request-link" data-name="${row.name}">${row.name}</a></td>
					<td>${frappe.utils.escape_html(row.vendor_name || "")}</td>
					<td>${frappe.utils.escape_html(row.vendor_type || "")}</td>
					<td>${frappe.utils.escape_html(row.contact_person || "")}</td>
					<td>${frappe.utils.escape_html(row.email || "")}</td>
					<td>${frappe.utils.escape_html(row.workflow_state || "Draft")}</td>
					<td>${frappe.datetime.str_to_user(row.creation)}</td>
				</tr>
			`);
			$tbody.append($tr);
		});

		// Click anywhere in the row to open the doc
		$tbody.find("tr").on("click", function() {
			let name = $(this).find(".vendor-request-link").data("name");
			if (name) {
				frappe.set_route("Form", "Vendor Onboarding Request", name);
			}
		});
	}
};