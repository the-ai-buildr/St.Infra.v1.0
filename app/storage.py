import datetime

from google.cloud import storage

from app.config import settings


def get_bucket() -> storage.Bucket:
    bucket_name = (settings.GCS_BUCKET_NAME or "").strip()
    if not bucket_name:
        raise RuntimeError(
            "GCS_BUCKET_NAME is not configured. Set app.config.settings.GCS_BUCKET_NAME "
            "before using Google Cloud Storage operations."
        )

    client = storage.Client(project=settings.GCP_PROJECT_ID or None)
    return client.bucket(bucket_name)


def upload_file(
    file_bytes: bytes,
    destination_blob: str,
    content_type: str = "application/octet-stream",
) -> str:
    """Upload bytes to GCS and return the gs:// URI."""
    bucket = get_bucket()
    blob = bucket.blob(destination_blob)
    blob.upload_from_string(file_bytes, content_type=content_type)
    return f"gs://{bucket.name}/{destination_blob}"


def get_signed_url(blob_name: str, expiry_minutes: int = 15) -> str:
    """Return a short-lived HTTPS download URL for a GCS object."""
    bucket = get_bucket()
    blob = bucket.blob(blob_name)
    return blob.generate_signed_url(
        version="v4",
        expiration=datetime.timedelta(minutes=expiry_minutes),
        method="GET",
    )
