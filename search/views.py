import os
import re

from asgiref.sync import async_to_sync, sync_to_async
from django.http import JsonResponse, HttpResponse
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from pins.models import Pin
from sentence_transformers import SentenceTransformer
from PIL import Image
import faiss
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


class Search(APIView):
    def post(self, request, *args, **kwargs):
        if request.FILES.get("image") is not None:
            file = request.FILES['image']

            media_url = os.path.join(BASE_DIR, 'media')

            index = faiss.read_index(f"{media_url}/vector.index")

            model = SentenceTransformer(f"{media_url}/new_clip_model")

            img = Image.open(file)

            k = 8

            query_vector = model.encode([img])

            D, I = index.search(query_vector, k)

            all_responses_received = []

            for e in I[0]:
                if e != -1:
                    pin = Pin.objects.get(id=e)

                    image = str(pin.image)

                    all_responses_received.append(
                        {
                            'image': image, 'name': pin.name,
                            'slug': pin.slug
                        }
                    )

            return JsonResponse(all_responses_received, safe=False)
        else:
            return Response({
                'status': 'incomplete'
            })


@sync_to_async
@async_to_sync
async def wordSearch(request, slug):
    sentence = re.sub("-", " ", slug.strip().lower())

    # isEnglish = await check_language(sentence)
    #
    # if isEnglish:
    #     pass
    # else:
    #     sentence = await translate_sentence(sentence)

    media_url = os.path.join(BASE_DIR, 'media')

    index = faiss.read_index(f"{media_url}/vector.index")

    model = SentenceTransformer(f"{media_url}/new_clip_model")

    k = 8

    query_vector = model.encode([sentence])

    D, I = index.search(query_vector, k)

    all_responses_received = []

    for e in I[0]:
        if e != -1:
            pin = await get_pin(e)

            image = str(pin.image)

            all_responses_received.append(
                {
                    'image': image, 'name': pin.name,
                    'slug': pin.slug
                }
            )

    return JsonResponse(all_responses_received, safe=False)


@sync_to_async
def check_language(sentence):
    from google.cloud import translate_v2 as translate

    media_url = os.path.join(BASE_DIR, 'media')

    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = f"{media_url}/googlekey.json"

    translate_client = translate.Client()

    result = translate_client.detect_language(sentence)

    if result["language"] != "en":
        return False
    else:
        return True


@sync_to_async
def translate_sentence(sentence):
    from google.cloud import translate_v2

    media_url = os.path.join(BASE_DIR, 'media')

    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = f"{media_url}/googlekey.json"

    translate_client = translate_v2.Client()

    text = sentence

    target = "en"

    output = translate_client.translate(text, target_language=target)

    return output["translatedText"]


@sync_to_async
def get_pin(id):
    return Pin.objects.get(id=id)