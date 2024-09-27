from rest_framework import generics, permissions, throttling
from rest_framework.exceptions import PermissionDenied
from rest_framework.throttling import ScopedRateThrottle
from .models import Estimate
from .serializers import EstimateSerializer


class EstimateCreateView(generics.CreateAPIView):
    queryset = Estimate.objects.all()
    serializer_class = EstimateSerializer
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [throttling.UserRateThrottle, ScopedRateThrottle]
    throttle_scope = 'user_minute'

    def perform_create(self, serializer):
        # Automatically set the 'created_by' field to the current user
        serializer.save(created_by=self.request.user)


class EstimateDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Estimate.objects.all()
    serializer_class = EstimateSerializer