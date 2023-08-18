class ModelValidations:

    class Lengths:
        USERNAME = 20
        PASSWORD = 20
        ITEM_ID = 30
        ITEM_NAME = 250
        ITEM_TYPE = 1
        CONDITION = 1
        THEME_PATH = 150
        NOTES = 215

    class Choices:
        ITEM_TYPE = ('M', 'M'), ('S', 'S')
        CONDITION = ('U', 'U'), ('N', 'N')


class Date:

    DATE_FORMAT = '%Y-%m-%d'


class Forms:
    pass


class Options:
    
    GRAPH_METRICS = [
        {'value':'graph_prices_new', 'label':'Average Price (New) (£)', 'colour':'red'},
        {'value':'graph_prices_used', 'label':'Average Price (Used) (£)', 'colour':'blue'},
        {'value':'graph_quantities_new', 'label':'Total Quantity (New)', 'colour':'green'},
        {'value':'graph_quantities_used', 'label':'Total Quantity (Used)', 'colour':'yellow '},
    ]

