from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import category
from .serializers import CategorySerializer


@api_view(["GET", "POST"])
def categories(request):
    if request.method == "GET":
        all_categories = category.objects.all()
        serializer = CategorySerializer(all_categories, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        category.objects.create(
            name=request.data["name"],
            kind=request.data["kind"],
        )
        return Response({"created": True})

@api_view()
def categoryDetails(reqest, pk):
    category_obj = category.objects.get(pk=pk)
    serializer = CategorySerializer(category_obj)
    return Response(serializer.data)