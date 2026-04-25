from pathlib import Path

from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand

from portfolio.models import AboutSection, Blog, HomeSection, Project
from portfolio.storage import cloudinary_media_enabled, get_image_storage, get_raw_storage


class Command(BaseCommand):
    help = "Upload tracked local media files to Cloudinary and update model file paths."

    def handle(self, *args, **options):
        if not cloudinary_media_enabled():
            self.stdout.write(self.style.WARNING("Cloudinary is not enabled. Skipping media sync."))
            return

        image_storage = get_image_storage()
        raw_storage = get_raw_storage()
        media_root = Path(settings.MEDIA_ROOT)

        synced = 0

        synced += self._sync_queryset(HomeSection.objects.exclude(hero_image=""), "hero_image", image_storage, media_root)
        synced += self._sync_queryset(Project.objects.exclude(image=""), "image", image_storage, media_root)
        synced += self._sync_queryset(Blog.objects.exclude(image=""), "image", image_storage, media_root)
        synced += self._sync_queryset(AboutSection.objects.exclude(cv_file=""), "cv_file", raw_storage, media_root)

        self.stdout.write(self.style.SUCCESS(f"Cloudinary media sync complete. Updated {synced} file(s)."))

    def _sync_queryset(self, queryset, field_name, storage, media_root: Path):
        updated = 0

        for obj in queryset:
            field = getattr(obj, field_name)
            if not field:
                continue

            relative_name = field.name
            local_path = media_root / relative_name

            if not local_path.exists():
                continue

            with local_path.open("rb") as source:
                saved_name = storage.save(relative_name, File(source, name=local_path.name))

            if saved_name != relative_name:
                setattr(obj, field_name, saved_name)
            obj.save(update_fields=[field_name])
            updated += 1

        return updated
