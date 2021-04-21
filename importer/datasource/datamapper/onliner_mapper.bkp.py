onliner_mapper = {
    'name': 'onliner',
    'mapper_type': 'json',
    'mapper': {
        'collection': 'adverts',
        'item': {
            'external_id': 'id',
            'car': 'manufacturer.name',
            'model': 'model.name',
            'generation': 'generation.name',
            'released': 'specs.year',
            'color': 'specs.color',
            'engine.capacity': 'specs.engine.capacity',
            'engine.type': 'specs.engine.type',
            'engine.is_hybrid': 'specs.hybrid',
            'transmission': 'specs.transmission',
            'drivetrain': 'specs.drivetrain',
            'odometer.val': 'specs.odometer.value',
            'odometer.uom': 'specs.odometer.unit',
            'seller.name': 'seller.name',
            'seller.phones': 'seller.phones',
            'price.amount': 'price.amount',
            'price.currency': 'price.currency',
            'location': 'location.city.name',
            'images': 'images',
            'original_link': 'html_url',
        }
    }
}