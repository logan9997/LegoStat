import psycopg2 
from environment_manager import Manager
from datetime import datetime as dt
from config import Date
from utils import item_type_convert
from psycopg2.errors import UniqueViolation

class DB:

    def __init__(self) -> None:
        self.con = psycopg2.connect(**Manager().get_database_credentials('psycopg2'))
        self.cursor = self.con.cursor()

    def clean_data(Self, data:dict):
        for k, v in data.items():
            if type(v) == str:
                data[k] = v.replace("'", '')

    def insert_item(self, data:dict):
        self.clean_data(data)
        sql = f'''
        INSERT INTO "App_item" VALUES (
            '{data['no']}',
            '{data['name']}',
            {data['year_released']},
            '{item_type_convert(data['type'])}',
            0
        )
        '''
        try:
            self.cursor.execute(sql)
            self.con.commit()
        except UniqueViolation:
            self.con.close()

    def insert_price_info(self, data:dict):
        self.clean_data(data)
        sql = f'''
        INSERT INTO "App_price"(date, condition, avg_price, total_quantity, item_id) VALUES (
            '{dt.today().strftime(Date.DATE_FORMAT)}',
            '{data['new_or_used']}',
            {round(float(data['avg_price']), 2)},
            '{data['total_quantity']}',
            '{data['item']['no']}'
        )
        '''
        self.cursor.execute(sql)
        self.con.commit()

    def get_ids(self):
        sql = '''
        SELECT item_id
        FROM "App_item"
        '''
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return [row[0] for row in result]
    
    def get_item_type(self, item_id):
        sql = f'''
        SELECT item_type
        FROM "App_item"
        WHERE item_id = '{item_id}'
        '''
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result[0][0]