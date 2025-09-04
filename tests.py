import pytest
from model import Question


def test_create_question():
    question = Question(title='q1')
    assert question.id != None


def test_create_multiple_questions():
    question1 = Question(title='q1')
    question2 = Question(title='q2')
    assert question1.id != question2.id


def test_create_question_with_invalid_title():
    with pytest.raises(Exception):
        Question(title='')
    with pytest.raises(Exception):
        Question(title='a'*201)
    with pytest.raises(Exception):
        Question(title='a'*500)


def test_create_question_with_valid_points():
    question = Question(title='q1', points=1)
    assert question.points == 1
    question = Question(title='q1', points=100)
    assert question.points == 100


def test_create_choice():
    question = Question(title='q1')

    question.add_choice('a', False)

    choice = question.choices[0]
    assert len(question.choices) == 1
    assert choice.text == 'a'
    assert not choice.is_correct

# Testa se criar uma questão com pontos inválidos levanta uma exceção.


def test_create_question_with_invalid_points():
    with pytest.raises(Exception, match='Points must be between 1 and 100'):
        Question(title='q1', points=0)
    with pytest.raises(Exception, match='Points must be between 1 and 100'):
        Question(title='q1', points=101)

# Testa o comportamento de adicionar várias alternativas a uma questão.


def test_add_multiple_choices():
    question = Question(title='q1')
    question.add_choice('a')
    question.add_choice('b')
    assert len(question.choices) == 2

# Testa se adicionar uma alternativa com texto inválido levanta uma exceção.


def test_add_choice_with_invalid_text():
    question = Question(title='q1')
    with pytest.raises(Exception, match='Text cannot be empty'):
        question.add_choice('')
    with pytest.raises(Exception, match='Text cannot be longer than 100 characters'):
        question.add_choice('a' * 101)

# Testa o comportamento de remover uma alternativa de uma questão.


def test_remove_choice():
    question = Question(title='q1')
    choice_to_keep = question.add_choice('a')
    choice_to_remove = question.add_choice('b')

    question.remove_choice_by_id(choice_to_remove.id)

    assert len(question.choices) == 1
    assert question.choices[0].id == choice_to_keep.id

# Testa se tentar remover uma alternativa que não existe levanta uma exceção.


def test_remove_non_existent_choice_raises_exception():
    question = Question(title='q1')
    question.add_choice('a')

    with pytest.raises(Exception, match='Invalid choice id'):
        question.remove_choice_by_id(999)

# Testa o comportamento de marcar uma alternativa como correta.


def test_set_correct_choice():
    question = Question(title='q1')
    choice1 = question.add_choice('a')

    question.set_correct_choices([choice1.id])

    assert choice1.is_correct is True

# Testa se o sistema identifica corretamente uma resposta certa.


def test_correct_selected_choices_with_correct_answer():
    question = Question(title='q1')
    choice1 = question.add_choice('a')
    question.set_correct_choices([choice1.id])

    result = question.correct_selected_choices([choice1.id])

    assert result == [choice1.id]

# Testa se o sistema identifica corretamente uma resposta errada.


def test_correct_selected_choices_with_incorrect_answer():
    question = Question(title='q1')
    choice1 = question.add_choice('a')
    choice2 = question.add_choice('b')
    question.set_correct_choices([choice1.id])

    result = question.correct_selected_choices([choice2.id])

    assert result == []

# Testa a correção para uma questão de múltipla escolha com mais de uma resposta certa.


def test_correct_selected_choices_with_multiple_correct_answers():
    question = Question(title='q1', max_selections=2)
    choice1 = question.add_choice('a')
    choice2 = question.add_choice('b')
    choice3 = question.add_choice('c')
    question.set_correct_choices([choice1.id, choice3.id])

    result = question.correct_selected_choices([choice1.id, choice2.id])

    assert result == [choice1.id]

# Testa se selecionar mais alternativas que o permitido levanta uma exceção.


def test_correct_selected_choices_exceeding_max_selections_raises_exception():
    question = Question(title='q1', max_selections=1)
    choice1 = question.add_choice('a')
    choice2 = question.add_choice('b')

    with pytest.raises(Exception, match='Cannot select more than 1 choice'):
        question.correct_selected_choices([choice1.id, choice2.id])
