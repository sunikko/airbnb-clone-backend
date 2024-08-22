from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import category
from .serializers import CategorySerializer


class Categories(APIView):
    def get(self, request):
        all_categories = category.objects.all()
        serializer = CategorySerializer(all_categories, many=True)
        return Response(serializer.data)
    
    def post(self, request):
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


class CategoryDetail(APIView):
    def get_object(self, pk):
        try:
            category_obj = category.objects.get(pk=pk)
            return category_obj
        except category_obj.DoesNotExist:
            return NotFound

    def get(self, request, pk):
        serializer = CategorySerializer(self.get_object(pk))
        return Response(serializer.data)
    
    def put(self, request, pk):
        serializer = CategorySerializer(
            self.get_object(pk),
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            updated_category = serializer.save()
            return Response(CategorySerializer(updated_category).data)
        else:
            return Response(serializer.errors)
        
    def delete(self, request, pk):
        self.get_object(pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)