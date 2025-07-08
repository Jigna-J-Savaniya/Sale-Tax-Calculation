{
    'name': 'Sale Tax Calculations',
    'version': '17.0.1.0.0',
    'category': 'Customizations',
    'summary': 'Adds tax breakdown by rate in sale order.',

    'depends': ['sale', 'account'],

    'data': [
        'security/ir.model.access.csv',
        'views/sale_order_views.xml',
    ],

    "installable": True,
    "application": False

}
