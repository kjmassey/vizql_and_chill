from rest_framework.serializers import ModelSerializer
from tableau.models import TestModel, RatingsModel, ContentMetaDataModel


class TestModelSerializer(ModelSerializer):

    class Meta:
        model = TestModel
        fields = "__all__"


class RatingsSerializer(ModelSerializer):

    class Meta:
        model = RatingsModel
        fields = "__all__"


class ContentMetaDataSerializer(ModelSerializer):
    """
    Serializer for the mocked metadata for Tableau items.
    """

    class Meta:
        model = ContentMetaDataModel
        fields = "__all__"
