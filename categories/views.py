from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import category
from .serializers import CategorySerializer


@api_view()
def categories(request):
    all_categories = category.objects.all()
    serializer = CategorySerializer(all_categories, many=True)
    return Response(
        {
            "categories": serializer.data,
        }
    )