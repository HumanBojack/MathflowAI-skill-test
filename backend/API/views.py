from rest_framework.response import Response
from rest_framework.decorators import api_view
from base.models import Question, Answer, User
from API.serializers import QuestionSerializer


@api_view(["GET"])
def get_random_question(request):
    # Get a random question
    question = Question.objects.order_by("?").first()
    # Serialize the question
    serializer = QuestionSerializer(question)
    # Return the serialized question
    return Response(serializer.data)


@api_view(["GET"])
def hello_world(request):
    return Response({"message": "Hello, world!"})
