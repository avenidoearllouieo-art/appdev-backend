from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Locker
from .serializers import LockerSerializer

# GET all lockers
@api_view(['GET'])
def get_lockers(request):
    lockers = Locker.objects.all()
    serializer = LockerSerializer(lockers, many=True)
    return Response(serializer.data)

# POST open locker
@api_view(['POST'])
def open_locker(request, id):
    locker = Locker.objects.get(id=id)
    locker.status = "In Use"
    locker.time_left = 60
    locker.save()
    return Response({"message": "Locker opened"})