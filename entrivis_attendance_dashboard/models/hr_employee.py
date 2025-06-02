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
            day_period = {
                'morning': 'Morning',
                'lunch': 'Break',
                'afternoon': 'Afternoon',
            }
            for day_name, lines in sorted(day_attendance.items(), key=lambda d: list(calendar.day_name).index(d[0])):
                daily_blocks = ""
                daily_blocks += f"""
                    <div class="mb-1 row">
                        <div class="col-4"><b>Day Period</b></div>
                        <div class="col-4"><b>Start</b></div>
                        <div class="col-4"><b>End</b></div>
                    </div>"""
                for line in lines:
                    start_time = f"{int(line.hour_from):02d}:{int((line.hour_from % 1) * 60):02d}"
                    end_time = f"{int(line.hour_to):02d}:{int((line.hour_to % 1) * 60):02d}"
                    daily_blocks += f"""
                        <div class="mb-1 row">
                            <div class="col-4"><b>{day_period.get(line.day_period)} : </b></div>
                            <div class="col-4">{start_time}</div>
                            <div class="col-4">{end_time}</div>
                        </div>"""
                boxes.append(f"""
                    <div style="flex: 1 1 30%; border: 0.5px solid #A9A9A9; padding: 7px; min-width: 200px;" class="shadow-sm rounded bg-100">
                        <div class="p-2 rounded bg-success bg-opacity-25 mb-2"><b><center>{day_name}</center></b></div>
                        <div class="bg-info bg-opacity-25 p-2">
                        {daily_blocks}
                        </div>
                    </div>""")

            employee.week_schedule_html = f"""
                    <div style="display: flex; flex-wrap: wrap; gap: 10px;">
                        {''.join(boxes)}
                    </div>
                """