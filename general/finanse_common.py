import django_filters


class BaseDateRangeFilterSet(django_filters.FilterSet):
    start_date = django_filters.DateFilter(
        field_name="needs__wymagana_data_realizacji", lookup_expr="gte", label="Od daty"
    )
    end_date = django_filters.DateFilter(
        field_name="needs__wymagana_data_realizacji", lookup_expr="lte", label="Do daty"
    )

    def filter_queryset(self, queryset):
        # Pobierz wartości start_date i end_date z zapytania
        start_date = self.form.cleaned_data.get("start_date")
        end_date = self.form.cleaned_data.get("end_date")

        if start_date and end_date:
            # Filtrowanie queryset w oparciu o wspólny zakres dat w powiązanych rekordach needs
            queryset = queryset.filter(
                needs__wymagana_data_realizacji__gte=start_date,
                needs__wymagana_data_realizacji__lte=end_date,
            ).distinct()
        return super().filter_queryset(queryset)

    class Meta:
        abstract = True  # Ustawienie klasy bazowej jako abstrakcyjnej
