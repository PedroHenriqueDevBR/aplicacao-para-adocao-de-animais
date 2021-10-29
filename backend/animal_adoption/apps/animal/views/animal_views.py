from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from apps.animal.validators.animal_validator import animal_is_valid_or_errors
from apps.core.models import Animal
from rest_framework.permissions import IsAuthenticated
from apps.animal.serializers.animal_serializers import (
    AnimalSerializer,
    CreateAnimalSerializer,
)


class AnimalListForAdoption(APIView):
    name = "animal_list_for_adoption"

    # List all animals with adoption enable in logget person region
    def get(self, request):
        animals = Animal.objects.filter(blocked=False, adopted=False)
        serializer = AnimalSerializer(animals, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AnimalLocationList(APIView):
    name = "animal_location_list"
    permission_classes = [IsAuthenticated]

    # List all animals with adoption enable in logget person region
    def get(self, request):
        logged_person = request.user.person
        animals = Animal.objects.filter(
            blocked=False, 
            owner__city=logged_person.city
        ).exclude(
            owner__latitude='', 
            owner__longitude='',
        ).exclude(
            owner__latitude='0',
            owner__longitude='0'
        )
        serializer = AnimalSerializer(animals, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AnimalListFilter(APIView):
    name = "animal_list_filter"

    # List all animals with adoption enable in logget person region
    def get(self, request):
        pass


class AnimalListAndCreate(APIView):
    name = "animal_list_and_create"
    permission_classes = [IsAuthenticated]

    # get all animals from logged user
    def get(self, request):
        person = request.user.person
        animals = person.all_animals
        serializer = AnimalSerializer(animals, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Create a new animal from logget person
    def post(self, request):
        data = request.data
        errors = animal_is_valid_or_errors(data)
        if len(errors) > 0:
            return Response({"errors": errors}, status=status.HTTP_406_NOT_ACCEPTABLE)
        data["owner"] = request.user.person.pk
        creator_serializer = CreateAnimalSerializer(data=data)
        if creator_serializer.is_valid():
            creator_serializer.save()
            return Response(creator_serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(
            creator_serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE
        )


class AnimalShow(APIView):
    name = "animal-show"

    # Select data from animal (if logged person is wouner)
    def get(self, request, pk):
        try:
            animal = Animal.objects.get(pk=pk)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = AnimalSerializer(animal, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AnimalEditAndDelete(APIView):
    name = "animal_edit_and_delete"
    permission_classes = [IsAuthenticated]

    # Select data from animal (if logged person is wouner)
    def get(self, request, pk):
        try:
            animal = Animal.objects.get(pk=pk)
            assert animal.owner == request.user.person
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = AnimalSerializer(animal, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Update data from animal (if logged person is wouner)
    def put(self, request, pk):
        try:
            animal = Animal.objects.get(pk=pk)
            assert animal.owner == request.user.person
            data = request.data
            errors = animal_is_valid_or_errors(data)
            if len(errors) > 0:
                return Response(
                    {"errors": errors}, status=status.HTTP_406_NOT_ACCEPTABLE
                )
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        data["owner"] = request.user.person.pk
        serializer = CreateAnimalSerializer(animal, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

    # Delete animal (if logged person is wouner)
    def delete(self, request, pk):
        try:
            animal = Animal.objects.get(pk=pk)
            assert animal.owner == request.user.person
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        animal.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
