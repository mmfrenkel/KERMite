from server.server import app, db                  # this dependency is necessary to prevent a circular import
from server.models.sudoku_puzzle import Puzzle
from server.models.puzzle_pieces import PuzzlePiece
from server.models.puzzle_exception import PuzzleException
from server.config import UnitTestingConfig
from server.tests.unit.mock_session import MockSession
import pytest

app.config.from_object(UnitTestingConfig)


@pytest.fixture(autouse=False)
def incomplete_puzzle():
    """
    Have an incomplete puzzle that can be used for testing
    """
    puzzle = Puzzle(difficulty_level=0.2, size=2)
    puzzle.id = 1
    puzzle.puzzle_pieces = [
        PuzzlePiece(1, 0, 0, value=2, static_piece=True),
        PuzzlePiece(1, 1, 0, value=4, static_piece=True),
        PuzzlePiece(1, 2, 0, value=3, static_piece=True),
        PuzzlePiece(1, 3, 0, value=1, static_piece=True),
        PuzzlePiece(1, 0, 1, value=1, static_piece=True),
        PuzzlePiece(1, 1, 1, value=3, static_piece=False),
        PuzzlePiece(1, 2, 1, value=4, static_piece=True),
        PuzzlePiece(1, 3, 1, value=2, static_piece=True),
        PuzzlePiece(1, 0, 2, value=None, static_piece=False),
        PuzzlePiece(1, 1, 2, value=2, static_piece=True),
        PuzzlePiece(1, 2, 2, value=1, static_piece=True),
        PuzzlePiece(1, 3, 2, value=3, static_piece=True),
        PuzzlePiece(1, 0, 3, value=3, static_piece=True),
        PuzzlePiece(1, 1, 3, value=1, static_piece=True),
        PuzzlePiece(1, 2, 3, value=None, static_piece=False),
        PuzzlePiece(1, 3, 3, value=4, static_piece=True)
    ]
    return puzzle


@pytest.fixture(autouse=False)
def complete_puzzle():
    puzzle = Puzzle(difficulty_level=0.2, size=2)
    puzzle.id = 1
    puzzle.puzzle_pieces = [
        PuzzlePiece(1, 0, 0, value=2, static_piece=True),
        PuzzlePiece(1, 1, 0, value=4, static_piece=True),
        PuzzlePiece(1, 2, 0, value=3, static_piece=True),
        PuzzlePiece(1, 3, 0, value=1, static_piece=True),
        PuzzlePiece(1, 0, 1, value=1, static_piece=True),
        PuzzlePiece(1, 1, 1, value=3, static_piece=False),
        PuzzlePiece(1, 2, 1, value=4, static_piece=True),
        PuzzlePiece(1, 3, 1, value=2, static_piece=True),
        PuzzlePiece(1, 0, 2, value=4, static_piece=False),
        PuzzlePiece(1, 1, 2, value=2, static_piece=True),
        PuzzlePiece(1, 2, 2, value=1, static_piece=True),
        PuzzlePiece(1, 3, 2, value=3, static_piece=True),
        PuzzlePiece(1, 0, 3, value=3, static_piece=True),
        PuzzlePiece(1, 1, 3, value=1, static_piece=True),
        PuzzlePiece(1, 2, 3, value=2, static_piece=False),
        PuzzlePiece(1, 3, 3, value=4, static_piece=True)
    ]
    puzzle.completed = True
    return puzzle


@pytest.fixture(autouse=False)
def incorrect_puzzle():
    puzzle = Puzzle(difficulty_level=0.2, size=2)
    puzzle.id = 1
    puzzle.puzzle_pieces = [
        PuzzlePiece(1, 0, 0, value=2, static_piece=True),
        PuzzlePiece(1, 1, 0, value=4, static_piece=True),
        PuzzlePiece(1, 2, 0, value=3, static_piece=True),
        PuzzlePiece(1, 3, 0, value=1, static_piece=True),
        PuzzlePiece(1, 0, 1, value=1, static_piece=True),
        PuzzlePiece(1, 1, 1, value=1, static_piece=False),
        PuzzlePiece(1, 2, 1, value=4, static_piece=True),
        PuzzlePiece(1, 3, 1, value=2, static_piece=True),
        PuzzlePiece(1, 0, 2, value=2, static_piece=False),
        PuzzlePiece(1, 1, 2, value=2, static_piece=True),
        PuzzlePiece(1, 2, 2, value=1, static_piece=True),
        PuzzlePiece(1, 3, 2, value=3, static_piece=True),
        PuzzlePiece(1, 0, 3, value=3, static_piece=True),
        PuzzlePiece(1, 1, 3, value=1, static_piece=True),
        PuzzlePiece(1, 2, 3, value=4, static_piece=False),
        PuzzlePiece(1, 3, 3, value=4, static_piece=True)
    ]
    return puzzle


