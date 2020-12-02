"""
Unit testing for sudoku resources.
"""
from flask import g, request
from backend import app, db
from backend.models.player import PuzzlePlayer
from backend.models.puzzle_exception import PuzzleException
from backend.models.sudoku_puzzle import Puzzle
from backend.models.user import User
from backend.resources.sudoku_puzzle_piece import SudokuPuzzlePiece
from backend.resources.sudoku_puzzle import SudokuPuzzle, sudoku_to_dict
from backend.resources.sudoku_puzzles import SudokuPuzzles
from backend.resources.sudoku_player import SudokuPlayer
from backend.config import UnitTestingConfig
from backend.decorators import handle_cors
from tests.unit.mocks import MockSession, user, mock_save, mock_get_puzzle, \
    mock_single_puzzles_for_player, mock_no_puzzles_for_player

app.config.from_object(UnitTestingConfig)


def raise_exception(*args, **kwargs):
    """Use to mock an unknown exception being raised in the route handling"""
    raise Exception("A very bad and unknown exception!")


def raise_known_exception(*args, **kwargs):
    """Use to mock an known exception, a PuzzleException, being raised in the route handling"""
    raise PuzzleException("A bad, but known exception!")


def test_sudoku_to_json():
    """
    Conversion of sudoku puzzle to json should be successful.
    """
    foobar = User('54321', 'foo', 'bar', 'foobar@comsci.com')
    foobar.id = 1

    princess = User('98734', 'Princess', 'Bride', 'princess@princessbride.com')
    princess.id = 2

    sudoku = Puzzle(difficulty_level=0.6, size=4)
    players = [foobar, princess]

    result = sudoku_to_dict(sudoku, players)

    # note that because you cannot predict what sudoku boards are created, not comparing pieces,
    # just for simplicity for now
    assert not result['puzzle_id']
    assert not result['completed']
    assert result['difficulty'] == 0.6
    assert result['point_value'] == 110
    assert result['players'] == [
        {'id': 1, 'first_name': 'foo', 'last_name': 'bar', 'email': 'foobar@comsci.com'},
        {'id': 2, 'first_name': 'Princess',
         'last_name': 'Bride', 'email': 'princess@princessbride.com'}
    ]


def test_get_sudoku_puzzles_none(mock_no_puzzles_for_player, user):
    """
    If there are no puzzles associated with the player, an attempt to get all puzzles should
    return nothing.
    """
    with app.app_context():
        puzzles_resource = SudokuPuzzles()
        g.user = user
        result = puzzles_resource.get()

    expected = {
        'message': 'No unhidden sudoku puzzles are associated with Jane Doe (id = 1)',
        'puzzles': []
    }
    assert result == expected


def test_get_sudoku_puzzles_one(monkeypatch, user, mock_get_puzzle):
    """
    If there are puzzles associated with the player, an attempt to get all puzzles should
    return all associated puzzles.
    """
    def mock_get_puzzles_for_player(*args, **kwargs):
        """Helper mock"""
        return [PuzzlePlayer(player_id=5, puzzle_id=3)]

    def mock_get_players(*args, **kwargs):
        """Helper mock"""
        return [
            User(first_name='Sally', last_name='Sue', email='sallysue@emails.com', g_id='123445')
        ]

    monkeypatch.setattr(PuzzlePlayer, 'find_all_puzzles_for_player', mock_get_puzzles_for_player)
    monkeypatch.setattr(PuzzlePlayer, 'find_players_for_puzzle', mock_get_players)

    with app.app_context():
        g.user = user
        puzzles_resource = SudokuPuzzles()
        result = puzzles_resource.get()

    expected = {'puzzles':
        [
            {'puzzle_id': None,
             'completed': False,
             'difficulty': 0.5,
             'point_value': 90,
             'pieces': [
                 {'x_coordinate': 0, 'y_coordinate': 1, 'static_piece': False, 'value': None},
                 {'x_coordinate': 1, 'y_coordinate': 1, 'static_piece': True, 'value': 3}
             ],
             'players': [
                 {'id': None,
                  'first_name': 'Sally',
                  'last_name': 'Sue',
                  'email': 'sallysue@emails.com'}
             ]
             }
        ]
    }
    assert result == expected


