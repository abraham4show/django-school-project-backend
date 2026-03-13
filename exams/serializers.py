from rest_framework import serializers
from .models import Exam, Question
from rest_framework import serializers
from .models import ExamAttempt, Answer

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'question', 'answer_text', 'selected_option']

class ExamAttemptSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)
    exam_title = serializers.CharField(source='exam.title', read_only=True)
    total_marks = serializers.IntegerField(source='exam.total_marks', read_only=True)

    class Meta:
        model = ExamAttempt
        fields = ['id', 'student', 'exam', 'exam_title', 'total_marks', 'started_at', 'submitted_at', 'score', 'passed', 'answers']

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'text', 'type', 'points', 'order', 'options', 'correct_answer']

class ExamSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, required=False)
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    class_name = serializers.CharField(source='class_group.name', read_only=True)

    class Meta:
        model = Exam
        fields = [
            'id', 'title', 'subject', 'subject_name',
            'class_group', 'class_name', 'date', 'duration',
            'total_marks', 'status', 'created_at', 'updated_at',
            'questions'
        ]
        read_only_fields = ['total_marks', 'created_at', 'updated_at']

    def create(self, validated_data):
        questions_data = validated_data.pop('questions', [])
        exam = Exam.objects.create(**validated_data)
        total_marks = 0
        for idx, q_data in enumerate(questions_data):
            q_data['order'] = idx
            Question.objects.create(exam=exam, **q_data)
            total_marks += q_data.get('points', 0)
        exam.total_marks = total_marks
        exam.save(update_fields=['total_marks'])
        return exam

    def update(self, instance, validated_data):
        questions_data = validated_data.pop('questions', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if questions_data is not None:
            existing_ids = [q['id'] for q in questions_data if 'id' in q]
            instance.questions.exclude(id__in=existing_ids).delete()

            total_marks = 0
            for idx, q_data in enumerate(questions_data):
                q_data['order'] = idx
                q_id = q_data.get('id')
                if q_id:
                    question = Question.objects.get(id=q_id, exam=instance)
                    for attr, val in q_data.items():
                        setattr(question, attr, val)
                    question.save()
                else:
                    Question.objects.create(exam=instance, **q_data)
                total_marks += q_data.get('points', 0)
            instance.total_marks = total_marks
            instance.save(update_fields=['total_marks'])
        return instance

        