# Copyright (c) 2023, ithead@ambibuzz.com and contributors
# For license information, please see license.txt

import frappe

def execute(filters = None):
	if filter is None:
		return [], []

	data = get_data(filters.start_date, filters.end_date, filters.employee, filters.company, filters.department)
	columns = get_columns()
	return columns, data

def get_attendances(start_date, end_date, employee = None, company = None, department = None):
	attendance_filters = [
						["Attendance", "attendance_date", "between", [start_date, end_date]],
						["Attendance", "docstatus", "=", "1"],
						]

	if employee:
		attendance_filters.append(["Attendance", "employee", "=", employee])
	if company:
		attendance_filters.append(["Attendance", "company", "=", company])
	if department:
		attendance_filters.append(["Attendance", "department", "=", department])

	attendance_fields = ["attendance_date", "employee", "company", "department", "working_hours", "name", "shift_hour"]

	attendance_list = frappe.get_all(
									"Attendance",
									filters = attendance_filters,
									fields = attendance_fields
									)
	return attendance_list

def get_timesheets(start_date, end_date, employee = None, company = None, department = None):
	timesheet_filters = [
						["Timesheet", "start_date", ">=", start_date],
						["Timesheet", "end_date", "<=", end_date],
						["Timesheet", "status", "=", "Submitted"],
						["Timesheet", "is_overtime", "=", 1]
						]
	if employee:
		timesheet_filters.append(["Timesheet", "employee", "=", employee])

	timesheet_fields = ["name"]

	timesheet_list = frappe.get_all(
									"Timesheet",
									filters = timesheet_filters,
									fields = timesheet_fields
									)

	return timesheet_list

def get_employees(employee = None, company = None, department = None):
	# if nothing was passed as argument for Employee to the report, create a list
	# of all employees
	employee_filter = [["Employee", "status", "=", "Active"]]
	if employee is not None:
		# or else simply add the passed Employee argument
		employee_filter.append(["Employee", "name", "=", employee])

	employee_fields = ["name"]

	employee_list = frappe.get_all("Employee", filters = employee_filter, fields = employee_fields)

	return employee_list

def get_timesheet_details(timesheet_parent, attendance_date):
	td_filters = [
				["Timesheet Detail", "parent", "=", timesheet_parent],
				["Timesheet Detail", "from_time", "between", [attendance_date, attendance_date]],
				["Timesheet Detail", "activity_type", "=", "Over Time"]
				]
	td_fields = ["activity_type", "hours", "name"]

	timesheet_detail_list = frappe.get_all(
										"Timesheet Detail",
										filters = td_filters,
										fields = td_fields
									)
	return timesheet_detail_list

def get_data(start_date, end_date, employee = None, company = None, department = None):
	result = []
	# Fetch either all employees or the one filtered
	employee_list = get_employees(employee, company, department)
	if (employee_list is None or len(employee_list) < 0):
		return result
	
	for e in employee_list:
		attendance_list = get_attendances(start_date, end_date, e.name, company, department)
		timesheet_list = get_timesheets(start_date, end_date, e.name, company, department)
		for i in attendance_list:
			total_timesheet_hr = 0
			for j in timesheet_list:
				total_hours = 0
				timesheet_detail_list = get_timesheet_details(j.name, i.attendance_date)
				if (len(timesheet_detail_list) > 0):
					i.update({
						"timesheet": j.name,
						})
				else:
					continue
				for k in timesheet_detail_list:
						total_hours += k.hours
				total_timesheet_hr += total_hours
			excess_hours = i.working_hours - i.shift_hour
			balance_overtime_hours = total_timesheet_hr - excess_hours
			i.update({
					"overtime_hours": total_timesheet_hr,
					"excess_hours": excess_hours,
					"balance_overtime_hours": balance_overtime_hours,
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
				"fieldname": "overtime_hours",
				"fieldtype": "Float",
				"label": "Overtime Hours",
				"width": 0
				},
				{
				"fieldname": "excess_hours",
				"fieldtype": "Float",
				"label": "Excess Hours",
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
				},
		]
	return columns