@pytest.fixture(autouse=False)
def pieces():
    return [
        PuzzlePiece(1, 0, 0, value=2, static_piece=True),
        PuzzlePiece(1, 1, 0, value=4, static_piece=True),
        PuzzlePiece(1, 2, 0, value=3, static_piece=True),
        PuzzlePiece(1, 3, 0, value=1, static_piece=True),
        PuzzlePiece(1, 0, 1, value=1, static_piece=True),
        PuzzlePiece(1, 1, 1, value=1, static_piece=False),
        PuzzlePiece(1, 2, 1, value=4, static_piece=True),
        PuzzlePiece(1, 3, 1, value=2, static_piece=True),
        PuzzlePiece(1, 0, 2, value=2, static_piece=False),
        PuzzlePiece(1, 1, 2, value=2, static_piece=True),
        PuzzlePiece(1, 2, 2, value=1, static_piece=True),
        PuzzlePiece(1, 3, 2, value=3, static_piece=True),
        PuzzlePiece(1, 0, 3, value=3, static_piece=True),
        PuzzlePiece(1, 1, 3, value=1, static_piece=True),
        PuzzlePiece(1, 2, 3, value=4, static_piece=False),
        PuzzlePiece(1, 3, 3, value=4, static_piece=True)
    ]

def test_create_sudoku_puzzle_valid_defaults():
    """
    Make sure that it is possible to create a sudoku puzzle using defaults.
    """
    sudoku = Puzzle()
    assert sudoku.difficulty == 0.5
    assert sudoku.size == 3
    assert not sudoku.completed


def test_create_sudoku_puzzle_valid_specification():
    """
    Make sure that it is possible to create a sudoku puzzle by specifying difficulty and size.
    """
    sudoku = Puzzle(difficulty_level=0.6, size=4)
    assert sudoku.difficulty == 0.6
    assert sudoku.size == 4
    assert not sudoku.completed


def test_create_sudoku_puzzle_invalid_difficulty_str():
    """
    Make sure that it is NOT possible to create a sudoku puzzle by specifying invalid difficulty level
    that is not of type float.
    """
    with pytest.raises(PuzzleException) as pe:
        sudoku = Puzzle(difficulty_level='bad level', size=4)
        assert "Sudoku puzzle difficulty specified must be a float value" in str(pe.value)


def test_create_sudoku_puzzle_invalid_difficulty_too_low():
    """
    Make sure that it is NOT possible to create a sudoku puzzle by specifying invalid difficulty level
    that is out of range (too low).
    """
    with pytest.raises(PuzzleException) as pe:
        sudoku = Puzzle(difficulty_level=0.0, size=4)
        assert "Difficulty levels must range between" in str(pe.value)


def test_create_sudoku_puzzle_invalid_difficulty_too_high():
    """
    Make sure that it is NOT possible to create a sudoku puzzle by specifying invalid difficulty level
    that is out of range (too high).
    """
    with pytest.raises(PuzzleException) as pe:
        sudoku = Puzzle(difficulty_level=1.1, size=4)
        assert "Difficulty levels must range between" in str(pe.value)


def test_create_sudoku_puzzle_invalid_size_str():
    """
    Make sure that it is NOT possible to create a sudoku puzzle by specifying invalid size
    that is not of type int.
    """
    with pytest.raises(PuzzleException) as pe:
        sudoku = Puzzle(difficulty_level=0.3, size='invalid size')
        assert "Sudoku puzzle sizes specified must be valid integers" in str(pe.value)


def test_create_sudoku_puzzle_invalid_size_too_low():
    """
    Make sure that it is NOT possible to create a sudoku puzzle by specifying invalid size
    that is out of range (too low).
    """
    with pytest.raises(PuzzleException) as pe:
        sudoku = Puzzle(difficulty_level=0.5, size=0)
        assert "Valid sizes range from" in str(pe.value)