def test_get_sudoku_puzzles_many(monkeypatch, user, mock_get_puzzle):
    """
    If there are puzzles associated with the player, an attempt to get all puzzles should
    return all associated puzzles.
    """
    def mock_get_puzzles_for_player_duo(*args, **kwargs):
        """Mock get player puzzles"""
        return [PuzzlePlayer(player_id=5, puzzle_id=3), PuzzlePlayer(player_id=5, puzzle_id=4)]

    def mock_get_players_duo(*args, **kwargs):
        """Mock get players as Users"""
        return [
            User(first_name='Sally', last_name='Sue', email='sallysue@emails.com', g_id='123445'),
            User(first_name='Joe', last_name='Smith', email='joesmith@emails.com', g_id='123466')
        ]

    monkeypatch.setattr(PuzzlePlayer, 'find_all_puzzles_for_player',
                        mock_get_puzzles_for_player_duo)
    monkeypatch.setattr(PuzzlePlayer, 'find_players_for_puzzle',
                        mock_get_players_duo)

    with app.app_context():
        g.user = user
        puzzles_resource = SudokuPuzzles()
        result = puzzles_resource.get()

    expected = {
        'puzzles': [
            {
                'puzzle_id': None,
                'completed': False,
                'difficulty': 0.5,
                'point_value': 90,
                'pieces': [
                    {'x_coordinate': 0, 'y_coordinate': 1, 'static_piece': False, 'value': None},
                    {'x_coordinate': 1, 'y_coordinate': 1, 'static_piece': True, 'value': 3}
                ],
                'players': [
                    {'id': None, 'first_name': 'Sally',
                     'last_name': 'Sue', 'email': 'sallysue@emails.com'},
                    {'id': None, 'first_name': 'Joe', 'last_name': 'Smith',
                     'email': 'joesmith@emails.com'}
                ]
            },
            {
                'puzzle_id': None,
                'completed': False,
                'difficulty': 0.5,
                'point_value': 90,
                'pieces': [
                    {'x_coordinate': 0, 'y_coordinate': 1, 'static_piece': False, 'value': None},
                    {'x_coordinate': 1, 'y_coordinate': 1, 'static_piece': True, 'value': 3}
                ],
                'players': [
                    {'id': None, 'first_name': 'Sally', 'last_name': 'Sue',
                     'email': 'sallysue@emails.com'},
                    {'id': None, 'first_name': 'Joe', 'last_name': 'Smith',
                     'email': 'joesmith@emails.com'}
                ]
            }
        ]
    }
    assert result == expected


def test_sudoku_puzzles_create_known_exception(monkeypatch, user, mock_save):
    """
    If a known exception (Puzzle Exception) is raised during the processing
    of the request, the response should follow an expected format.
    """
    class MockParser:
        """
        Mock the parsing function of the endpoint.
        """
        def add_argument(self, *args, **kwargs):
            """
            Mock add argument, do nothing
            """
            return

        def parse_args(self):
            """
            Mock parse args, return known dictionary
            """
            return {
                'difficulty': 0.5,
                'size': 5,
                'additional_players': ['johnsmith@js.com']
            }

    monkeypatch.setattr(Puzzle, 'set_pieces', lambda x: None)  # to speed up tests
    monkeypatch.setattr(PuzzlePlayer, 'save', raise_known_exception)

    with app.app_context():
        g.user = user
        puzzles_resource = SudokuPuzzles()
        puzzles_resource.parser = MockParser()
        result = puzzles_resource.post()

    expected = ({'message': 'Failed to create new Sudoku Puzzle',
                 'reason': "A bad, but known exception!"}, 400)
    assert result == expected


def test_get_sudoku_puzzles_create_one_unknown_exception(monkeypatch, user, mock_save):
    """
    If an unknown exception (Puzzle Exception) is raised during the
    processing of the request, the response should follow an expected format.
    """

    class MockParser:
        """
        Mock the parsing function of the endpoint.
        """
        def add_argument(self, *args, **kwargs):
            """
            Mock add arguments, do nothing
            """
            return

        def parse_args(self):
            """
            Mock parse arguments, return known dict
            """
            return {
                'difficulty': 0.5,
                'size': 5,
                'additional_players': ['johnsmith@js.com']
            }

    monkeypatch.setattr(Puzzle, 'set_pieces', lambda x: None)  # to speed up tests
    monkeypatch.setattr(PuzzlePlayer, 'save', raise_exception)

    with app.app_context():
        g.user = user
        puzzles_resource = SudokuPuzzles()
        puzzles_resource.parser = MockParser()
        result = puzzles_resource.post()

    expected = ({'message': 'Failed to create new Sudoku Puzzle'}, 500)
    assert result == expected


