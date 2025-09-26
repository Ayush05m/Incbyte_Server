import cloudinary.uploader

async def upload_image(file_content: bytes, public_id: str = None):
    try:
        upload_result = cloudinary.uploader.upload(file_content, public_id=public_id)
        return upload_result['secure_url']
    except Exception as e:
        print(f"Error uploading image to Cloudinary: {e}")
        return None
