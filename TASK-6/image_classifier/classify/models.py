from django.db import models

class ImageUpload(models.Model):
    image = models.ImageField(upload_to='uploads/')  # 'uploads/' stores the images in a subfolder inside 'media'
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image {self.id} uploaded on {self.uploaded_at}"


