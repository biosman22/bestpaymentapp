from django.forms import model_to_dict
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Model

class LazyEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Model):
            return model_to_dict(obj)
        return super().default(obj)