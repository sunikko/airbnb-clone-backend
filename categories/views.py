from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound
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
            if 'pk' in request.data:
                return Response({"error": "The 'pk' field should not be included in the request."}, status=status.HTTP_400_BAD_REQUEST)
            else:
                new_category = serializer.save() # call create() function on serializer
                return Response(
                    CategorySerializer(new_category).data
                )
        else:
            return Response(serializer.errors)


@api_view(["GET", "PUT"])
def categoryDetails(request, pk):
    try:
        category_obj = category.objects.get(pk=pk)
    except category_obj.DoesNotExist:
        raise NotFound

    if request.method == "GET":
        serializer = CategorySerializer(category_obj)
        return Response(serializer.data)
    elif request.method == "PUT":
        serializer = CategorySerializer(
            category_obj,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            updated_category = serializer.save()
            return Response(CategorySerializer(updated_category).data)
        else:
            return Response(serializer.errors)