def test_create_puzzle_no_others(monkeypatch, user, mock_save):
    """
    A valid request to create a puzzle should be successful.
    """
    class MockParser:
        """
        Mock the parsing function of the endpoint.
        """
        def add_argument(self, *args, **kwargs):
            """Mock add argument, do nothing."""
            return

        def parse_args(self):
            """Mock the parsing function by returning known dict"""
            return {
                'difficulty': 0.5,
                'size': 5
            }

    monkeypatch.setattr(Puzzle, 'set_pieces', lambda x: None)  # to speed up tests
    monkeypatch.setattr(db, "session", MockSession)

    with app.app_context():
        g.user = user
        puzzles_resource = SudokuPuzzles()
        puzzles_resource.parser = MockParser()
        result = puzzles_resource.post()

    expected = {
        'message': 'New Sudoku puzzle successfully created',
        'difficulty': 0.5,
        'size': 5,
        'puzzle_id': 1,
        'unregistered_emails': []
    }
    assert result == expected


def test_create_puzzle_unregistered_other(monkeypatch, user, mock_save):
    """
    A valid request to create a puzzle should be successful.
    """
    class MockParser:
        """
        Mock the parsing function of the endpoint.
        """
        def add_argument(self, *args, **kwargs):
            """Mock add argument, do nothing."""
            return

        def parse_args(self):
            """Mock the parsing function by returning known dict"""
            return {
                'difficulty': 0.5,
                'size': 5,
                'additional_players': ['johnsmith@js.com']
            }

    def mock_find_players_by_email(*args, **kwargs):
        """Helper mock"""
        return [], ['johnsmith@js.com']

    monkeypatch.setattr(Puzzle, 'set_pieces', lambda x: None)  # to speed up tests
    monkeypatch.setattr(db, "session", MockSession)
    monkeypatch.setattr(User, "find_users_by_email", mock_find_players_by_email)

    with app.app_context():
        g.user = user
        puzzles_resource = SudokuPuzzles()
        puzzles_resource.parser = MockParser()
        result = puzzles_resource.post()

    expected = {
        'message': 'New Sudoku puzzle successfully created',
        'difficulty': 0.5,
        'size': 5,
        'puzzle_id': 1,
        'unregistered_emails': ['johnsmith@js.com']
    }
    assert result == expected


def test_create_puzzle_registered_others(monkeypatch, user, mock_save):
    """
    A valid request to create a puzzle should be successful.
    """
    class MockParser:
        """
        Mock the parsing function of the endpoint.
        """
        def add_argument(self, *args, **kwargs):
            """Mock add argument, do nothing."""
            return

        def parse_args(self):
            """Mock the parsing function by returning known dict"""
            return {
                'difficulty': 0.5,
                'size': 5,
                'additional_players': ['johnsmith@js.com', 'applegate@fruits.com',
                                       'paulrevere@independence.com']
            }

    def mock_find_players_by_email(*args, **kwargs):
        """Helper mock"""
        user1 = User(g_id='923423', first_name="Jane", last_name="Doe", email='johnsmith@js.com')
        user2 = User(g_id='333', first_name="Joe", last_name="Doe", email='applegate@fruits.com')
        user3 = User(g_id='444', first_name="Dan", last_name="Doe", email='revere@independence.com')
        return [user1, user2, user3], []

    monkeypatch.setattr(Puzzle, 'set_pieces', lambda x: None)  # to speed up tests
    monkeypatch.setattr(db, "session", MockSession)
    monkeypatch.setattr(User, "find_users_by_email", mock_find_players_by_email)
    monkeypatch.setattr(PuzzlePlayer, "find_players_for_puzzle", lambda x: [user])

    with app.app_context():
        g.user = user
        puzzles_resource = SudokuPuzzles()
        puzzles_resource.parser = MockParser()
        result = puzzles_resource.post()

    expected = {
        'message': 'New Sudoku puzzle successfully created',
        'difficulty': 0.5,
        'size': 5,
        'puzzle_id': 1,
        'unregistered_emails': []
    }
    assert result == expected


