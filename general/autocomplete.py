from dal import autocomplete

from general.models import uslugi, zlecenia_kontrolingowe, Crip, Rodzaje_uslug
from ideas.models import Ideas
from needs.models import Needs

from django.contrib.auth.models import User


class UslugiAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = uslugi.objects.all()
        if self.q:
            qs = qs.filter(numer__icontains=self.q)
        return qs[:30]


class ZleceniaAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = zlecenia_kontrolingowe.objects.all()
        if self.q:
            qs = qs.filter(numer__icontains=self.q)
        return qs[:30]


class InvitationsAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = User.objects.all()
        if self.q:
            qs = qs.filter(username__icontains=self.q)
        return qs[:20]


class AttendanceAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = User.objects.all()
        if self.q:
            qs = qs.filter(username__icontains=self.q)
        return qs[:20]


class DiscussedIdeasAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Ideas.objects.all()
        if self.q:
            qs = qs.filter(id__icontains=self.q)
        return qs[:40]


class DiscussedNeedsAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Needs.objects.all()
        if self.q:
            qs = qs.filter(id__icontains=self.q)
        return qs[:40]


class CripsAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Crip.objects.all()
        if self.q:
            qs = qs.filter(crip_id__icontains=self.q)
        return qs[:40]

class RodzajeUslugAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Rodzaje_uslug.objects.all()
        if self.q:
            qs = qs.filter(usluga__icontains=self.q)
        return qs[:40]