def test_create_sudoku_puzzle_invalid_size_too_high():
    """
    Make sure that it is NOT possible to create a sudoku puzzle by specifying invalid size
    that is out of range (too high).
    """
    with pytest.raises(PuzzleException) as pe:
        sudoku = Puzzle(difficulty_level=0.5, size=10)
        assert "Valid sizes range from" in str(pe.value)


def test_set_point_value1():
    """
    Make sure that point values are calculated correctly based on difficulty and size.
    """
    sudoku = Puzzle(difficulty_level=0.6, size=4)
    assert sudoku.point_value == 110


def test_set_point_value2():
    """
    Make sure that point values are calculated correctly based on difficulty and size.
    """
    sudoku = Puzzle(difficulty_level=0.2, size=3)
    assert sudoku.point_value == 50


def test_get_pieces_as_arr_all(incomplete_puzzle):
    """
    Test get the pieces as an array of values for testing
    """
    result = incomplete_puzzle.get_pieces_as_arr(static_only=False)
    expected = [[2, 4, 3, 1], [1, 3, 4, 2], [None, 2, 1, 3], [3, 1, None, 4]]
    assert result == expected


def test_get_pieces_as_arr_static_only(incomplete_puzzle):
    """
    Test get the pieces as an array of values for testing; this should be the original
    puzzle board ONLY
    """
    result = incomplete_puzzle.get_pieces_as_arr(static_only=True)
    expected = [[2, 4, 3, 1], [1, None, 4, 2], [None, 2, 1, 3], [3, 1, None, 4]]
    assert result == expected


def test_recreate_original_puzzle(incomplete_puzzle):
    """
    Test get the pieces as an array of values for testing; this should be the original
    puzzle board ONLY
    """
    result = incomplete_puzzle.recreate_original_puzzle_as_array()
    expected = [[2, 4, 3, 1], [1, None, 4, 2], [None, 2, 1, 3], [3, 1, None, 4]]
    assert result == expected


def test_check_for_completion_null_values(incomplete_puzzle):
    """
    A puzzle is not complete if there are pieces in the puzzle with null (i.e., None) values.
    """
    assert not incomplete_puzzle.is_complete_puzzle()


def test_check_for_completion_complete(complete_puzzle):
    """
    A puzzle that is complete should be deemed complete in the completeness check.
    """
    assert complete_puzzle.is_complete_puzzle()


def test_check_for_completion_incorrect_values(incorrect_puzzle):
    """
    A puzzle is not complete if there are pieces that are not valid.
    """
    assert not incorrect_puzzle.is_complete_puzzle()


def test_check_discrepancies_none(complete_puzzle):
    """
    A puzzle is not complete if there are pieces that are not valid.
    """
    assert [] == complete_puzzle.compare_with_solved_board()


def test_check_discrepancies_many_incorrect(incorrect_puzzle):
    """
    A puzzle is not complete if there are pieces that are not valid.
    """
    expected = [
        {'x_coordinate': 1, 'y_coordinate': 1},
        {'x_coordinate': 0, 'y_coordinate': 2},
        {'x_coordinate': 2, 'y_coordinate': 3}
    ]
    assert expected == incorrect_puzzle.compare_with_solved_board()


def test_check_discrepancies_incomplete_puzzle(incomplete_puzzle):
    """
    A puzzle is not complete if there are pieces that are not valid.
    """
    expected = [
        {'x_coordinate': 0, 'y_coordinate': 2},
        {'x_coordinate': 2, 'y_coordinate': 3}
    ]
    assert expected == incomplete_puzzle.compare_with_solved_board()


def test_get_puzzle_none(monkeypatch):
    class MockBaseQuery:

        def __init__(self, *args, **kwargs):
            pass

        def filter_by(self, *args, **kwargs):
            class Results():
                def first(self):
                    return None

            return Results()

        def join(self, *args, **kwargs):
            return

    monkeypatch.setattr('flask_sqlalchemy._QueryProperty.__get__', MockBaseQuery)
    assert Puzzle.get_puzzle(1) is None


