import os
import re

from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Pin

from .serializers import pin_serializer
from sentence_transformers import SentenceTransformer
from PIL import Image
import faiss
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
import random


class Pins(APIView):
    def get(self, request):
        allPinsCount = Pin.objects.all().count()

        num = random.randint(0, allPinsCount-10)

        allPins = Pin.objects.all()[num:num + 10]

        all_responses_received = []

        for pin in allPins:
            image = str(pin.image)

            all_responses_received.append(
                {
                    'image': image, "slug": pin.slug,
                    "name": pin.name, "id": pin.id
                }
            )

        return JsonResponse(all_responses_received, safe=False)

    def post(self, request, *args, **kwargs):
        serializer = pin_serializer(data=request.data)
        if serializer.is_valid():
            name = serializer.validated_data.get('name').strip().lower()

            temporalSlug = name.strip().lower()

            temporal_name = re.sub("[$&+,;:=?@#|'<>.^*()%!\s+\"`]", "-", f'{temporalSlug}')

            new_product_slug = temporal_name + f'-{Pin.objects.all().count()}'

            pin = serializer.save(slug=new_product_slug)

            media_url = os.path.join(BASE_DIR, 'media')

            index = faiss.read_index(f"{media_url}/vector.index")

            model = SentenceTransformer(f"{media_url}/new_clip_model")

            images = [
                Image.open(f"{media_url}/{request.FILES['image'].name}"),
            ]

            embeddings = model.encode(images)

            index.add_with_ids(embeddings, [str(pin.id)])

            faiss.write_index(index, f"{media_url}/vector.index")

            sentence_index = faiss.read_index(f"{media_url}/sentence.index")

            sentence_model = SentenceTransformer(f"{media_url}/new_sentence_model")

            sentences = [name]

            sentence_embeddings = sentence_model.encode(sentences)

            sentence_index.add_with_ids(sentence_embeddings, [str(pin.id)])

            faiss.write_index(sentence_index, f"{media_url}/sentence.index")

            return Response({
                'status': f'saved'
            })
        else:
            return Response(serializer.errors)