def test_create_puzzle_registered_duplicates(monkeypatch, user, mock_save):
    """
    A valid request to create a puzzle should be successful. If there are duplicate
    users specified in additional players, system should process only distinct values.
    """
    class MockParser:
        """Mock the parsing function of the endpoint."""
        def add_argument(self, *args, **kwargs):
            """Mock add argument, do nothing."""
            return

        def parse_args(self):
            """Mock the parsing function by returning known dict"""
            return {
                'difficulty': 0.5,
                'size': 5,
                'additional_players': ['johnsmith@js.com',
                                       'paulrevere@independence.com', 'paulrevere@independence.com']
            }

    def mock_find_players_by_email(*args, **kwargs):
        """Helper mock"""
        user1 = User(g_id='923423', first_name="Jane", last_name="Doe", email='johnsmith@js.com')
        return [user1], ['paulrevere@independence.com']

    monkeypatch.setattr(Puzzle, 'set_pieces', lambda x: None)  # to speed up tests
    monkeypatch.setattr(db, "session", MockSession)
    monkeypatch.setattr(User, "find_users_by_email", mock_find_players_by_email)
    monkeypatch.setattr(PuzzlePlayer, "find_players_for_puzzle", lambda x: [user])

    with app.app_context():
        g.user = user
        puzzles_resource = SudokuPuzzles()
        puzzles_resource.parser = MockParser()
        result = puzzles_resource.post()

    expected = {
        'message': 'New Sudoku puzzle successfully created',
        'difficulty': 0.5,
        'size': 5,
        'puzzle_id': 1,
        'unregistered_emails': ['paulrevere@independence.com']
    }
    assert result == expected


def test_create_puzzle_self_added_as_additional_player(monkeypatch, user, mock_save):
    """
    A valid request to create a puzzle should be successful. If the username of
    the person is specified (it does not need to be), it should not be considered
    an additional player.
    """
    class MockParser:
        """Mock the parsing function of the endpoint."""
        def add_argument(self, *args, **kwargs):
            """Mock add argument, do nothing."""
            return

        def parse_args(self):
            """Mock the parsing function by returning known dict"""
            return {
                'difficulty': 0.5,
                'size': 5,
                'additional_players': ['janedoe1@tests.com']
            }

    def mock_find_players_by_email(*args, **kwargs):
        """Helper mock"""
        return [user], []

    monkeypatch.setattr(Puzzle, 'set_pieces', lambda x: None)  # to speed up tests
    monkeypatch.setattr(db, "session", MockSession)
    monkeypatch.setattr(User, "find_users_by_email", mock_find_players_by_email)
    monkeypatch.setattr(PuzzlePlayer, "find_players_for_puzzle", lambda x: [user])

    with app.app_context():
        g.user = user
        puzzles_resource = SudokuPuzzles()
        puzzles_resource.parser = MockParser()
        result = puzzles_resource.post()

    expected = {
        'message': 'New Sudoku puzzle successfully created',
        'difficulty': 0.5,
        'size': 5,
        'puzzle_id': 1,
        'unregistered_emails': []
    }
    assert result == expected


def test_sudoku_puzzles_too_many_additional(monkeypatch, user, mock_save):
    """
    A valid request to create a puzzle should be successful.
    """
    class MockParser:
        """
        Mock the parsing function of the endpoint.
        """
        def add_argument(self, *args, **kwargs):
            """Mock add argument, do nothing."""
            return

        def parse_args(self):
            """Mock the parsing function by returning known dict"""
            return {
                'difficulty': 0.5,
                'size': 5,
                'additional_players': ['johnsmith@js.com', 'applegate@fruits.com',
                                       'paulrevere@independence.com', 'anotheruser.com']
            }

    with app.app_context():
        g.user = user
        puzzles_resource = SudokuPuzzles()
        puzzles_resource.parser = MockParser()
        result = puzzles_resource.post()

    expected = ({
        'message': 'Failed to create new Sudoku Puzzle',
        'reason': 'Too many additional players have been specified;'
                  ' the total number of players allowed per puzzle is 4'}, 400)
    assert result == expected


def test_set_puzzle_visibility_hidden(monkeypatch, mock_single_puzzles_for_player, user):
    """
    Test to ensure that visbility can be set to hidden.
    """
    class MockParser:
        """Mock the parsing function of the endpoint."""
        def add_argument(self, *args, **kwargs):
            """Mock add argument, do nothing."""
            return

        def parse_args(self):
            """Mock the parsing function by returning known dic"""
            return {'hidden': True}

    monkeypatch.setattr(db, "session", MockSession)

    with app.app_context():
        puzzles_resource = SudokuPuzzle()
        puzzles_resource.parser = MockParser()
        g.user = user
        result = puzzles_resource.post(puzzle_id=1)

    expected = {'message': 'Successfully updated the visibility of puzzle 1 '
                           'for player 1 to hidden = True'}
    assert expected == result


