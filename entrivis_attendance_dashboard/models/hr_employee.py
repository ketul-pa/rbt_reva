from odoo import models, fields, api
from datetime import datetime, timedelta
from pytz import timezone, UTC
import calendar


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    week_schedule_html = fields.Html(string="Weekly Schedule", sanitize=False,
                                     compute="_compute_schedule_html", store=True)
                                     # default=lambda self: self._default_schedule_html())
    birthdate = fields.Date("BirthDate")

    @api.depends('resource_calendar_id')
    def _compute_schedule_html(self):
        for employee in self:
            calendar_model = employee.resource_calendar_id

            if not calendar_model or not calendar_model.attendance_ids:
                employee.week_schedule_html = "<div>No working schedule assigned.</div>"
                continue

            day_attendance = {}
            for line in calendar_model.attendance_ids:
                day_name = calendar.day_name[int(line.dayofweek)]
                day_attendance.setdefault(day_name, []).append(line)

            boxes = []
            for day_name, lines in sorted(day_attendance.items(), key=lambda d: list(calendar.day_name).index(d[0])):
                daily_blocks = ""
                for line in lines:
                    start_time = f"{int(line.hour_from):02d}:{int((line.hour_from % 1) * 60):02d}"
                    end_time = f"{int(line.hour_to):02d}:{int((line.hour_to % 1) * 60):02d}"
                    daily_blocks += f"""
                            <div style="margin-bottom: 5px;">
                                Start: <span style="color: green;">{start_time}</span> -
                                End: <span style="color: red;">{end_time}</span>
                            </div>
                        """
                boxes.append(f"""
                        <div style="flex: 1 1 30%; border: 2px solid #007bff; padding: 10px; border-radius: 8px; min-width: 200px;">
                            <b style="color: #000;">{day_name}</b><br/>
                            {daily_blocks}
                        </div>
                    """)

            employee.week_schedule_html = f"""
                    <div style="display: flex; flex-wrap: wrap; gap: 10px;">
                        {''.join(boxes)}
                    </div>
                """