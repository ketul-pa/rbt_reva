{
    "name": "Attendance Dashboard",
    "version": "18.0.1.0.0",
    'author': 'Incipientcorp',
    "maintainer": "Incipientcorp",
    "description": "AttendanceDashboard",
    'website': "www.incipientcorp.com",
    'license': 'LGPL-3',
    "depends": ['hr_attendance', 'hr', 'hr_holidays'],
    "data": [
        "views/hr_attendance.xml",
        "views/hr_employee.xml",
    ],
    'assets': {
        'web.assets_backend': [
            'entrivis_attendance_dashboard/static/src/scss/attendance_dashboard.scss',
            'entrivis_attendance_dashboard/static/src/xml/attendance_dashboard.xml',
            'entrivis_attendance_dashboard/static/src/js/attendance_dashboard.js',
        ],
    },
}