def test_set_puzzle_visibility_visible(monkeypatch, mock_single_puzzles_for_player, user):
    """
    Test to ensure that visibility can be set to not hidden.
    """
    class MockParser:
        """Mock the parsing function of the endpoint."""
        def add_argument(self, *args, **kwargs):
            """Mock add argument, do nothing."""
            return

        def parse_args(self):
            """Mock the parsing function by returning known dic"""
            return {'hidden': False}

    monkeypatch.setattr(db, "session", MockSession)

    with app.app_context():
        puzzles_resource = SudokuPuzzle()
        puzzles_resource.parser = MockParser()
        g.user = user
        result = puzzles_resource.post(puzzle_id=1)

    expected = {
        'message': 'Successfully updated the visibility of puzzle 1 for player 1 to hidden = False'
    }
    assert expected == result


def test_set_puzzle_visibility_not_available(monkeypatch, mock_single_puzzles_for_player, user):
    """
    Test for when a user wants to change visibility, but the puzzle is not
    existent or not associated with them.
    """
    with app.app_context():
        puzzles_resource = SudokuPuzzle()
        g.user = user
        result = puzzles_resource.post(puzzle_id=2)

    expected = ({'message': 'Puzzle requested does not exist or is not associated '
                            'with user Jane Doe (id = 1)'}, 404)
    assert expected == result


def test_set_puzzle_visibility_exception(monkeypatch, mock_single_puzzles_for_player, user):
    """
    Test for when a user wants to change visibility, but the puzzle is not
    existent or not associated with them.
    """
    class MockParser:
        """Mock the parsing function of the endpoint."""
        def add_argument(self, *args, **kwargs):
            """Mock add argument, do nothing."""
            return

        def parse_args(self):
            """Mock the parsing function by returning known dict"""
            return {'hidden': True}

    monkeypatch.setattr(PuzzlePlayer, 'update_visibility', raise_exception)

    with app.app_context():
        puzzles_resource = SudokuPuzzle()
        puzzles_resource.parser = MockParser()
        g.user = user
        result = puzzles_resource.post(puzzle_id=1)

    expected = ({'message': 'Attempt to edit the visibility of puzzle failed',
                 'reason': 'Unknown error occurred.'}, 500)
    assert expected == result


def test_get_sudoku_puzzle_none_retrieved(mock_no_puzzles_for_player, user):
    """
    If an attempt is made to a get a puzzle that doesn't exist, the response should
    provide an alert that the puzzle doesn't exist.
    """
    with app.app_context():
        puzzles_resource = SudokuPuzzle()
        g.user = user
        result = puzzles_resource.get(1)

    expected = ({'message': 'Puzzle requested does not exist or is '
                            'not associated with user Jane Doe (id = 1)'}, 404)
    assert result == expected


def test_get_sudoku_puzzle_none_associated(monkeypatch, user):
    """
    If an attempt is made to a get a puzzle that is not associated with
    the user, the response should provide an alert that the puzzle is not accessible to them.
    """
    def mock_get_puzzles_for_player(*args, **kwargs):
        return [PuzzlePlayer(3, 2)]

    monkeypatch.setattr(PuzzlePlayer, 'find_all_puzzles_for_player', mock_get_puzzles_for_player)

    with app.app_context():
        puzzles_resource = SudokuPuzzle()
        g.user = user
        result = puzzles_resource.get(1)

    expected = ({'message': 'Puzzle requested does not exist or is '
                            'not associated with user Jane Doe (id = 1)'}, 404)
    assert result == expected


def test_get_sudoku_puzzle_found(monkeypatch, mock_get_puzzle, mock_single_puzzles_for_player,
                                 user):
    """
    If an attempt is made to a get a puzzle that is associated with a user, the response should
    successfully return that puzzle.
    """
    def mock_get_players(*args, **kwargs):
        user = User(first_name='Sally', last_name='Sue', email='sallysue@emails.com', g_id='123445')
        user.id = 1
        return [user]

    monkeypatch.setattr(PuzzlePlayer, 'find_players_for_puzzle', mock_get_players)

    with app.app_context():
        puzzles_resource = SudokuPuzzle()
        g.user = user
        result = puzzles_resource.get(1)

    expected = {'puzzle_id': None, 'completed': False, 'difficulty': 0.5, 'point_value': 90,
                'pieces': [
                    {'x_coordinate': 0, 'y_coordinate': 1, 'static_piece': False, 'value': None},
                    {'x_coordinate': 1, 'y_coordinate': 1, 'static_piece': True, 'value': 3}],
                'players': [{'id': 1, 'first_name': 'Sally', 'last_name': 'Sue',
                             'email': 'sallysue@emails.com'}]}
    assert result == expected


