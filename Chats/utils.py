from datetime import datetime, timedelta

def categorize_messages(messages):
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    day_before_yesterday = today - timedelta(days=2)

    categorized_messages = {
        'today': [],
        'yesterday': [],
        f'{day_before_yesterday.strftime("%Y-%m-%d")}': []
    }

    for message in messages:
        sent_time = datetime.strptime(message['create_at'], '%Y-%m-%dT%H:%M:%S.%f%z').date()

        if sent_time == today:
            categorized_messages['today'].append(message)
        elif sent_time == yesterday:
            categorized_messages['yesterday'].append(message)
        elif sent_time == day_before_yesterday:
            categorized_messages[f'{day_before_yesterday.strftime("%Y-%m-%d")}'].append(message)

    return categorized_messages


