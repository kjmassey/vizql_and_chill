from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from tableau.models import TestModel, RatingsModel, ContentMetaDataModel
from tableau.serializers import (
    TestModelSerializer,
    RatingsSerializer,
    ContentMetaDataSerializer,
)
from rest_framework.decorators import action
from tableau.helpers.jwt import generate_login_jwt
from tableau.helpers.rest_api.funcs import (
    do_site_content_query,
    perform_content_search,
    get_item_tags,
    get_user_recommendations,
    get_user_favorites,
    add_item_to_favorites,
    remove_item_from_favorites,
    get_workbook_preview_image,
    get_url_to_item,
    do_single_item_query,
)
import traceback


# Create your views here.
class APITest(ModelViewSet):

    queryset = TestModel.objects.all()
    serializer_class = TestModelSerializer


class TableauViewsSet(ModelViewSet):

    queryset = TestModel.objects.all()
    serializer_class = TestModelSerializer

    @action(detail=False, methods=["get"])
    def getUserJwt(self, request, *args, **kwargs):

        try:
            return Response({"token": generate_login_jwt(), "error": None})

        except Exception as e:
            print("+++++++ EXCEPTION +++++++")
            print(e)

            ...

    @action(detail=False, methods=["post"])
    def getSiteContent(self, request, *args, **kwargs):
        print("+++++ VDS ENDPOINT LOAD, INITIAL: ", request.data)

        try:
            return Response(do_site_content_query(request.data))

        except Exception as e:
            print("+++++++ EXCEPTION +++++++")
            print(e)
            print(traceback.format_exc())
            return Response(str(e))

    @action(detail=False, methods=["post"])
    def vdsQuerySingleItem(self, request):
        """
        Query the Site Content datasource for a single item. Return luid, name, type and url
        """

        try:
            return Response(do_single_item_query(request.data))

        except Exception as e:
            print("+++++++ EXCEPTION +++++++")
            print(e)
            print(traceback.format_exc())
            return Response(str(e))

    @action(detail=False, methods=["post"])
    def contentSearch(self, request, *args, **kwargs):

        try:
            return Response(perform_content_search(request.data))

        except Exception as e:
            ...

    @action(detail=False, methods=["post"])
    def getRatingsForUser(self, request):

        try:
            qry = RatingsModel.objects.filter(user=request.data["user"], is_active=True)
            ser = RatingsSerializer(qry, many=True)

            return Response(ser.data)

        except Exception as e:
            ...

    @action(detail=False, methods=["post"])
    def addUserRating(self, request):

        try:
            ser = RatingsSerializer(data=request.data)

            if ser.is_valid():
                ser.save()
                return Response(ser.data)

            return Response(ser.errors)

        except Exception as e:
            ...

    @action(detail=False, methods=["post"])
    def getItemTags(self, request):

        try:
            return Response(get_item_tags(request.data))

        except Exception as e:
            ...

    @action(detail=False, methods=["post"])
    def getRecommendationsForUser(self, request):
        """
        Get recommendations for a user
        """

        try:
            return Response(get_user_recommendations(request.data))

        except Exception as e:
            ...

    @action(detail=False, methods=["post"])
    def getUserFavorites(self, request):
        """
        Get user favorites
        """

        try:
            return Response(get_user_favorites(request.data))

        except Exception as e:
            ...

    @action(detail=False, methods=["post"])
    def addToUserFavorites(self, request):
        """
        Get user favorites
        """

        try:
            print("++++ REQUEST")
            print(request.data)
            return Response(add_item_to_favorites(request.data))

        except Exception as e:
            ...

    @action(detail=False, methods=["post"])
    def removeFromUserFavorites(self, request):
        """
        Get user favorites
        """

        try:
            return Response(remove_item_from_favorites(request.data))

        except Exception as e:
            print("+++++ EXC")
            print(traceback.format_exc())
            ...

    @action(detail=False, methods=["get"])
    def getMockedContent(self, request):
        """
        Get mocked content
        """

        try:
            qry = ContentMetaDataModel.objects.all()
            ser = ContentMetaDataSerializer(qry, many=True)

            return Response(ser.data)

        except Exception as e:
            print("+++++ EXC")
            print(traceback.format_exc())
            ...

    @action(detail=False, methods=["post"])
    def retrieveContentDetails(self, request):
        """
        Get content details
        """

        try:
            qry = ContentMetaDataModel.objects.get(luid=request.data["luid"])
            return Response(ContentMetaDataSerializer(qry, many=False).data)

        except ContentMetaDataModel.DoesNotExist:
            return Response({})

        except Exception as e:
            print("+++++ EXC")
            print(traceback.format_exc())
            ...

    @action(detail=False, methods=["post"])
    def getWorkbookPreviewImage(self, request):
        """
        Get workbook preview image
        """

        try:
            print("+++++ REQUEST: ", request.data)
            return Response(get_workbook_preview_image(request.data))

        except Exception as e:
            print("+++++ EXC")
            print(traceback.format_exc())
            return Response({"error": str(e)})

    @action(detail=False, methods=["post"])
    def getItemsByTag(self, request):
        """
        Get items by tag
        """

        try:
            results = []

            qry = ContentMetaDataModel.objects.filter(
                tags__icontains=request.data["tag"]
            )[:25]
            ser = ContentMetaDataSerializer(qry, many=True)

            for item in ser.data:
                item_type = item["type"]

                item_dict = {}

                item_dict["addedAt"] = None
                item_dict["label"] = None
                item_dict["position"] = None
                item_dict[item_type] = {
                    "id": item["luid"],
                    "description": item["description"],
                    "name": item["name"],
                }
                item_dict["type"] = item_type

                results.append(item_dict)

            return Response(results)

        except Exception as e:
            print("+++++ EXC")
            print(traceback.format_exc())
            ...

    @action(detail=False, methods=["post"])
    def getItemUrl(self, request):
        """
        Get item url
        """

        try:
            return Response(get_url_to_item(request.data))

        except Exception as e:
            print("+++++ EXC")
            print(traceback.format_exc())
            ...

            return Response(e)

    @action(detail=False, methods=["get"])
    def getAgedContent(self, request):
        """
        Get aged content
        """

        results = []

        try:
            qry = ContentMetaDataModel.objects.filter(
                modified_date__lt="2024-10-01 00:00:00", owner_name__isnull=False
            )[:25]
            ser = ContentMetaDataSerializer(qry, many=True)

            for item in ser.data:
                item_type = item["type"]

                item_dict = {}

                item_dict["addedAt"] = None
                item_dict["label"] = None
                item_dict["position"] = None
                item_dict[item_type] = {
                    "id": item["luid"],
                    "description": item["description"],
                    "name": item["name"],
                    "owner_name": item["owner_name"],
                }
                item_dict["type"] = item_type

                results.append(item_dict)

            return Response(results)

        except Exception as e:
            print("+++++ EXC")
            print(traceback.format_exc())

            return Response(str(e))

    @action(detail=False, methods=["get"])
    def getNewContent(self, request):
        """
        Get aged content
        """

        results = []

        try:
            qry = ContentMetaDataModel.objects.filter(
                modified_date__gt="2024-04-01 00:00:00"
            )[:25]
            ser = ContentMetaDataSerializer(qry, many=True)

            for item in ser.data:
                item_type = item["type"]

                item_dict = {}

                item_dict["addedAt"] = None
                item_dict["label"] = None
                item_dict["position"] = None
                item_dict[item_type] = {
                    "id": item["luid"],
                    "description": item["description"],
                    "name": item["name"],
                    "owner_name": item["owner_name"],
                }
                item_dict["type"] = item_type

                results.append(item_dict)

            return Response(results)

        except Exception as e:
            print("+++++ EXC")
            print(traceback.format_exc())

            return Response(str(e))

    @action(detail=False, methods=["get"])
    def getFeaturedAuthorContent(self, request):
        """
        Get featured author content
        """

        results = []

        try:
            qry = ContentMetaDataModel.objects.filter(
                owner_name="Lindsay Betzendahl", type="workbook"
            )[:25]
            ser = ContentMetaDataSerializer(qry, many=True)

            for item in ser.data:
                item_type = item["type"]

                item_dict = {}

                item_dict["addedAt"] = None
                item_dict["label"] = None
                item_dict["position"] = None
                item_dict[item_type] = {
                    "id": item["luid"],
                    "description": item["description"],
                    "name": item["name"],
                    "owner_name": item["owner_name"],
                }
                item_dict["type"] = item_type

                results.append(item_dict)

            return Response(results)

        except Exception as e:
            print("+++++ EXC")
            print(traceback.format_exc())

            return Response(str(e))
