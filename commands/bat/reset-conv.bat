cd .. cd ..

python manage.py shell
from response.models import Conversation
Conversation.objects.all().delete()