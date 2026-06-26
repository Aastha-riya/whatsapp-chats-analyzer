import pandas as pd
import re
def preprocessor(data):
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}(?:\s|\u202f)*(?:AM|PM)\s-\s'
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    df = pd.DataFrame({
    'user_message': messages,
    'message_date': dates
    })

    df['message_date'] = pd.to_datetime(
        df['message_date'],
        format='%m/%d/%y, %I:%M %p - '
    )

    df.rename(columns={'message_date': 'date'}, inplace=True)
    df['only_date'] = df['date'].dt.date
    df['month_num'] = df['date'].dt.month

    users = []
    messages = []

    for message in df['user_message']:
        if ': ' in message:
            user, msg = message.split(': ', 1)
            users.append(user)
            messages.append(msg)
        else:
            users.append('group_notification')
            messages.append(message)
    df['user'] = users
    df['message'] = messages

    df.drop(columns=['user_message'], inplace=True)

    df['day_name'] = df['date'].dt.day_name()
    df['day']=df['date'].dt.day
    df['month'] =df['date'].dt.month_name()
    df['year']= df['date'].dt.year
    df['hour']=df['date'].dt.hour
    df['minute']=df['date'].dt.minute
    df['am_pm'] = df['date'].dt.strftime('%p')

    period = []
    for hour in df['hour']:
        start = hour
        end = (hour + 1) % 24
        period.append(f"{start:02d}-{end:02d}")

    df['period'] = period

    return df
