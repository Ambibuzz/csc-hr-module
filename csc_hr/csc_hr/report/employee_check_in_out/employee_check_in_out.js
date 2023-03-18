// Copyright (c) 2023, ithead@ambibuzz.com and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Employee Check In Out"] = {
	"filters": [
		{
			"fieldname":"employee",
			"label": "Employee",
			"fieldtype": "Link",
			"options": "Employee",
			"reqd": 1
		},
		{
			"fieldname":"start_date",
			"label": "Start Date",
			"fieldtype": "Date",
			"reqd": 1
		},
		{
			"fieldname":"end_date",
			"label": "End Date",
			"fieldtype": "Date",
			"reqd": 1
		},
		{
			"fieldname":"company",
			"label": "Company",
			"fieldtype": "Link",
			"options": "Company",
		},
		{
			"fieldname":"department",
			"label": "Department",
			"fieldtype": "Link",
			"options": "Department",
		}
	]
};
