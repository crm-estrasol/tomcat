from odoo import api, fields, models
from odoo.addons.website.tools import get_video_embed_code
import logging
_logger = logging.getLogger(__name__)
class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    limit_days = fields.Integer("Dias cambio semaforo")
   
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        _logger.info("-----------------------------------"+str(self.env['ir.config_parameter'].sudo().get_param('intelli.pdf_m')))
        res.update(
            limit_days = self.env['ir.config_parameter'].sudo().get_param('intelli.limit_days'),    
        )
        return res
    
    def set_values(self):
        super(ResConfigSettings, self).set_values()
        param = self.env['ir.config_parameter'].sudo()
        limit_days = self.limit_days or False 
        param.set_param('intelli.limit_days', limit_days)
       