def test_get_puzzle_found(monkeypatch, pieces):

    class MockBaseQuery:

        def __init__(self, *args, **kwargs):
            pass

        def filter_by(self, *args, **kwargs):
            class Results():
                def first(self):
                    return Puzzle(difficulty_level=0.2, size=2)

            return Results()

        def join(self, *args, **kwargs):
            return

    def mock_find_pieces(*args, **kwargs):
        return pieces

    monkeypatch.setattr('flask_sqlalchemy._QueryProperty.__get__', MockBaseQuery)
    monkeypatch.setattr(PuzzlePiece, "find_all_pieces", mock_find_pieces)

    result = Puzzle.get_puzzle(1)
    assert result.difficulty == 0.2
    assert result.size == 2
    assert result.puzzle_pieces == pieces


def test_save(monkeypatch, complete_puzzle):
    monkeypatch.setattr(db, "session", MockSession)

    result = complete_puzzle.save(autocommit=False)
    assert result == 1


def test_save_autocommit(monkeypatch, complete_puzzle):
    monkeypatch.setattr(db, "session", MockSession)

    result = complete_puzzle.save(autocommit=True)
    assert result == 1


def test_attempt_update_complete_puzzle(monkeypatch, complete_puzzle):
    with pytest.raises(PuzzleException) as pe:
        complete_puzzle.update(0, 0, 1)
        assert 'Updates cannot be made to previously completed puzzles.' in str(pe.value)


def test_update_invalid_coordinate1(monkeypatch, incomplete_puzzle):
    with pytest.raises(PuzzleException) as pe:
        incomplete_puzzle.update(1, 6, 1)
        assert 'Coordinates provided (1, 6) are outside the range of the puzzle.' in str(pe.value)


def test_update_invalid_coordinate2(monkeypatch, incomplete_puzzle):
    with pytest.raises(PuzzleException) as pe:
        incomplete_puzzle.update(1, -1, 1)
        assert 'Coordinates provided (1, -1) are outside the range of the puzzle.' in str(pe.value)


def test_update_invalid_coordinate3(monkeypatch, incomplete_puzzle):
    with pytest.raises(PuzzleException) as pe:
        incomplete_puzzle.update(6, 1, 1)
        assert 'Coordinates provided (6, 1) are outside the range of the puzzle.' in str(pe.value)


def test_update_invalid_coordinate4(monkeypatch, incomplete_puzzle):
    with pytest.raises(PuzzleException) as pe:
        incomplete_puzzle.update(-1, 1, 1)
        assert 'Coordinates provided (-1, 1) are outside the range of the puzzle.' in str(pe.value)


def test_update_invalid_value1(monkeypatch, incomplete_puzzle):
    with pytest.raises(PuzzleException) as pe:
        incomplete_puzzle.update(1, 1, 0)
        assert 'Invalid value provided (0)' in str(pe.value)


def test_update_invalid_value2(monkeypatch, incomplete_puzzle):
    with pytest.raises(PuzzleException) as pe:
        incomplete_puzzle.update(1, 1, 5)
        assert 'Invalid value provided (5)' in str(pe.value)


def test_update_valid(monkeypatch, incomplete_puzzle):
    monkeypatch.setattr(db, "session", MockSession)
    incomplete_puzzle.update(1, 1, 3)

    for piece in incomplete_puzzle.puzzle_pieces:
        if piece.x_coordinate == 1 and piece.y_coordinate == 1:
            assert piece.value == 3


def test_update_valid_complete_puzzle(monkeypatch, incomplete_puzzle):
    monkeypatch.setattr(db, "session", MockSession)
    incomplete_puzzle.update(2, 3, 2)
    incomplete_puzzle.update(0, 2, 4)   # this should result in a winning puzzle

    for piece in incomplete_puzzle.puzzle_pieces:
        if piece.x_coordinate == 2 and piece.y_coordinate == 3:
            assert piece.value == 2
        if piece.x_coordinate == 0 and piece.y_coordinate == 2:
            assert piece.value == 4

    assert incomplete_puzzle.completed


def test_set_puzzle_complete(monkeypatch, incomplete_puzzle):
    monkeypatch.setattr(db, "session", MockSession)
    incomplete_puzzle.set_puzzle_complete(autocommit=True)
    assert incomplete_puzzle.completed


def test_as_str(incomplete_puzzle):
    assert str(incomplete_puzzle) == 'SudokuPuzzle(id=1, difficulty=0.2, completed=False, point_value=30, size=2)'