def test_join_sudoku_puzzle_already_joined(monkeypatch, user, mock_single_puzzles_for_player):
    """
    If an attempt is made to join a puzzle that a player already exists
    in, they cannot be added twice.
    """
    with app.app_context():
        player_resource = SudokuPlayer()
        g.user = user
        result = player_resource.post(1)

    expected = {'message': "Jane Doe (id = 1) is already is associated with puzzle 1."}
    assert result == expected


def test_join_sudoku_puzzle(monkeypatch, user, mock_no_puzzles_for_player):
    """
    If an attempt is made to join a puzzle that they do not currently exist in, then the attempt
    should be successful.
    """
    def mock_add_player(*args, **kwargs):
        return None

    monkeypatch.setattr(PuzzlePlayer, 'add_player_to_puzzle', mock_add_player)

    with app.app_context():
        player_resource = SudokuPlayer()
        g.user = user
        result = player_resource.post(1)

    expected = {'message': "Successfully added Jane Doe (id = 1) to puzzle with id 1."}
    assert result == expected


def test_join_sudoku_puzzle_full(monkeypatch, user, mock_no_puzzles_for_player):
    """
    If an attempt is made to join a puzzle that they do not currently exist in, then the attempt
    should be successful.
    """
    def mock_add_player(*args, **kwargs):
        raise PuzzleException("There are already 4 players affiliated with puzzle 1")

    monkeypatch.setattr(PuzzlePlayer, 'add_player_to_puzzle', mock_add_player)

    with app.app_context():
        player_resource = SudokuPlayer()
        g.user = user
        result = player_resource.post(1)

    expected = ({'message': 'Attempt to add Jane Doe (id = 1) to puzzle 1 failed.',
                 'reason': 'There are already 4 players affiliated with puzzle 1'}, 400)
    assert result == expected


def test_join_sudoku_puzzle_known_exception(monkeypatch, user, mock_no_puzzles_for_player):
    """
    If an attempt is made to join a puzzle, but an Puzzle Exception is thrown, the response should
    follow a known format.
    """
    monkeypatch.setattr(PuzzlePlayer, 'add_player_to_puzzle', raise_known_exception)

    with app.app_context():
        player_resource = SudokuPlayer()
        g.user = user
        result = player_resource.post(1)

    expected = ({'message': 'Attempt to add Jane Doe (id = 1) to puzzle 1 failed.',
                 'reason': 'A bad, but known exception!'}, 400)
    assert result == expected


def test_join_sudoku_puzzle_unknown_exception(monkeypatch, user, mock_no_puzzles_for_player):
    """
    If an attempt is made to join a puzzle, but an unkonwn Exception is thrown,
    the response should follow a known format.
    """
    def mock_add_player(*args, **kwargs):
        raise Exception("A very bad exception!")

    monkeypatch.setattr(PuzzlePlayer, 'add_player_to_puzzle', mock_add_player)

    with app.app_context():
        player_resource = SudokuPlayer()
        g.user = user
        result = player_resource.post(1)

    expected = ({'message': 'Attempt to add Jane Doe (id = 1) to puzzle 1 failed.',
                 'reason': 'Unknown error occurred.'}, 500)
    assert result == expected


def test_sudoku_puzzles_add_move_not_associated(monkeypatch, user,
                                                    mock_single_puzzles_for_player):
    """
    If a player attempts to make a move on a puzzle that they are not associated with,
    the attempt should fail.
    """
    class MockParser:
        """
        Mock the parsing function of the endpoint.
        """
        def add_argument(self, *args, **kwargs):
            """Mock add argument, do nothing."""
            return

        def parse_args(self):
            """Mock the parsing function by returning known dict"""
            return {
                'x_coordinate': 0,
                'y_coordinate': 1,
                'value': 1
            }

    with app.app_context():
        g.user = user
        puzzle_piece_resource = SudokuPuzzlePiece()
        puzzle_piece_resource.parser = MockParser()
        result = puzzle_piece_resource.post(2)

    expected = (
    {'message': 'Puzzle requested does not exist or is not associated with Jane Doe (id = 1).'},
    404)
    assert result == expected


