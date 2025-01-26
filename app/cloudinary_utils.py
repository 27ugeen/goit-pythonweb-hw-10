import cloudinary
import cloudinary.uploader
import cloudinary.api
from settings import settings

cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET,
    secure=True
)

def upload_avatar(file, public_id):
    response = cloudinary.uploader.upload(
        file.file,
        folder="avatars/",
        public_id=public_id,
        overwrite=True,
        resource_type="image"
    )
    return response.get("secure_url")