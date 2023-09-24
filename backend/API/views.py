from datetime import datetime, time

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from base.models import Question, Answer, User
from API.serializers import QuestionSerializer, AnswerSerializer


@api_view(["GET"])
def get_random_question(request):
    # Get the user_id from the query params
    user_id = request.query_params.get("user_id", None)
    if user_id:
        try:
            # Get the user
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )

        # Get the user answers that were created today
        answers = Answer.objects.filter(
            user=user, created_at__date=datetime.now().date()
        )
        # Get the questions that the user has answered today
        answered_questions = [answer.question.id for answer in answers]

    if user_id:
        # Get the questions that the user has not answered today
        questions = Question.objects.exclude(id__in=answered_questions)
    else:
        # Get all the questions
        questions = Question.objects.all()

    # Get a random question from the questions queryset
    question = questions.order_by("?").first()
    # Serialize the question
    serializer = QuestionSerializer(question)
    # Return the serialized question
    return Response(serializer.data)


@api_view(["POST"])
def post_answer(request):
    # Get the question_id and user_id from the request data
    question_id = request.data.get("question_id")
    user_id = request.data.get("user_id")
    try:
        # Get the question and user
        question = Question.objects.get(id=question_id)
        user = User.objects.get(id=user_id)
    except (Question.DoesNotExist, User.DoesNotExist):
        return Response(
            {"error": "Question or User not found"}, status=status.HTTP_404_NOT_FOUND
        )
    # Get the answer from the request data
    answer = request.data.get("answer")
    # Create the answer
    answer = Answer.objects.create(question=question, user=user, answer=answer)

    # Update the user's money if the user has answered 10 questions today
    answers = Answer.objects.filter(user=user, created_at__date=datetime.now().date())
    if len(answers) == 10:
        # Get the total amount of money from the correct_answers
        money = sum(
            [
                answer.question.money_value
                for answer in answers
                if answer.answer == answer.question.answer
            ]
        )
        # Update the user's money
        user.money += money
        user.save()

    # Delete the user's answers that were created before today (at 00:00)
    answers = Answer.objects.filter(
        user=user, created_at__lt=datetime.combine(datetime.now().date(), time.min)
    )
    answers.delete()

    # Serialize the answer
    serializer = AnswerSerializer(answer)
    # Return the serialized answer
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
