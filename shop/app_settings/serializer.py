from rest_framework import serializers

from .models import SiteSettings


class SiteSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteSettings
        fields = ['cost_express', 'edge_for_free_delivery', 'cost_usual_delivery', 'root_category',
                  'category_main_page', 'quantity_popular', 'time_cache_product']
