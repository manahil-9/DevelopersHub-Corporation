from django.shortcuts import render
from .forms import ImageUploadForm
from .tflite_inference import get_prediction
from django.http import HttpResponse

def classify_image(request):
    prediction = None

    if request.method == 'POST' and request.FILES.get('image'):
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the uploaded image to the database
            uploaded_image = form.save()

            # Get the image file path
            image_path = uploaded_image.image.path

            # Define the model path (update this path as per your actual model location)
            model_path = "models\model_unquant.tflite"  # Ensure this is the correct path

            classes = ['Everyday Objects', 'Nature and Scenery', 'Animals and Miscellaneous'] 

            # Make the prediction using the image path and the model path
            prediction = get_prediction(image_path, model_path, classes)

            # Render the result
            return render(request, 'classify/result.html', {'prediction': prediction})

    else:
        form = ImageUploadForm()

    return render(request, 'classify/index.html', {'form': form})
