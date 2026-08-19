from datetime import date


class ChartFormatter:
    @staticmethod
    def monthly_chart(data_dict, year):

        labels = []
        data = []

        for month in range(1, 13):
            labels.append(date(int(year), month, 1).strftime("%b"))

            data.append(data_dict.get(month, 0))

        return labels, data

    @staticmethod
    def single_month_chart(month, value):

        labels = [date(date.today().year, int(month), 1).strftime("%b")]

        data = [value]

        return labels, data
