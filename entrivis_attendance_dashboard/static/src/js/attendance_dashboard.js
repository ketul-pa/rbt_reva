/** @odoo-module **/
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Component, onWillStart } from "@odoo/owl";
import { onMounted } from "@odoo/owl";
import { user } from "@web/core/user";

export class AttendanceDashboard extends Component {
    static template = 'AttendanceDashboardMain';
    static props = ["*"];

     setup() {
        this.orm = useService("orm");
        this.action = useService("action");
        this.employee_count = '0';
        this.contract_count = '0';
        this.company_code_99a = '';
        this.company_code_99s = '';
        this.company_code_99x = '';
        this.today_missing_attendance = [];
        this.upcoming_birthday_employee = [];
        this.missing_attendance_count = '';
        this.today_check_in_check_out = [];
        this.today_check_in_check_out_count = '';
        this.today_time_off = [];
        this.upcoming_30_days_time_off = [];
        this.upcoming_30_days_time_off_count = '';
        this.today_date = '';
        this.end_date = '';

        onWillStart(async () => {
            const data = await this.orm.call('attendance.dashboard', 'get_dashboard_data', []);
            this.employee_count = data.employee_count;
            this.contract_count = data.contract_count;
            this.company_code_99a = data.company_code_99a;
            this.company_code_99s = data.company_code_99s;
            this.company_code_99x = data.company_code_99x;
            this.today_missing_attendance = data.today_missing_attendance;
            this.missing_attendance_count = data.missing_attendance_count;
            this.today_check_in_check_out = data.today_check_in_check_out;
            this.upcoming_birthday_employee = data.upcoming_birthday_employee;
            this.today_check_in_check_out_count = data.today_check_in_check_out_count;
            this.today_time_off = data.today_time_off;
            this.today_time_off_count = data.today_time_off_count;
            this.upcoming_30_days_time_off = data.upcoming_30_days_time_off;
            this.upcoming_30_days_time_off_count = data.upcoming_30_days_time_off_count;
            this.today_date = data.today_date;
            this.end_date = data.end_date;
        });
    }

    openEmployees() {
        this.action.doAction({
            name: 'All Employee',
            type: 'ir.actions.act_window',
            res_model: 'hr.employee',
            view_mode: 'tree,form',
            views: [[false, 'list'], [false, 'form']],
            view_id: 'hr.view_employee_form',
            target: 'current',
        });
    }

    openContracts() {
        this.action.doAction({
            name: 'Open Contracts',
            type: 'ir.actions.act_window',
            res_model: 'hr.contract',
            view_mode: 'tree,form',
            views: [[false, 'list'], [false, 'form']],  // Tree & Form view
            domain: [['state', '=', 'open']],  // Filter only 'running' contracts
            target: 'current',
        });
    }

    openAttendanceAnalysisReport() {
        this.action.doAction({
            name: 'Attendance Analysis',
            type: 'ir.actions.act_window',
            res_model: 'hr.attendance.report',
            view_mode: 'pivot',
            views: [[false, 'pivot']],
            target: 'current',
        });
    }

    openTimeOffAnalysisReport() {
        this.action.doAction({
            name: 'Time Off Analysis',
            type: 'ir.actions.act_window',
            res_model: 'hr.leave',
            view_mode: 'pivot',
            views: [[false, 'pivot']],
            target: 'current',
        });
    }
}

registry.category("actions").add("attendance_dashboard", AttendanceDashboard);