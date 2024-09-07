from hashlib import md5

from PIL import Image
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.generics import CreateAPIView, DestroyAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from images.models import RecipeImage
from images.permissions import IsImageOwner
from images.serializers import ImageSerializer


@extend_schema_view(
    post=extend_schema(
        request={
            "multipart/form-data": {
                "type": "object",
                "properties": {
                    "recipe_id": {"type": "string"},
                    "image_path": {"type": "string", "format": "binary"},
                },
            }
        },
        responses={
            201: ImageSerializer,
        },
    ),
)
class ImageCreateAPIView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ImageSerializer
    parser_classes = (MultiPartParser, FormParser)

    def perform_create(self, serializer):
        image = serializer.validated_data.get("image_path")
        with Image.open(image) as img:
            hash_md5 = md5(img.tobytes()).hexdigest()
        serializer.save(
            hash_md5=hash_md5,
            image_size=image.size,
            created_by=self.request.user
        )


class ImageDeleteAPIView(DestroyAPIView):
    permission_classes = (IsAuthenticated, IsAdminUser | IsImageOwner)
    serializer_class = ImageSerializer
    parser_classes = (MultiPartParser, FormParser)
    queryset = RecipeImage.objects.filter(is_deleted=False)
    lookup_url_kwarg = "recipe_pk"

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()
