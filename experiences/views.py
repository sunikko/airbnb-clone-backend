from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.status import HTTP_204_NO_CONTENT
from .models import Perk
from .serializers import PerkSerializer


class PerkListView(APIView):
    def get(self, request):
        all_experiences = Perk.objects.all()
        serializer = PerkSerializer(all_experiences, many=True)
        return Response(
            serializer.data,
        )
    
    def post(self, request):
        serializer = PerkSerializer(data=request.data)
        if serializer.is_valid():
            new_experience_obj = serializer.save()
            return Response(
                PerkSerializer(new_experience_obj).data
            )
        else:
            return Response(serializer.errors)
        

class PerkDetail(APIView):
    def get_object(self, pk):
        try:
            return Perk.objects.get(pk=pk)
        except Perk.DoesNotExist:
            raise NotFound
        
    def get(self, request, pk):
        serializer = PerkSerializer(self.get_object(pk))
        return Response(serializer.data)
    
    def put(self, request, pk):
        serializer = PerkSerializer(
            self.get_object(pk), 
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
             updated_obj = serializer.save()
             return Response(PerkSerializer(updated_obj).data)
        else:
            return Response(serializer.errors)
        
    def delete(self, request, pk):
        perk_obj = self.get_object(pk)
        perk_obj.delete()
        return Response(status=HTTP_204_NO_CONTENT)



