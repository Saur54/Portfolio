import os
from importlib.util import find_spec

from django.conf import settings
from django.core.files.storage import FileSystemStorage, Storage
from django.utils.deconstruct import deconstructible


def _cloudinary_packages_available() -> bool:
    return find_spec("cloudinary") is not None and find_spec("cloudinary_storage") is not None


def _cloudinary_credentials_configured() -> bool:
    cloudinary_url = os.getenv("CLOUDINARY_URL")
    if cloudinary_url:
        return True

    return all(
        [
            os.getenv("CLOUDINARY_CLOUD_NAME"),
            os.getenv("CLOUDINARY_API_KEY"),
            os.getenv("CLOUDINARY_API_SECRET"),
        ]
    )


def cloudinary_media_enabled() -> bool:
    return _cloudinary_packages_available() and _cloudinary_credentials_configured()


def _build_local_media_storage() -> FileSystemStorage:
    return FileSystemStorage(location=settings.MEDIA_ROOT, base_url=settings.MEDIA_URL)


@deconstructible
class _BaseHybridMediaStorage(Storage):
    def __init__(self):
        self._local_storage = _build_local_media_storage()
        self._cloud_storage = None

        if cloudinary_media_enabled():
            self._cloud_storage = self._build_cloudinary_storage()

    def _build_cloudinary_storage(self):
        raise NotImplementedError

    def _read_storage(self, name):
        if self._cloud_storage is not None:
            try:
                if self._cloud_storage.exists(name):
                    return self._cloud_storage
            except Exception:
                pass

        if self._local_storage.exists(name):
            return self._local_storage

        return self._cloud_storage or self._local_storage

    def _write_storage(self):
        return self._cloud_storage or self._local_storage

    def open(self, name, mode="rb"):
        return self._read_storage(name).open(name, mode)

    def save(self, name, content, max_length=None):
        return self._write_storage().save(name, content, max_length=max_length)

    def exists(self, name):
        if self._cloud_storage is not None:
            try:
                if self._cloud_storage.exists(name):
                    return True
            except Exception:
                pass

        return self._local_storage.exists(name)

    def delete(self, name):
        storage = self._read_storage(name)
        if storage is not None:
            storage.delete(name)

    def size(self, name):
        return self._read_storage(name).size(name)

    def url(self, name):
        return self._read_storage(name).url(name)

    def path(self, name):
        storage = self._read_storage(name)
        return storage.path(name)

    def get_valid_name(self, name):
        return self._write_storage().get_valid_name(name)

    def generate_filename(self, filename):
        return self._write_storage().generate_filename(filename)


class HybridImageStorage(_BaseHybridMediaStorage):
    def _build_cloudinary_storage(self):
        from cloudinary_storage.storage import MediaCloudinaryStorage

        return MediaCloudinaryStorage()


class HybridRawStorage(_BaseHybridMediaStorage):
    def _build_cloudinary_storage(self):
        from cloudinary_storage.storage import RawMediaCloudinaryStorage

        return RawMediaCloudinaryStorage()


def get_image_storage():
    return HybridImageStorage()


def get_raw_storage():
    return HybridRawStorage()
