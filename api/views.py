from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Movie, Rating
from .serializers import MSerializer, RSerializer, USerializer
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class UViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = USerializer



class MViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @action(detail=True, methods=['POST'])
    def rate_movie(self, request, pk=None):
        if 'stars' in request.data:
            movie = Movie.objects.get(id=pk)
            stars = request.data['stars']
            user = request.user
            print(user)
            try:
                rating = Rating.objects.get(user=user.id, movie=movie.id)
                rating.stars = stars
                rating.save()
                serializer = RSerializer(rating, many=False)
                response = {'message': 'Rating update', 'result': serializer.data}

                return Response(response, status=status.HTTP_200_OK)
            except:
                rating = Rating.objects.create(user=user, movie=movie, stars=stars)
                serializer = RSerializer(rating, many=False)
                response = {'message': 'Rating Created ', 'result': serializer.data}
                return Response(response, status=status.HTTP_200_OK)

        else:
            response = {'message': 'its not working'}
            return Response(response, status=status.HTTP_200_OK)


class RViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
