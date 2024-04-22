from .models import Product
from channels.db import database_sync_to_async


@database_sync_to_async
def get_products_for_last_parsing():
    last_record = Product.objects.order_by('-id').first()
    if last_record:
        last_recording_time = last_record.recording_time
        return list(Product.objects.filter(recording_time=last_recording_time))
    return []


