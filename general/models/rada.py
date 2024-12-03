from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from ideas.models import Ideas
from needs.models import Needs


class MeetingStatus(models.Model):
    status = models.CharField(max_length=20)

    def __str__(self):
        return self.status


class Meeting(models.Model):
    meeting_status = models.ForeignKey(
        MeetingStatus, on_delete=models.PROTECT, null=True
    )
    general_resolution = models.CharField(
        max_length=5000, null=True, blank=True, default=""
    )
    meeting_date = models.DateField(default=timezone.now, null=True)
    creation_date = models.DateField(default=timezone.now, null=True)
    # Users invited to the meeting
    invitations = models.ManyToManyField(
        User, related_name="meeting_invitations", blank=True
    )

    # Users who attended the meeting
    attendance_list = models.ManyToManyField(
        User, related_name="meeting_attendance", blank=True
    )

    # Ideas and needs discussed in the meeting (through Resolution)
    discussed_ideas = models.ManyToManyField(
        Ideas, related_name="meeting_ideas", through="Resolution", blank=True
    )
    discussed_needs = models.ManyToManyField(
        Needs, related_name="meeting_needs", through="Resolution", blank=True
    )

    # Sorting fields
    sort_field = models.CharField(
        max_length=50,
        choices=[
            ("id", "ID"),
            ("section", "Sekcja"),
            ("client", "Klient"),
        ],
        default="id",
    )
    sort_order = models.CharField(
        max_length=4,
        choices=[
            ("asc", "Rosnąco"),
            ("desc", "Malejąco"),
        ],
        default="asc",
    )

    def __str__(self):
        return f"{self.meeting_date.strftime('%Y-%m-%d')} - Postanowienia: {self.general_resolution[:50]}..."  # Trimming long resolution


class Resolution(models.Model):
    meeting = models.ForeignKey(
        Meeting, on_delete=models.CASCADE, related_name="resolutions"
    )
    idea = models.ForeignKey(
        Ideas,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="idea_resolutions",
    )
    need = models.ForeignKey(
        Needs,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="need_resolutions",
    )
    resolution_text = models.TextField(null=True, blank=True, default="")

    def __str__(self):
        subject = self.idea or self.need or "Unknown"
        return f"Postanowienie dla {subject} na posiedzeniu {self.meeting}"

    def clean(self):
        if not self.idea and not self.need:
            raise ValidationError(
                "Resolution must be related to either an Idea or a Need."
            )
