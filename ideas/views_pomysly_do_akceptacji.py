from .common_idea import BazaIdeaView
from django.shortcuts import redirect


class PomyslyDoAkceptacji(BazaIdeaView):
    template_name = "ideas_table.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(status_akceptacji__akceptacja="do akceptacji")
        return queryset.filter()

    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name="idea_viewer").exists():
            return redirect(self.login_url)
        return super().dispatch(request, *args, **kwargs)
