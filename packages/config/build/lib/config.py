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

    DATE_FORMAT = '%Y/%m/%d'