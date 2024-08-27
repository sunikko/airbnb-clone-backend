from rest_framework.views import APIView
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.response import Response
from rest_framework.exceptions import (
    NotFound,
    NotAuthenticated,
    ParseError,
    PermissionDenied,
)
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.db import transaction
from django.conf import settings
from django.utils import timezone
from django.shortcuts import get_object_or_404
from .models import Amenity, Room
from .serializers import AmenitySerializer, RoomListSerializer, RoomDetailSerializer
from categories.models import category
from reviews.serializers import ReviewSerializer
from medias.serializers import PhotoSerializer
from bookings.models import Booking
from bookings.serializers import PublicBookingSerializer, CreateRoomBookingSerializer


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
    
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        all_rooms = Room.objects.all()
        serializer = RoomListSerializer(
            all_rooms, 
            many=True,
            context={"request": request},
        )
        return Response(serializer.data)
    
    def post(self, request):
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
            try:
                with transaction.atomic(): # one transaction - doesn't really save a room on DB
                    room_obj = serializer.save(
                        owner=request.user, # when call create() function with validatedata it replaces owner
                        category=category_obj,
                    )
                    amenities = request.data.get("amenities")
                    for amenity_pk in amenities:
                        # remove try: ecept Amenity.DoesNotExist: room.delete() to make it error for transaction
                        amenity_obj = Amenity.objects.get(pk=amenity_pk)
                        room_obj.amenities.add(amenity_obj) # many to many field
            except Exception:
                    raise ParseError("Amenity not found")
            return Response(
                RoomListSerializer(room_obj).data,
            )
        else:
            return Response(serializer.errors)
        

class RoomDetailView(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound
        
    def get(self, request, pk):
        room_obj = self.get_object(pk)
        serializer = RoomDetailSerializer(
            room_obj,
            context={"request": request},
        )
        return Response(serializer.data)
    
    def delete(self, request, pk):
        room_obj = self.get_object(pk)
        if room_obj.owner != request.user:
            raise PermissionDenied
        room_obj.delete()
        return Response(status=HTTP_204_NO_CONTENT)

    def put(self, request, pk):
        room_obj = self.get_object(pk)
        if room_obj.owner != request.user:
            raise PermissionDenied
        serializer = RoomDetailSerializer(
            room_obj,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            category_obj=room_obj.category
            category_pk = request.data.get("category")
            if category_pk:
                try:
                    category_obj = category.objects.get(pk=category_pk)
                    if category_obj.kind == category.CategoryKindChoices.EXPERIENCES:
                        raise ParseError("The category kind should be 'rooms'")
                except category.DoesNotExist:
                    raise ParseError("category does not exist")
            amenities_list = list(room_obj.amenities.all())
            amenities = request.data.get("amenities")
            if amenities:
                amenities_list = []
                for amenity_pk in amenities:
                    try:
                        amenity_obj = Amenity.objects.get(pk=amenity_pk)
                        amenities_list.append(amenity_obj)
                    except Exception as e:
                        raise ParseError(f"Amenity not found {e}")
            updated_room_obj = serializer.save(category=category_obj)
            updated_room_obj.amenities.set(amenities_list)
            return Response(RoomDetailSerializer(updated_room_obj).data)
        else:
            return Response(serializer.errors)


class RoomReviews(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        return get_object_or_404(Room, pk=pk)
        
    def get(self, request, pk):
        try:
            page = request.query_params.get("page", 1)
            page = int(page)
        except ValueError:
            page = 1
        page_size = settings.PAGE_SIZE
        start = (page-1) * page_size
        end = start + page_size
        room_obj = self.get_object(pk)
        serializer = ReviewSerializer(
            room_obj.reviews.all()[start:end], # django sql query LIMIT: page_size & OFFSET:start
            many=True,
        )
        return Response(serializer.data)
    
    def post(self, request, pk):
        room_obj = self.get_object(pk)
        if request.user != room_obj.owner:
            raise PermissionDenied("You do not have permission to review your own room.")

        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            review_obj = serializer.save(
                user=request.user,
                room=room_obj,
            )
            review_serializer = ReviewSerializer(review_obj)
            return Response(review_serializer.data, status=201)
        return Response(serializer.errors, status=400)

class RoomPhotos(APIView):
    
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            return NotFound
        
    def post(self, request, pk):
        room = self.get_object(pk)
        if request.user != room.owner:
            raise PermissionDenied
        serializer = PhotoSerializer(data=request.data)
        if serializer.is_valid():
            photo = serializer.save(room=room)
            serializer = PhotoSerializer(photo)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        


class RoomBookings(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except:
            raise NotFound
        
    def get(self, requset, pk):
        room = self.get_object(pk)
        now = timezone.localtime(timezone.now()).date()
        bookings = Booking.objects.filter(
            room=room,
            kind=Booking.BookingKindChoices.ROOM,
            check_in__gt=now
        )
        serializer = PublicBookingSerializer(bookings, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        room = self.get_object(pk)
        serializer = CreateRoomBookingSerializer(data=request.data)
        if serializer.is_valid():
            return Response({"ok": True})
        else:
            return Response(serializer.errors)