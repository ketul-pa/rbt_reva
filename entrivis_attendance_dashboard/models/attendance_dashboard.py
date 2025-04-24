from datetime import timedelta
from odoo import models, fields, api
from datetime import datetime
from dateutil.relativedelta import relativedelta

class AttendanceDashboard(models.Model):
    _name = 'attendance.dashboard'
    _description = 'Attendance Dashboard'

    @api.model
    def get_dashboard_data(self):
        data = {}
        data.update(self._get_counts())
        data.update(self._get_today_attendance_data())
        data.update(self._get_check_in_check_out_data())
        data.update(self._get_todays_time_off_data())
        data.update(self._get_upcoming_30_days_time_off_data())
        data.update(self._get_upcoming_birthday())
        return data

    def _get_upcoming_birthday(self):
        today = datetime.today().date()
        upcoming = today + timedelta(days=30)
        employees = self.env['hr.employee'].search([('birthdate', '!=', False)])
        birthday_data = []

        for emp in employees:
            birthdate = emp.birthdate
            if not birthdate:
                continue

            this_year_birthday = birthdate.replace(year=today.year)
            this_year_birthday = this_year_birthday if isinstance(this_year_birthday, datetime) else datetime.combine(
                this_year_birthday, datetime.min.time())
            this_year_birthday = this_year_birthday.date()

            if this_year_birthday < today:
                this_year_birthday = this_year_birthday.replace(year=today.year + 1)

            if today <= this_year_birthday <= upcoming:
                birthday_data.append({
                    'name': emp.name,
                    'birthdate': birthdate.strftime('%Y-%m-%d'),
                })

        return {
            'upcoming_birthday_employee': birthday_data
        }


    def _get_counts(self):
        employee_count = self.env['hr.employee'].search_count([])
        # contract_count = self.env['hr.contract'].search_count([('state', '=', 'open')])
        contract_count = 50
        return {
            'employee_count': employee_count,
            'contract_count': contract_count,
        }

    def _get_today_attendance_data(self):
        today = fields.Date.today()
        today_start = datetime.combine(today, datetime.min.time()).strftime('%Y-%m-%d %H:%M:%S')
        # today_end = datetime.combine(today, datetime.max.time()).strftime('%Y-%m-%d %H:%M:%S')

        # Fetch employees whose last check-in is missing or not within today's range
        missing_attendance_employees = self.env['hr.employee'].search([
            '|',
            ('last_check_in', '=', False),  # Missing last_check_in
            ('last_check_in', '<', today_start)  # last_check_in not within today's range
        ])

        attendance_data = []
        for employee in missing_attendance_employees:
            attendance_data.append({
                'emp_id': employee.id,
                'id': employee.id,
                'name': employee.name,
                # 'registration_number': employee.registration_number if employee.registration_number else "-",
                # 'shift': employee.resource_calendar_id.name if employee.registration_number else "-",
            })
        print("\n\n attendance data-----------", attendance_data, len(attendance_data))
        return {
            'today_missing_attendance': attendance_data,
            'missing_attendance_count': len(attendance_data),
        }

    def _get_check_in_check_out_data(self):
        today = fields.Date.today()
        today_start = datetime.combine(today, datetime.min.time()).strftime('%Y-%m-%d %H:%M:%S')
        today_end = datetime.combine(today, datetime.max.time()).strftime('%Y-%m-%d %H:%M:%S')

        # Fetch attendance records where check_in is within today's range
        today_attendance_records = self.env['hr.attendance'].search([
            ('check_in', '>=', today_start),
            ('check_in', '<=', today_end)
        ])

        attendance_data = []
        for record in today_attendance_records:
            employee = record.employee_id
            attendance_data.append({
                'employee_id': employee.id,
                'employee_name': employee.name,
                'check_in': record.check_in,
                'check_out': record.check_out if record.check_out else "-",
                # 'registration_number': employee.registration_number if employee.registration_number else "-",
            })

        return {
            'today_check_in_check_out': attendance_data,
            'today_check_in_check_out_count': len(attendance_data)
        }

    def _get_todays_time_off_data(self):
        today = fields.Date.today()

        # Fetch leave records where today falls in the leave range
        todays_leaves = self.env['hr.leave'].search([
            '|', '|',
            ('date_from', '=', today),  # Leave starts today
            ('date_to', '=', today),  # Leave ends today
            '&', ('date_from', '<=', today), ('date_to', '>=', today)  # Leave spans across today
        ])
        time_off_data = []
        for leave in todays_leaves:
            for employee in leave.employee_id:
                time_off_data.append({
                    'employee_id': employee.id,
                    'employee_name': employee.name,
                    'time_off_type': leave.holiday_status_id.name,
                    'date_from': leave.date_from,
                    'date_to': leave.date_to,
                    'duration': leave.duration_display,
                    'description': leave.name,
                    'status': leave.state,
                })

        return {
            'today_time_off': time_off_data,
            'today_time_off_count': len(time_off_data)
        }

    def _get_upcoming_30_days_time_off_data(self):
        today = fields.Date.today()
        end_date = today + timedelta(days=30)  # Calculate the next 30 days

        upcoming_leaves = self.env['hr.leave'].search([
            '|',
            '&', ('date_from', '>=', today), ('date_from', '<=', end_date),  # Leaves starting within the next 30 days
            '&', ('date_to', '>=', today), ('date_to', '<=', end_date)  # Leaves ending within the next 30 days
        ])

        time_off_data = []
        for leave in upcoming_leaves:
            for employee in leave.employee_id:
                time_off_data.append({
                    'employee_id': employee.id,
                    'employee_name': employee.name,
                    'time_off_type': leave.holiday_status_id.name,
                    'date_from': leave.date_from,
                    'date_to': leave.date_to,
                    'duration': leave.duration_display,
                    'description': leave.name if leave.name else "-",
                    'status': leave.state,
                })

        return {
            'today_date': today.strftime('%d-%m-%Y'),  # Format date as string
            'end_date': end_date.strftime('%d-%m-%Y'),
            'upcoming_30_days_time_off': time_off_data,
            'upcoming_30_days_time_off_count': len(time_off_data)
        }

