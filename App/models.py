from django.db import models
from config import ModelValidations as MV
from utils import clean_html_codes
from django.utils import timezone

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=MV.Lengths.USERNAME)
    password = models.CharField(max_length=MV.Lengths.PASSWORD)

class Item(models.Model):
    item_id = models.CharField(primary_key=True, max_length=MV.Lengths.ITEM_ID)
    item_name = models.CharField(max_length=MV.Lengths.ITEM_NAME)
    year_released = models.IntegerField()
    item_type = models.CharField(max_length=MV.Lengths.ITEM_TYPE, choices=(MV.Choices.ITEM_TYPE))
    views = models.IntegerField()

class Portfolio(models.Model):
    entry_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    date_added = models.DateField(default=timezone.now)
    date_bought = models.DateField(null=True, blank=True)
    date_sold = models.DateField(null=True, blank=True)
    bought_for = models.FloatField(null=True, blank=True, default=0)
    sold_for = models.FloatField(null=True, blank=True, default=0)
    notes = models.CharField(max_length=MV.Lengths.NOTES)
    condition = models.CharField(max_length=MV.Lengths.CONDITION, choices=(MV.Choices.CONDITION))


class Watchlist(models.Model):
    entry_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)   

class Theme(models.Model):
    entry_id = models.AutoField(primary_key=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    theme_path = models.CharField(max_length=MV.Lengths.THEME_PATH)


class Price(models.Model):
    record_id = models.AutoField(primary_key=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    date = models.DateField()
    condition = models.CharField(max_length=MV.Lengths.CONDITION, choices=(MV.Choices.CONDITION))
    avg_price = models.FloatField()
    total_quantity = models.IntegerField()

class SetItem(models.Model):
    entry_id = models.AutoField(primary_key=True)
    figure = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='figure_id')
    set = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='set_id')