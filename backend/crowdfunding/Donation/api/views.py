'DRF (Django REST Framework) views for Crowdfunding.)'
# ACTION (CUSTOM)
from rest_framework.decorators import action
# VIEWSETS
from rest_framework.viewsets import ModelViewSet
# PERMISSIONS
from rest_framework.permissions import AllowAny

'from Project'
# MODEL
from Donation.models import Donation
# SERIALIZER
from Donation.api.serializer import DonationSerializer

class DonationViewSet(ModelViewSet):

    queryset = Donation.objects.all()
    serializer_class = DonationSerializer

    permission_classes = [AllowAny]
    # Top Five Donations (Custom Action)
    @action(detail=False, methods=['get'])
    def top_five_donations(self, request):
        top_five = Donation.objects.order_by('-amount')[:5]
        serializer = self.get_serializer(top_five, many=True)
        return Response(serializer.data)
