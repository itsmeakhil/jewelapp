from rest_framework.views import APIView

from agent.models import Area
from agent.serializers import AreaSerializer
from utils import responses as response


class AreaList(APIView):

    def get(self, request):
        try:
            area = Area.objects.get_all_active()
            serializer = AreaSerializer(area, many=True)
            return response.get_success_200('Area list loaded successfully', serializer.data)
        except Exception as e:
            return response.exception_500(e)