def test_sudoku_puzzles_add_move_success(monkeypatch, user, mock_single_puzzles_for_player,
                                     mock_get_puzzle):
    """
    If a player attempts to make a move on a puzzle that they are associated with,
    the attempt should be successful.
    """
    class MockParser:
        """
        Mock the parsing function of the endpoint.
        """
        def add_argument(self, *args, **kwargs):
            """
            Mock add argument, do nothing.
            """
            return

        def parse_args(self):
            """
            Mock the parsing function by returning known dict
            """
            return {
                'x_coordinate': 0,
                'y_coordinate': 1,
                'value': 1
            }

    monkeypatch.setattr(db, "session", MockSession)

    with app.app_context():
        g.user = user
        puzzle_piece_resource = SudokuPuzzlePiece()
        puzzle_piece_resource.parser = MockParser()
        result = puzzle_piece_resource.post(1)

    expected = {'message': 'Successfully saved the submission of 1 at '
                           '(0, 1) on puzzle_id 1 by Jane Doe (id = 1)'}
    assert result == expected


def test_get_sudoku_puzzles_add_position_invalid(monkeypatch, user, mock_single_puzzles_for_player,
                                             mock_get_puzzle):
    """
    If a player attempts to make an invalid move on a puzzle that they are
    associated with, the request should not be successful.
    """
    class MockParser:
        """
        Mock the parsing function of the endpoint.
        """
        def add_argument(self, *args, **kwargs):
            """
            Mock add argument, do nothing.
            """
            return

        def parse_args(self):
            """
            Mock the parsing function by returning known dict
            """
            return {
                'x_coordinate': 0,
                'y_coordinate': 100,
                'value': 1
            }

    monkeypatch.setattr(db, "session", MockSession)

    with app.app_context():
        g.user = user
        puzzle_piece_resource = SudokuPuzzlePiece()
        puzzle_piece_resource.parser = MockParser()
        result = puzzle_piece_resource.post(1)

    expected = ({'message': 'Attempt to save 1 at (0, 100) on '
                            'puzzle_id 1 by user Jane Doe (id = 1) was unsuccessful',
                 'reason': 'Coordinates provided (0, 100) are outside the range of the puzzle. '
                           'Available coordinates are (0, 0) to (9, 9).'}, 400)
    assert result == expected


def test_get_sudoku_puzzles_add_value_invalid(monkeypatch, user, mock_single_puzzles_for_player,
                                             mock_get_puzzle):
    """
    If a player attempts to make an invalid move on a puzzle that they are
    associated with, the request should not be successful.
    """
    class MockParser:
        """
        Mock the parsing function of the endpoint.
        """
        def add_argument(self, *args, **kwargs):
            """
            Mock add argument, do nothing.
            """
            return

        def parse_args(self):
            """
            Mock the parsing function by returning known dict
            """
            return {
                'x_coordinate': 0,
                'y_coordinate': 0,
                'value': -1
            }

    monkeypatch.setattr(db, "session", MockSession)

    with app.app_context():
        g.user = user
        puzzle_piece_resource = SudokuPuzzlePiece()
        puzzle_piece_resource.parser = MockParser()
        result = puzzle_piece_resource.post(1)

    expected = ({'message': 'Attempt to save -1 at (0, 0) on puzzle_id 1 by user '
                            'Jane Doe (id = 1) was unsuccessful',
                 'reason': 'Invalid value provided (-1). Available values are 1 to 9.'}, 400)
    assert result == expected


def test_get_sudoku_puzzles_add_move_exception(monkeypatch, user, mock_single_puzzles_for_player,
                                               mock_get_puzzle):
    """
    If a player attempts to make a move on the puzzle, but an exception is raised,
    the response should follow a predictable format.
    """

    class MockParser:
        """
        Mock the parsing function of the endpoint.
        """
        def add_argument(self, *args, **kwargs):
            """
            Mock add argument, do nothing.
            """
            return

        def parse_args(self):
            """
            Mock the parsing function by returning known dict
            """
            return {
                'x_coordinate': 0,
                'y_coordinate': 100,
                'value': 1
            }

    monkeypatch.setattr(Puzzle, 'update', raise_exception)
    monkeypatch.setattr(db, "session", MockSession)

    with app.app_context():
        g.user = user
        puzzle_piece_resource = SudokuPuzzlePiece()
        puzzle_piece_resource.parser = MockParser()
        result = puzzle_piece_resource.post(1)

    expected = ({'message': 'Unexpected error occurred while adding new value to puzzle'}, 500)
    assert result == expected


