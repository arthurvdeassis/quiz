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


# Fixtures e testes

@pytest.fixture
def question_with_one_correct_answer():
    question = Question(title="Qual a capital do Brasil?", max_selections=1)
    question.add_choice("São Paulo", is_correct=False)
    question.add_choice("Brasília", is_correct=True)
    question.add_choice("Rio de Janeiro", is_correct=False)

    question_fixed = Question(
        title="Qual a capital do Brasil?", max_selections=1)
    c1 = question_fixed.add_choice("São Paulo")
    c2 = question_fixed.add_choice("Brasília")
    c3 = question_fixed.add_choice("Rio de Janeiro")
    question_fixed.set_correct_choices([c2.id])

    return question_fixed


@pytest.fixture
def question_with_multiple_correct_answers():
    question = Question(
        title="Quais destes são planetas do sistema solar?", max_selections=2)
    c1 = question.add_choice("Marte")
    c2 = question.add_choice("Lua")
    c3 = question.add_choice("Júpiter")
    c4 = question.add_choice("Plutão")
    question.set_correct_choices([c1.id, c3.id])

    return question

# Testa se a fixture básica foi criada com o número correto de alternativas.


def test_fixture_setup_correctly(question_with_one_correct_answer):
    assert len(question_with_one_correct_answer.choices) == 3

# Testa a seleção da única resposta correta.


def test_selection_of_single_correct_answer(question_with_one_correct_answer):
    correct_choice_id = 2

    result = question_with_one_correct_answer.correct_selected_choices([
                                                                       correct_choice_id])

    assert result == [correct_choice_id]

# Testa a remoção de uma alternativa.


def test_remove_choice_from_fixture(question_with_one_correct_answer):
    choice_id_to_remove = 1

    question_with_one_correct_answer.remove_choice_by_id(choice_id_to_remove)

    assert len(question_with_one_correct_answer.choices) == 2
    remaining_ids = [
        choice.id for choice in question_with_one_correct_answer.choices]
    assert choice_id_to_remove not in remaining_ids

# Testa a seleção parcialmente correta de múltiplas respostas


def test_partial_correct_selection_in_multi_choice(question_with_multiple_correct_answers):
    result = question_with_multiple_correct_answers.correct_selected_choices([
                                                                             1, 2])
    assert result == [1]

# Testa a seleção correta de múltiplas respostas


def test_all_correct_selections_in_multi_choice(question_with_multiple_correct_answers):
    result = question_with_multiple_correct_answers.correct_selected_choices([
                                                                             1, 3])
    assert set(result) == {1, 3}
