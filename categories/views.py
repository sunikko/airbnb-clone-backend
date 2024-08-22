from rest_framework import status
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
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            # category.objects.create(
            #     name=request.data["name"],
            #     kind=request.data["kind"],
            # )
            if 'pk' in request.data:
                return Response({"error": "The 'pk' field should not be included in the request."}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"created": True})
        else:
            return Response(serializer.errors)

@api_view()
def categoryDetails(reqest, pk):
    category_obj = category.objects.get(pk=pk)
    serializer = CategorySerializer(category_obj)
    return Response(serializer.data)