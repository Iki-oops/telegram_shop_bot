from loader import dp
from .private import IsPrivateAdmin
from .photo_url import IsValidUrl


if __name__ == "filters":
    dp.filters_factory.bind(IsPrivateAdmin)
    dp.filters_factory.bind(IsValidUrl)
