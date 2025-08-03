from datetime import date, timedelta
from .models import Transaction

def get_weekly_summary(user, year, month):
    qs = Transaction.objects.filter(user=user, date__year=year, date__month=month)
    if not qs.exists():
        return []
    first_day = date(year, month, 1)
    if month == 12:
        last_day = date(year + 1, 1, 1) - timedelta(days=1)
    else:
        last_day = date(year, month + 1, 1) - timedelta(days=1)
    week_map = {}
    for tx in qs:
        iso_year, iso_week, iso_weekday = tx.date.isocalendar()
        if iso_week not in week_map:
            week_start = tx.date - timedelta(days=tx.date.weekday())
            week_end = week_start + timedelta(days=6)
            week_start = max(week_start, first_day)
            week_end = min(week_end, last_day)
            week_map[iso_week] = {
                'week': iso_week,
                'start_date': week_start,
                'end_date': week_end,
                'transactions': [],
            }
        week_map[iso_week]['transactions'].append(tx)
    week_summaries = []
    for week, info in sorted(week_map.items()):
        txs = info['transactions']
        summary = {'expense': 0, 'income': 0}
        for tx in txs:
            if tx.transaction_type == 'expense':
                summary['expense'] += tx.amount
            elif tx.transaction_type == 'income':
                summary['income'] += tx.amount
        categories = {}
        for tx in txs:
            cat = tx.category
            if cat.parent:
                parent = cat.parent
                parent_id = parent.id
                if parent_id not in categories:
                    categories[parent_id] = {
                        'id': parent.id,
                        'name': parent.name,
                        'type': parent.category_type,
                        'total': 0,
                        'children': {}
                    }
                if cat.id not in categories[parent_id]['children']:
                    categories[parent_id]['children'][cat.id] = {
                        'id': cat.id,
                        'name': cat.name,
                        'total': 0
                    }
                categories[parent_id]['children'][cat.id]['total'] += tx.amount
                categories[parent_id]['total'] += tx.amount
            else:
                if cat.id not in categories:
                    categories[cat.id] = {
                        'id': cat.id,
                        'name': cat.name,
                        'type': cat.category_type,
                        'total': 0,
                        'children': {}
                    }
                categories[cat.id]['total'] += tx.amount
        cat_list = []
        for cat in categories.values():
            children = list(cat['children'].values())
            cat_list.append({
                'id': cat['id'],
                'name': cat['name'],
                'type': cat['type'],
                'total': cat['total'],
                'children': children
            })
        week_summaries.append({
            'week': info['week'],
            'start_date': info['start_date'],
            'end_date': info['end_date'],
            'summary': summary,
            'categories': cat_list
        })
    return week_summaries 