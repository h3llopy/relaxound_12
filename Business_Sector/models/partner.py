# -*- coding: utf-8 -*-
# Copyright 2016-TODAY Serpent Consulting Services Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _
import csv

class BusinessSector(models.Model):

        _inherit = 'res.partner'

        # Added one field Business sector with dropdown
	
        business_sec = fields.Selection([
                ('sec1', 'Beauty / Wellness'),
                ('sec2', 'Books'), 
                ('sec3', 'Gardening'),
                ('sec4', 'Gastronomy'),
                ('sec5', 'Art / Culture'),
                ('sec6', 'Home Living'),
                ('sec7', 'Misc'),
                ('sec8', 'GPC'),
                ('sec9', 'retail store'),], string='Business Sector:')
        
        agent_name = fields.Char('Sale Agent')

        @api.onchange('zip')
        def onchange_zip(self):
                if self.zip != None and self.zip != '':
                        with open('src/zip_code.csv', 'r') as csv_file:
                                csv_obj = csv.reader(csv_file)
                                print("#### CSV OPENED #########")
                                all_val = [i for i in csv_obj]
                                for row in all_val:
                                        if self.zip in row:
                                                self.update({'agent_name': row[1]})
                                # else:
                                #         self.update({'agent_name': ''})

                elif self.zip == '':
                        self.update({'agent_name': None})
                else:
                        self.update({'agent_name': None})




