{
    'name' : 'hospital management',
    'version' : '1.2',
    'summary': 'hospital management software',
    'sequence': -100,
    'description': """hospital management software""",
    'license': 'LGPL-3',
    'category': 'Productivity',
    'website': '',
    'images' : [],
    'depends' : [
        'hr',
        'mail',
        'sale'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/patient.xml',
        'views/sale.xml'
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
