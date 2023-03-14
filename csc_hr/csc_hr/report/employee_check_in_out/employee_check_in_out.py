# Copyright (c) 2023, ithead@ambibuzz.com and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
	data = get_data(filters.employee, filters.start_date, filters.end_date)
	columns = get_columns()
	return columns, data

def get_data(employee = "HR-EMP-00008", start_date="2023-01-01", end_date="2023-03-14"):
	result = []
	attendance_list = frappe.get_all("Attendance", filters = [["Attendance", "attendance_date", "between", [start_date, end_date]], ["Attendance", "docstatus", "=", "1"], ["Attendance", "employee", "=", employee]], fields = ["attendance_date","employee","company","department","working_hours", "name"])
	for i in attendance_list:
		timesheet_name = None
		timesheet_list = frappe.get_all("Timesheet", filters = [["Timesheet", "start_date", ">=", start_date], ["Timesheet", "end_date", "<=", end_date],["Timesheet", "employee", "=", employee],  ["Timesheet", "status", "=", "Submitted"]], fields = ["name"])
		total_timesheet_hr = 0
		for j in timesheet_list:
			timesheet_child_list = frappe.get_all("Timesheet Detail", filters = [["Timesheet Detail", "parent", "=", j.name], ["Timesheet Detail", "from_time", "between", [i.attendance_date, i.attendance_date]]], fields = ["activity_type", "hours", "name"])
			total_hours = 0
			for k in timesheet_child_list:
				total_hours += k.hours
			total_timesheet_hr += total_hours
			timesheet_name = j.name
		overtime_hours = i.working_hours - 8.0
		balance_overtime_hours = overtime_hours - total_timesheet_hr 
		i.update({
			"activity_hours": total_timesheet_hr,
			"overtime_hours": overtime_hours,
			"balance_overtime_hours": balance_overtime_hours,
			"timesheet": timesheet_name
		})
		result.append(i)
	return result

def get_columns():
    columns = [
		{
		"fieldname": "attendance_date",
		"fieldtype": "Date",
		"label":"Date",
		"width": 0
		},
		{
		"fieldname": "employee",
		"fieldtype": "Link",
		"options": "Employee",
		"label": "Employee",
		"width": 0
		},
		{
		"fieldname": "company",
		"fieldtype": "Data",
		"label": "Company",
		"width": 0
		},
		{
		"fieldname": "department",
		"fieldtype": "Data",
		"label": "Department",
		"width": 0
		},
		{
		"fieldname": "working_hours",
		"fieldtype": "Float",
		"label": "Working Hours",
		"width": 0
		},
		{
		"fieldname": "activity_type",
		"fieldtype": "Link",
		"label": "Activity Type",
		"options": "Employee Checkin",
		"width": 0
		},
		{
		"fieldname": "activity_hours",
		"fieldtype": "Float",
		"label": "Activity Hours",
		"width": 0
		},
		{
		"fieldname": "overtime_hours",
		"fieldtype": "Float",
		"label": "Overtime Hours",
		"width": 0
		},
		{
		"fieldname": "balance_overtime_hours",
		"fieldtype": "Float",
		"label": "Balance Overtime Hours",
		"width": 0
		},
		{
		"fieldname": "timesheet",
		"fieldtype": "Link",
		"options": "Timesheet",
		"label": "Timesheet",
		"width": 0
		},
		{
		"fieldname": "name",
		"fieldtype": "Link",
		"options": "Attendance",
		"label": "Attendance",
		"width": 0
		}
	]
    return columns
