from django.shortcuts import render
from django.core.handlers.wsgi import WSGIRequest
from db import DB
from config import Date, Pages
from utils import (
    timer, GraphData, condence_pages, 
    validate_page, condition_covert
)
from ..models import Price, Item

@timer
def trending(request:WSGIRequest):

    if 'metric_filter' not in request.session:
        request.session['metric_filter'] = 'avg_price__N'

    if 'winners_losers_filter' not in request.session:
        request.session['winners_losers_filter'] = 'ALL'

    if 'item_type_filter' not in request.session:
        request.session['item_type_filter'] = 'ALL'

    metric_filter:str = request.session.get('metric_filter', 'avg_price__N').split('__')
    metric = metric_filter[0]
    condition = metric_filter[1]
    
    trending_items:list[dict] = DB().get_trending_items(
        condition=condition, metric=metric, 
        select_fields=('item_id', 'item_type', 'metric_change')
    )

    item_type_filter = request.session.get('item_type_filter', 'ALL')
    if item_type_filter != 'ALL':
        trending_items = list(filter(
            lambda x: x['item_type'] == item_type_filter, trending_items
        ))

    winners_loser_filter = request.session.get('winners_losers_filter', 'ALL')
    if winners_loser_filter != 'ALL':
        if winners_loser_filter == 'winners':
            trending_items = list(filter(
                lambda x: x['metric_change'] > 0, trending_items
            ))
        else:
            trending_items = list(filter(
                lambda x: x['metric_change'] < 0, trending_items
            ))

    current_page = int(request.session.get('current_page', 1))
    number_of_pages = len(trending_items) // Pages.ItemsPerPage.TRENDING_ITEMS
    pages = [page + 1 for page in range(number_of_pages)]
    current_page = validate_page(pages, current_page)
    pages = condence_pages(pages, current_page)

    trending_items = trending_items[
        Pages.ItemsPerPage.TRENDING_ITEMS * (current_page - 1) : 
        Pages.ItemsPerPage.TRENDING_ITEMS * current_page
    ]

    graph_metric = metric + '_' + condition_covert(condition)
    selected_date_range = int(request.session.get('graph_range', 99999))

    for item in trending_items:
        
        item['item_name'] = Item.objects.filter(
            item_id=item['item_id']).values_list('item_name', flat=True
        )[0]

        item['avg_price_new'] = Price.objects.filter(
            item_id=item['item_id'], condition='N'
        ).latest('date').avg_price

        item['avg_price_used'] = Price.objects.filter(
            item_id=item['item_id'], condition='U'
        ).latest('date').avg_price

        item['total_quantity_new'] = Price.objects.filter(
            item_id=item['item_id'], condition='N'
        ).latest('date').total_quantity

        item['total_quantity_used'] = Price.objects.filter(
            item_id=item['item_id'], condition='U'
        ).latest('date').total_quantity

        graph_data = GraphData(Price, item['item_id'], date_range=selected_date_range)
        item.update(graph_data.get_metrics())
        item['graph_dates'] = graph_data.get_dates()

        least_recent_metric_entry = item['graph_' + graph_metric][0]
        if least_recent_metric_entry != 0:
            most_recent_metric_entry = item['graph_' + graph_metric][-1]
            item['metric_percentage_change'] = round(
                (least_recent_metric_entry - most_recent_metric_entry) / 
                least_recent_metric_entry * -100
                ,2
            )
        else:
            item['metric_percentage_change'] = 100

    trending_items = sorted(
        trending_items, 
        key=lambda x : abs(x['metric_percentage_change']), 
        reverse=True
    )

    context = {
        'trending_items':trending_items,
        'metrics':[graph_metric],
        'pages':pages,
        'current_page':current_page,
        'selected_date_range':selected_date_range
    }

    return render(request, 'App/trending.html', context=context)