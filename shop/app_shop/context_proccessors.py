from .models import Category
from app_settings.models import SiteSettings


def load_menu(request):
    try:
        settings = SiteSettings.load()
        sub_categories = settings.root_category.get_descendants(include_self=False)
    except AttributeError as exc:
        sub_categories = {}
    return {'main_menu': sub_categories}
