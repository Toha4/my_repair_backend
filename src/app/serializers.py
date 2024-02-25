from authentication.utils import get_current_user

SERIALIZER_DATE_PARAMS = dict(format="%d.%m.%Y", input_formats=["%d.%m.%Y", "iso-8601"])
SERIALIZER_DATETIME_PARAMS = dict(format="%d.%m.%Y %H:%M", input_formats=["%d.%m.%Y %H:%M", "iso-8601"])


class CurrentUserDefault(object):
    requires_context = True

    def __call__(self, serializer_instance=None):
        request = serializer_instance.context["request"]
        user = get_current_user(request)
        return user