def test_get_sudoku_puzzles_delete_piece(monkeypatch, user, mock_single_puzzles_for_player,
                                         mock_get_puzzle):
    """
    If a player attempts to make a move on a puzzle that they are associated
    with, the attempt should be successful.
    """
    class MockParser:
        """
        Mock the parsing function of the endpoint.
        """
        def add_argument(self, *args, **kwargs):
            """
            Mock add argument, do nothing.
            """
            return

        def parse_args(self):
            """
            Mock the parsing function by returning known dict
            """
            return {'x_coordinate': 0, 'y_coordinate': 1}

    monkeypatch.setattr(db, "session", MockSession)

    with app.app_context():
        g.user = user
        puzzle_piece_resource = SudokuPuzzlePiece()
        puzzle_piece_resource.parser = MockParser()
        result = puzzle_piece_resource.delete(1)

    expected = {'message': 'Successfully deleted piece at position (0, 1) on puzzle_id 1.'}
    assert result == expected


def test_get_sudoku_puzzles_delete_piece_invalid(monkeypatch, user, mock_single_puzzles_for_player,
                                                 mock_get_puzzle):
    """
    If a player attempts to make a move on a puzzle that they are associated with,
    the attempt should be successful, unless the piece is static.
    """
    class MockParser:
        """ Mock the parsing function of the endpoint."""
        def add_argument(self, *args, **kwargs):
            """ Mock add argument, do nothing."""
            return

        def parse_args(self):
            """ Mock the parsing function by returning known dict """
            return {'x_coordinate': 1,'y_coordinate': 1}

    monkeypatch.setattr(db, "session", MockSession)

    with app.app_context():
        g.user = user
        puzzle_piece_resource = SudokuPuzzlePiece()
        puzzle_piece_resource.parser = MockParser()
        result = puzzle_piece_resource.delete(1)

    expected = ({'message': 'Attempt to delete piece at (1, 1) on puzzle_id 1 by user Jane Doe '
                            '(id = 1) was unsuccessful',
                 'reason': 'Changes can only be made to non-static puzzle pieces.'}, 400)
    assert result == expected


def test_get_sudoku_puzzles_delete_piece_not_associated(monkeypatch, user):
    """
    If a player attempts to delete a puzzle entry on a puzzle that they are not associated
    with then it should be unsuccessful.
    """
    class MockParser:
        """ Mock the parsing function of the endpoint."""
        def add_argument(self, *args, **kwargs):
            """ Mock add argument, do nothing."""
            return

        def parse_args(self):
            """ Mock the parsing function by returning known dict """
            return {'x_coordinate': 0,'y_coordinate': 1}

    monkeypatch.setattr(SudokuPuzzlePiece, "player_associated_with_puzzle", lambda x, y: False)

    with app.app_context():
        g.user = user
        puzzle_piece_resource = SudokuPuzzlePiece()
        puzzle_piece_resource.parser = MockParser()
        result = puzzle_piece_resource.delete(1)

    expected = {'message': 'Puzzle requested does not exist or '
                           'is not associated with Jane Doe (id = 1)'}, 404
    assert result == expected


def test_get_sudoku_puzzles_delete_piece_exception(monkeypatch, user,
                                                   mock_single_puzzles_for_player, mock_get_puzzle):
    """
    If a player attempts to delete a puzzle entry on a puzzle that they are not associated
    with then it should be unsuccessful.
    """
    class MockParser:
        """ Mock the parsing function of the endpoint."""
        def add_argument(self, *args, **kwargs):
            """ Mock add argument, do nothing."""
            return

        def parse_args(self):
            """ Mock the parsing function by returning known dict """
            return {'x_coordinate': 0,'y_coordinate': 1}

    monkeypatch.setattr(db, "session", MockSession)
    monkeypatch.setattr(Puzzle, 'get_puzzle', lambda x: raise_exception)

    with app.app_context():
        g.user = user
        puzzle_piece_resource = SudokuPuzzlePiece()
        puzzle_piece_resource.parser = MockParser()
        result = puzzle_piece_resource.delete(1)

    expected = ({'message': 'Unexpected error occurred while deleting value from puzzle'}, 500)
    assert result == expected
