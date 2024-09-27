from rest_framework import serializers
from .models import Estimate, EstimateEquipment


class EstimateEquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstimateEquipment
        fields = ['id', 'equipment', 'quantity', 'price_override', 'created_at']
        read_only_fields = ['id', 'created_at']


class EstimateSerializer(serializers.ModelSerializer):
    equipments = EstimateEquipmentSerializer(many=True, required=False)
    equipments_list = EstimateEquipmentSerializer(source='equipments', many=True, required=False)

    class Meta:
        model = Estimate
        fields = ['id', 'note', 'created_at', 'created_by', 'is_archived', 'equipments', 'equipments_list']
        read_only_fields = ['id', 'created_at']

    def create(self, validated_data):
        equipments_data = validated_data.pop('equipments', [])
        estimate = Estimate.objects.create(**validated_data)

        self._create_or_update_equipments(estimate, equipments_data)

        return estimate

    def update(self, instance, validated_data):
        equipments_data = validated_data.pop('equipments', [])
        
        # Update the Estimate object
        instance.note = validated_data.get('note', instance.note)
        instance.is_archived = validated_data.get('is_archived', instance.is_archived)
        instance.save()

        instance.equipments.all().delete()
        for equipment_data in equipments_data:
            EstimateEquipment.objects.create(estimate=instance, **equipment_data)

        return instance

    def _create_or_update_equipments(self, estimate, equipments_data):
        """
        Helper method to create or update equipment instances associated with the estimate.
        """
        equipment_instances = [
            EstimateEquipment(estimate=estimate, **equipment_data) for equipment_data in equipments_data
        ]
        EstimateEquipment.objects.bulk_create(equipment_instances)  # Bulk create for efficiency
