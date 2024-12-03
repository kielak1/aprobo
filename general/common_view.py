from django.http import HttpRequest, HttpResponse


def get_current_url(request: HttpRequest) -> str:
    # Uzyskanie bieżącego adresu URL
    current_url = request.build_absolute_uri()
    return current_url
