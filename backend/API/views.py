from datetime import datetime

from rest_framework import status
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
def get_money_buffer(request, user_id: int):
    try:
        # Get the user
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    # Get the money buffer by combining the user answers
    # Get the user answers that were created today
    answers = Answer.objects.filter(user=user, created_at__date=datetime.now().date())
    # Get the total amount of money from the correct_answers
    if len(answers) < 10:
        buffer_money = sum(
            [
                answer.question.money_value
                for answer in answers
                if answer.answer == answer.question.answer
            ]
        )
    else:
        buffer_money = 0

    # Return the money and the buffer
    return Response({"money": user.money, "buffer": buffer_money})
