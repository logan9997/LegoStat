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
        {'value': 'graph_prices_new',
            'label': 'Average Price (New) (£)', 'colour': 'red'},
        {'value': 'graph_prices_used',
            'label': 'Average Price (Used) (£)', 'colour': 'blue'},
        {'value': 'graph_quantities_new',
            'label': 'Total Quantity (New)', 'colour': 'green'},
        {'value': 'graph_quantities_used',
            'label': 'Total Quantity (Used)', 'colour': 'yellow '},
    ]

    GRAPH_DATE_RANGE_BUTTONS = [
        {'value': 7, 'label': '1W'},
        {'value': 30, 'label': '1M'},
        {'value': 90, 'label': '3M'},
        {'value': 365, 'label': '1Y'},
        {'value': 99999, 'label': 'MAX'},
    ]


class SimilarItem:

    COLOURS = [
        'White', 'Gray', 'Red', 'Black', 'Sand', 'Brown', 'Nougat', 'Orange',
        'Yellow', 'Lime', 'Green', 'Olive', 'Bright', 'Blue', 'Violet', 'Purple',
        'Pink', 'Reddish', 'Neon', 'Silver', 'Tan', 'Chrome', 'Pearl'
    ]

    COMMON_WORDS = [
        'dark', 'light', 'with', 'the', 'inlcudes', 'large', 'small',
        'head', 'leg', 'legs', 'torso', 'arm', 'arms', 'printed', 'right', 'left',
        'without', 'hair', 'helmet', 'trans', 'colour', 'color', 'medium', 'armor',
        'cape', 'hat', 'waist', 'neck', 'eyes', 'bent', 'circular', 'scowl', 'toes',
        'markings', 'one', 'logo', 'plain', 'dual', 'sided', 'type', 'belt', 'pattern',
        'vest', 'pocket', 'cone', 'detail', 'hip', 'hips', 'trim', 'solid', 'semi', 'above',
        'below', 'robe', 'scar', 'anniversary', 'edition'
    ]
    COMMON_WORDS.extend(list(map(str.capitalize, COMMON_WORDS)))
    COMMON_WORDS.extend(COLOURS)

    MAX_MATHCES = 12

class Pages:

    MAX_PAGES = 10

    class ItemsPerPage:

        TRENDING_ITEMS = 30