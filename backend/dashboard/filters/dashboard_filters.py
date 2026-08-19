class DashboardFilter:

    @staticmethod
    def apply_date_filter(queryset, field, year=None, month=None, day=None):

        filters = {}

        if year:
            filters[f"{field}__year"] = year

        if month:
            filters[f"{field}__month"] = month

        if day:

            if "-" in str(day):
                filters[field] = day

            else:
                filters[f"{field}__day"] = day

        return queryset.filter(**filters)