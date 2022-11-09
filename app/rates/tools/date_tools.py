import datetime

import pandas as pd


class DateTools:
    def get_business_days_range(self, start_date, end_date):
        """
        start_date and end_date: can be str ('YYYY-mm-dd') or a date
        (Timestamp).
        return: a list of business days (Timestamps) in the given range
        """

        days = pd.bdate_range(start_date, end_date)
        list_days = days.tolist()
        return [dates.date() for dates in list_days]

    def check_isvalid_range_date(self, start_date, end_date):
        """
        start_date: str indicating date ('YYYY-mm-dd')
        end_date: str indicating date ('YYYY-mm-dd')

        return: True if start_date is earlier than end_date else return False
        """
        start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()

        if start_date < end_date:
            return True
        return False

    def check_end_date_is_up_today(self, end_date):
        """
        end_date: str indicating date ('YYYY-mm-dd')

        return: True if end_date is earlier or equal than today
        else return False
        """

        end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
        today = datetime.datetime.now().date()

        if today < end_date:
            return False
        return True
