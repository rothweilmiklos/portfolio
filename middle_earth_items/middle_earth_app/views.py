from .models import Equipments
from .serializer import ItemsSerializer
from rest_framework import generics


# Create your views here.


class EquipmentsView(generics.ListAPIView):
    serializer_class = ItemsSerializer

    def get_queryset(self):
        wielder_caste = self.kwargs['wielder_caste']
        return Equipments.objects.filter(wielder_caste=wielder_caste)


class PurchasedEquipmentView(generics.RetrieveAPIView):
    serializer_class = ItemsSerializer
    queryset = Equipments.objects.all()
    lookup_field = "id"
    lookup_url_kwarg = "id"


class AddEquipment(generics.CreateAPIView):
    serializer_class = ItemsSerializer
    queryset = Equipments.objects.all()


