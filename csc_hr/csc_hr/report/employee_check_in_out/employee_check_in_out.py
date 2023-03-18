# Copyright (c) 2023, ithead@ambibuzz.com and contributors
# For license information, please see license.txt

import frappe

def execute(filters = None):
        data = get_data(filters.employee, filters.start_date, filters.end_date, filters.company, filters.department)
        columns = get_columns()
        return columns, data

def get_data(employee, start_date, end_date, company = None, department = None):
        attendance_filters = [
            ["Attendance", "attendance_date", "between", [start_date, end_date]],
            ["Attendance", "docstatus", "=", "1"],
            ["Attendance", "employee", "=", employee]
        ]
        timesheet_filters = [                   
            ["Timesheet", "start_date", ">=", start_date],
            ["Timesheet", "end_date", "<=", end_date],
            ["Timesheet", "employee", "=", employee],
            ["Timesheet", "status", "=", "Submitted"]
        ]

        attendance_fields = ["attendance_date", "employee", "company", "department","working_hours", "name", "shift_hour"]
        if company:
            attendance_filters.append(["Attendance", "company", "=", company])
        if department:
            attendance_filters.append(["Attendance", "department", "=", department])
        result = []
        attendance_list = frappe.get_all(
                                        "Attendance",
                                        filters = attendance_filters,
                                        fields = attendance_fields
                                        )
        timesheet_list = frappe.get_all(
                                    "Timesheet",
                                    filters = timesheet_filters,
                                    fields = ["name"]
                                    )
        for i in attendance_list:
            total_timesheet_hr = 0
            timesheet_name = None
            for j in timesheet_list:
                timesheet_child_list = frappe.get_all(
                                                    "Timesheet Detail",
                                                    filters = [["Timesheet Detail", "parent", "=", j.name],
                                                               ["Timesheet Detail", "from_time", "between", [i.attendance_date, i.attendance_date]],
                                                               ["Timesheet Detail", "activity_type", "=", "Over Time"]],
                                                    fields = ["activity_type", "hours", "name"]
                                                    )
                total_hours = 0
                if (len(timesheet_child_list) > 0):
                    i.update({
                        "is_overtime": 1,
                        "timesheet": j.name,
                        "activity_type": "Over Time"
                        })
                else:
                    continue
                for k in timesheet_child_list:
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
                "fieldname": "is_overtime",
                "fieldtype": "Data",
                "label": "Overtime",
                "width": 0
                },
                {
                "fieldname": "activity_type",
                "fieldtype": "Data",
                "label": "Activity Type",
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
