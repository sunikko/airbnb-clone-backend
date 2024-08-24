from rest_framework.views import APIView
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, NotAuthenticated, ParseError
from .models import Amenity, Room
from .serializers import AmenitySerializer, RoomListSerializer, RoomDetailSerializer
from categories.models import category


class Amenities(APIView):
    def get(self, request):
        all_amenities = Amenity.objects.all()
        serializer = AmenitySerializer(all_amenities, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AmenitySerializer(data=request.data)
        if serializer.is_valid():
            amenity_obj = serializer.save()
            return Response(
                AmenitySerializer(amenity_obj).data,
            )
        else:
            return Response(serializer.errors)


class AmenityDetail(APIView):
    def get_object(self, pk):
        try:
            return Amenity.objects.get(pk=pk)
        except Amenity.DoesNotExist:
            raise NotFound
        
    def get(self, request, pk):
        amenity = self.get_object(pk)
        serializer = AmenitySerializer(amenity)
        return Response(serializer.data)

    def put(self, request, pk):
        amenity = self.get_object(pk)
        serializer = AmenitySerializer(
            amenity,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            updated_amenity = serializer.save()
            return Response(
                AmenitySerializer(updated_amenity).data,
            )
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        amenity = self.get_object(pk)
        amenity.delete()
        return Response(status=HTTP_204_NO_CONTENT)
    

class RoomListView(APIView):
    def get(self, request):
        all_rooms = Room.objects.all()
        serializer = RoomListSerializer(all_rooms, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        if request.user.is_authenticated:
            serializer = RoomDetailSerializer(data=request.data) # RoomDetailSerializer instead of RoomListSerializer to check validations
            if serializer.is_valid():
                category_pk = request.data.get("category")
                if not category_pk:
                    raise ParseError("Category is required.")
                try:
                    category_obj = category.objects.get(pk=category_pk)
                    if category_obj.kind == category.CategoryKindChoices.EXPERIENCES:
                        raise ParseError("The category kind should be 'rooms'")
                except category.DoesNotExist:
                    raise ParseError("Category not found")
                room_obj = serializer.save(
                    owner=request.user, # when call create() function with validatedata it replaces owner
                    category=category_obj,
                )
                amenities = request.data.get("amenities")
                for amenity_pk in amenities:
                    try:
                        amenity_obj = Amenity.objects.get(pk=amenity_pk)
                        room_obj.amenities.add(amenity_obj) # many to many field
                    except Amenity.DoesNotExist:
                        print(f"Amenity with id {amenity_pk} not found")
                        pass
                return Response(
                    RoomListSerializer(room_obj).data,
                )
            else:
                return Response(serializer.errors)
        else:
            raise NotAuthenticated
      

class RoomDetailView(APIView):
    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound
        
    def get(self, request, pk):
        room_obj = self.get_object(pk)
        serializer = RoomDetailSerializer(room_obj)
        return Response(serializer.data)
    
