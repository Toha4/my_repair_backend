from authentication.utils import get_current_user

SERIALIZER_DATE_PARAMS = dict(format="%d.%m.%Y", input_formats=["%d.%m.%Y", "iso-8601"])


class CurrentUserDefault(object):
    def set_context(self, serializer_field):
        request = serializer_field.context["request"]
        self.user = get_current_user(request)

    def __call__(self):
        return self.user
