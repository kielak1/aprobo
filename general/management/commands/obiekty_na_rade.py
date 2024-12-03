from django.core.management.base import BaseCommand
from ideas.models import Ideas, StatusIdei
from needs.models import Needs, StatusNeed
import logging

# Set up logging
logger = logging.getLogger("avantic")


class Command(BaseCommand):
    help = "Jeśli brakuje co najmniej dwóch obiektów Needs i Ideas o statusie rada architektury, ustawia takie statusy dla dostępnych obiektów."

    def handle(self, *args, **kwargs):
        try:
            # Sprawdzanie obiektów Needs
            needs_rada_count = Needs.objects.filter(
                status_potrzeby__status="rada architektury"
            ).count()
            if needs_rada_count < 2:
                needs_to_update = Needs.objects.exclude(
                    status_potrzeby__status="rada architektury"
                )[: 2 - needs_rada_count]
                status_rada = StatusNeed.objects.get(status="rada architektury")
                for need in needs_to_update:
                    need.status_potrzeby = status_rada
                    need.status_akceptacji.status = "niegotowe"
                    need.save()
                    logger.info(
                        f'Need with id {need.id} has been updated to "rada architektury" and "niegotowe".'
                    )
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"Need with id {need.id} has been updated successfully."
                        )
                    )
            else:
                logger.info(
                    'There are already at least 2 Needs with status "rada architektury".'
                )
                self.stdout.write(
                    self.style.SUCCESS(
                        'There are already at least 2 Needs with status "rada architektury".'
                    )
                )

            # Sprawdzanie obiektów Ideas
            ideas_rada_count = Ideas.objects.filter(
                status_idei__status="rada architektury"
            ).count()
            if ideas_rada_count < 2:
                ideas_to_update = Ideas.objects.exclude(
                    status_idei__status="rada architektury"
                )[: 2 - ideas_rada_count]
                status_rada = StatusIdei.objects.get(status="rada architektury")
                for idea in ideas_to_update:
                    idea.status_idei = status_rada
                    idea.status_akceptacji.status = "niegotowe"
                    idea.save()
                    logger.info(
                        f'Idea with id {idea.id} has been updated to "rada architektury" and "niegotowe".'
                    )
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"Idea with id {idea.id} has been updated successfully."
                        )
                    )
            else:
                logger.info(
                    'There are already at least 2 Ideas with status "rada architektury".'
                )
                self.stdout.write(
                    self.style.SUCCESS(
                        'There are already at least 2 Ideas with status "rada architektury".'
                    )
                )

        except Exception as e:
            # Log the error
            logger.error(f"An error occurred: {e}", exc_info=True)
            self.stdout.write(self.style.ERROR(f"An error occurred: {e}"))
