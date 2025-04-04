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

def test_add_choice_to_question():
    question = Question(title='q1')
    choice = question.add_choice('Choice 1', True)
    assert len(question.choices) == 1
    assert choice.text == 'Choice 1'
    assert choice.is_correct is True

def test_remove_choice_by_id():
    question = Question(title='q1')
    choice1 = question.add_choice('Choice 1', True)
    choice2 = question.add_choice('Choice 2', False)
    question.remove_choice_by_id(choice1.id)
    assert len(question.choices) == 1
    assert question.choices[0].id == choice2.id

def test_remove_all_choices():
    question = Question(title='q1')
    question.add_choice('Choice 1', True)
    question.add_choice('Choice 2', False)
    question.remove_all_choices()
    assert len(question.choices) == 0

def test_select_choices_within_limit():
    question = Question(title='q1', max_selections=2)
    choice1 = question.add_choice('Choice 1', True)
    choice2 = question.add_choice('Choice 2', False)
    selected = question.select_choices([choice1.id, choice2.id])
    assert selected == [choice1.id]

def test_select_choices_exceeding_limit():
    question = Question(title='q1', max_selections=1)
    choice1 = question.add_choice('Choice 1', True)
    choice2 = question.add_choice('Choice 2', False)
    with pytest.raises(Exception):
        question.select_choices([choice1.id, choice2.id])

def test_set_correct_choices():
    question = Question(title='q1')
    choice1 = question.add_choice('Choice 1', False)
    choice2 = question.add_choice('Choice 2', False)
    question.set_correct_choices([choice1.id])
    assert choice1.is_correct is True
    assert choice2.is_correct is False

def test_create_choice_with_invalid_text():
    question = Question(title='q1')
    with pytest.raises(Exception):
        question.add_choice('', False)
    with pytest.raises(Exception):
        question.add_choice('a' * 101, False)

def test_create_question_with_invalid_points():
    with pytest.raises(Exception):
        Question(title='q1', points=0)
    with pytest.raises(Exception):
        Question(title='q1', points=101)

def test_select_correct_choices_only():
    q = Question("q", max_selections=2)
    c1 = q.add_choice("Correct", is_correct=True)
    c2 = q.add_choice("Incorrect", is_correct=False)
    selected = q.select_choices([c1.id, c2.id])
    assert selected == [c1.id]

def test_generate_choice_id_increments():
    q = Question("q")
    c1 = q.add_choice("A")
    c2 = q.add_choice("B")
    assert c2.id == c1.id + 1

@pytest.fixture
def question_with_choices():
    question = Question(title="Sample Question", max_selections=2)
    question.add_choice("Choice 1", True)
    question.add_choice("Choice 2", False)
    question.add_choice("Choice 3", True)
    return question

def test_create_choice_with_empty_text():
    question = Question(title="Sample Question", max_selections=2)
    with pytest.raises(Exception):
        question.add_choice("", False)

def test_set_correct_choices_updates_is_correct(question_with_choices):
    question_with_choices.set_correct_choices([question_with_choices.choices[0].id, question_with_choices.choices[2].id])
    assert question_with_choices.choices[0].is_correct is True
    assert question_with_choices.choices[1].is_correct is False
    assert question_with_choices.choices[2].is_correct is True
