# -*- coding: utf-8 -*-
import datetime

from odoo import api, fields, models


class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "hospital patient"

    name = fields.Char(string='Name', required=True)
    age = fields.Integer(string='Age')
    gender = fields.Selection([
        ('male', 'male'),
        ('female', 'female'),
        ('other', 'other'),
    ], required=True, default='male', )
    note = fields.Text(string='Description')
    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirmed'),
                              ('done', 'Done'), ('cancel', 'Canceled')], default='draft', string="status", copy=False)
    active = fields.Boolean(string="Active", default=True)

    date1 = fields.Date(string="Start Date", required=True, )
    date2 = fields.Date(string="End Date", required=True, )
    compared_date = fields.Char(string="Time Left", compute='compare')

    def compare(self):
        delta = self.date2 - self.date1
        self.compared_date = delta

    def send_activity(self):
        delta = self.date2 - self.date1
        hr_personal = self.env.ref('hr.group_hr_user').users
        for user in hr_personal:
            if delta.days < 90:
                self.env['mail.activity'].sudo().create({'res_id': self.id,
                                                         'summary': f'{delta} Left',
                                                         'res_model_id': self.env['ir.model'].search(
                                                             [('model', '=', 'hospital.patient')], limit=1).id,
                                                         'activity_type_id': self.env.ref(
                                                             'mail.mail_activity_data_todo').id,
                                                         'user_id': user.id,
                                                         })
    def confirm(self):
        if self.state == 'draft':
            self.state = 'confirm'
    def confirm_manger(self):
        if self.state == 'confirm':
            self.state = 'confirm_manger'
    def confirm_user(self):
        if self.state == 'confirm_manger':
            self.state = 'confirm_user'
    def done(self):
        if self.state == 'confirm_user':
            self.state = 'done'


class stateadded(models.Model):
    _inherit = "hospital.patient"

    state = fields.Selection(
        selection_add=[('confirm_manger', 'Confirm Manger'), ('confirm_user', 'Confirm User'), ('done',)])
