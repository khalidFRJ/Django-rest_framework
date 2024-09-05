from django.shortcuts import render
from django.http.response import JsonResponse
from .models import Guest, Movie, Reservation , Post
from rest_framework.decorators import api_view
from .serializers import GuestSerializer , MovieSerialiser , ReservationSerialiser , PostSerialiser
from rest_framework import status, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404
from rest_framework import mixins, generics , viewsets

from rest_framework.authentication import BasicAuthentication , TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAuthor0rRead0nly






# ====> 1 no REST_framwork and no model query FBV

def no_rest_no_model(request):
    guests = [
        {
            'id' : 1,
            'name' : 'khalid',
            'mobile' : +212654372937,
        },

        {
            'id': 2,
            'name': 'ahmed',
            'mobile' : +212456575654,
        }
    ]
    return JsonResponse (guests , safe=False)

# ====> 2 no rest_framwork and from model

def no_rest_with_model(request):
    data = Guest.objects.all()
    response = {
        'guests' : list(data.values('name', 'mobile'))
    }
    return JsonResponse(response)

# List == GET
# Create == POST
# pk query == GET
# update == PUT
# Delete destroy == DELETE

# ====> 3 Function based views
# - 3.1 GET and POST

@api_view(['GET', 'POST'])
def FBV_list(request):
    # GET
    if request.method == 'GET':
        guests = Guest.objects.all()
        serialiser =GuestSerializer(guests, many=True)
        return Response(serialiser.data)

    # POST
    elif request.method == 'POST':
        serialiser = GuestSerializer(data=request.data)
        if serialiser.is_valid():  # Corrected the typo here
            serialiser.save()
            return Response(serialiser.data, status=status.HTTP_201_CREATED)
        return Response(serialiser.errors, status=status.HTTP_400_BAD_REQUEST)
   
# - 3.2 GET and PUT and DELETE

@api_view(['GET', 'PUT', 'DELETE'])
def FBV_pk(request, pk):
    try:
        guest = Guest.objects.get(pk=pk)
    except Guest.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # GET
    if request.method == 'GET':
        serialiser = GuestSerializer(guest)
        return Response(serialiser.data)

    # PUT
    elif request.method == 'PUT':
        serialiser = GuestSerializer(guest, data=request.data)
        if serialiser.is_valid():  # Corrected the typo here
            serialiser.save()
            return Response(serialiser.data)
        return Response(serialiser.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE
    elif request.method == 'DELETE':
        guest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

# ====> 4 CBV Class based views
#4.1 List and Create == GET and POST

class CBV_List(APIView):

    def get(self, request):
        guests = Guest.objects.all()
        serializer = GuestSerializer(guests, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = GuestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

#4.2 GET PUT DELETE
class CBV_pk(APIView):
    def get_object(self, pk):
        try:
            return Guest.objects.get(pk=pk)
        except Guest.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        guest = self.get_object(pk)
        serializer = GuestSerializer(guest)
        return Response(serializer.data)

    def put(self, request, pk):
        guest = self.get_object(pk)
        serializer = GuestSerializer(guest, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        guest = self.get_object(pk)
        guest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# ====> 5 mixins  
# 5.1 mixins list
class mixins_list(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer

    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)


# 5.2 mixins get put delete
class mixins_pk(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer

    def get(self, request, pk):
        return self.retrieve(request, pk=pk)

    def put(self, request, pk):
        return self.update(request, pk=pk)

    def delete(self, request, pk):
        return self.destroy(request, pk=pk)

# ====> 6 generics
# 6.1 generics list
class generics_list(generics.ListCreateAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    authentication_classes = [TokenAuthentication]
    #permission_classes = [IsAuthenticated]

# 6.2 generics get put delete 
class generics_pk(generics.RetrieveUpdateDestroyAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    authentication_classes = [TokenAuthentication]
    #permission_classes = [IsAuthenticated]

# 7 ViewSets

class viewsets_guest(viewsets.ModelViewSet):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer

class Viewsets_Movie(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerialiser
    filter_backends = [filters.SearchFilter]        =======> filtring and searching 
    search_fields = ['movie']

class Viewsets_Reservation(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerialiser

# 8 find movie

@api_view(['GET'])
def find_movie(request):
    Movies = Movie.objects.filter(
        hall = request.data ['hall'],
        Movie = request.data ['Movie'],
    )
    serializer = MovieSerialiser(Movies,many=True)
    return Response(serializer.data)

# 9 creat new reservation
 
@api_view(['POST'])
def new_reservation(request):
    movie = Movie.objects.get(
        hall=request.data['hall'],
        movie=request.data['movie']
    )

    guest = Guest()
    guest.name = request.data['name']
    guest.mobile = request.data['mobile']
    guest.save()

    reservation = Reservation()
    reservation.guest = guest
    reservation.movie = movie
    reservation.save()

    return Response(status=status.HTTP_201_CREATED)

class Post_pk(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthor0rRead0nly]
    queryset = Post.objects.all()
    serializer_class = PostSerialiser
