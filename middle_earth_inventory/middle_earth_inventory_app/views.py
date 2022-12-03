from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from .models import WhoOwnsWhat
from .serializers import WhoOwnsWhatSerializer


# Create your views here.


class InventoryListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = WhoOwnsWhatSerializer

    def get_queryset(self):
        username = self.kwargs['username']
        return WhoOwnsWhat.objects.filter(owner_username=username)


class InventoryPurchaseView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = WhoOwnsWhatSerializer
    queryset = WhoOwnsWhat.objects.all()


class InventorySellView(generics.RetrieveDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = WhoOwnsWhatSerializer

    def get_queryset(self):
        inventory_id = self.kwargs['pk']
        return WhoOwnsWhat.objects.filter(id=inventory_id)
