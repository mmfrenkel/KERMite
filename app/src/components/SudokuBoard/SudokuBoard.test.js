import React from 'react';
import { render, act, screen, fireEvent, getByTestId } from "@testing-library/react";
import userEvent from '@testing-library/user-event'
import SudokuBoard from './SudokuBoard';
import CurrentUserContext from '../../context/CurrentUserContext';
import {PIECES} from '../../data/get_puzzle_response'
import Endpoint from '../../utils/Endpoint';
import {getSolvedSolutionResponse, getSolutionResponse} from '../../data/get_solution_response';

function getSocket({emitFn = jest.fn(), onFn = jest.fn()} = {}) {
  return {
    current: {
      emit: emitFn,
      on: onFn,
    },
  };
}

let playerNum = 0;
function getPlayer({
  id = playerNum++,
  first_name = `Joe${playerNum}`,
  last_name = `Shmoe${playerNum}`,
  email = `joseph${playerNum}.shmoe@gshmail.com`,
} = {}) {
  return {
    id,
    first_name,
    last_name,
    email,
  }
}

function getPlayers() {
  const players = [];
  for (let i = 0; i < 4; i++) {
    players.push(getPlayer());
  }
  return players;
}

function getEmptyPieces() {
  const emptyPieces = [];
  for (let x = 0; x < 9; x++) {
    for (let y = 0; y < 9; y++) {
      emptyPieces.push({
        "x_coordinate": x,
        "y_coordinate": y,
        "static_piece": false,
        "value": null,
      });
    }
  }
  return emptyPieces;
}

describe('SudokuBoard', () => {
  it('shows loading text when the puzzle is loading', async () => {
    render(
      <CurrentUserContext.Provider value={{userEmail:"bobsmith@gmail.com", userName:"Bob Smith"}}>
        <SudokuBoard 
          players={[]}
          playersLockingCells={{}}
          gridState={null}
          puzzleId="1"
          solved={false}
          ref={getSocket()}
        />
      </CurrentUserContext.Provider>
    );
    const loadingMessages = await screen.findAllByText("Loading puzzle...");
    expect(loadingMessages).toHaveLength(1);
  });

  it('shows puzzle grid when the puzzle has loaded', async () => {
    const {getAllByTestId} = render(
      <CurrentUserContext.Provider value={{userEmail:"bobsmith@gmail.com", userName:"Bob Smith"}}>
        <SudokuBoard 
          players={[]}
          playersLockingCells={{}}
          gridState={PIECES}
          puzzleId="1"
          solved={false}
          ref={getSocket()}
        />
      </CurrentUserContext.Provider>
    );
    const sudokuCells = getAllByTestId('sudoku-cell');
    expect(sudokuCells).toHaveLength(81);
  });

  it('emits add_lock event when nonempty number is entered', () => {
    const emit = jest.fn();
    const socket = getSocket({emitFn: emit});
    const [currentPlayer, ...otherPlayers] = getPlayers();
    const {getAllByTestId} = render(
      <CurrentUserContext.Provider value={{userEmail: currentPlayer.email, userName: `${currentPlayer.first_name} ${currentPlayer.last_name}`}}>
        <SudokuBoard 
          players={otherPlayers.concat(currentPlayer)}
          playersLockingCells={{}}
          gridState={getEmptyPieces()}
          puzzleId={'1'}
          solved={false}
          ref={socket}
        />
      </CurrentUserContext.Provider>
    );
    
    const sudokuCells = getAllByTestId('sudoku-cell');
    const emptyCell = sudokuCells[0];
    act(() => {
      fireEvent.focus(emptyCell);
      fireEvent.keyDown(emptyCell);
    });
    expect(emit).toHaveBeenCalledWith('add_lock', {
      "player": currentPlayer, "puzzle_id": "1", "x_coordinate": 0, "y_coordinate": 0});
  });

  it('emits remove_lock event when a user moves away', () => {
    const emit = jest.fn();
    const socket = getSocket({emitFn: emit});
    const [currentPlayer, ...otherPlayers] = getPlayers();
    const {getAllByTestId} = render(
      <CurrentUserContext.Provider value={{userEmail: currentPlayer.email, userName: `${currentPlayer.first_name} ${currentPlayer.last_name}`}}>
        <SudokuBoard 
          players={otherPlayers.concat(currentPlayer)}
          playersLockingCells={{}}
          gridState={getEmptyPieces()}
          puzzleId={'1'}
          solved={false}
          ref={socket}
        />
      </CurrentUserContext.Provider>
    );
    
    const sudokuCells = getAllByTestId('sudoku-cell');
    const emptyCell = sudokuCells[0];
    act(() => {
      fireEvent.blur(emptyCell);
    });
    expect(emit).toHaveBeenCalledWith('remove_lock', {
      "puzzle_id": "1", "x_coordinate": 0, "y_coordinate": 0});
  });

  it('calls the move endpoint when an input is made', async () => {
    jest.spyOn(Endpoint, "movePiece").mockImplementation(() => 'http://foo.bar.com:5000/puzzles/1/piece');
    const fetchSpy = jest.spyOn(global, "fetch");
    fetchSpy.mockImplementation(() => Promise.resolve({}));

    const {getAllByTestId} = render(
      <CurrentUserContext.Provider value={{userEmail:"bobsmith@gmail.com", userName:"Bob Smith"}}>
        <SudokuBoard 
          players={getPlayers()}
          playersLockingCells={{}}
          gridState={getEmptyPieces()}
          puzzleId="1"
          solved={false}
          ref={getSocket()}
        />
      </CurrentUserContext.Provider>
    );

    const sudokuCells = getAllByTestId('sudoku-cell');
    act(() => {
      userEvent.type(sudokuCells[0], '2');
    });

    expect(fetchSpy).toHaveBeenCalledWith('http://foo.bar.com:5000/puzzles/1/piece', {
      "body": "{\"x_coordinate\":0,\"y_coordinate\":0,\"value\":2}",
     "headers": {
       "Authorization": "Bearer undefined",
       "Content-Type": "application/json",
     },
     "method": "POST",
    });
  });

  it('calls the solution endpoint when then Check Solution button is clicked', async () => {
    const fetchSpy = jest.spyOn(global, "fetch");
    fetchSpy.mockImplementation(() => Promise.resolve(getSolvedSolutionResponse()));
    const {getByTestId} = render(
      <CurrentUserContext.Provider value={{userEmail:"bobsmith@gmail.com", userName:"Bob Smith"}}>
        <SudokuBoard 
          players={[]}
          playersLockingCells={{}}
          gridState={PIECES}
          puzzleId="1"
          solved={false}
          ref={getSocket()}
        />
      </CurrentUserContext.Provider>
    );
    act(() => {
      fireEvent.click(getByTestId('check-soln-btn'));
    });
    expect(fetchSpy).toHaveBeenCalledTimes(1);
  });

  it('shows that the puzzle has errors when the check solution button is clicked, but the grid contains mistakes', async () => {
    jest.spyOn(global, "fetch").mockImplementation(() => Promise.resolve(getSolutionResponse()));
    const {getByTestId} = render(
      <CurrentUserContext.Provider value={{userEmail:"bobsmith@gmail.com", userName:"Bob Smith"}}>
        <SudokuBoard 
          players={[]}
          playersLockingCells={{}}
          gridState={PIECES}
          puzzleId="1"
          solved={false}
          ref={getSocket()}
        />
      </CurrentUserContext.Provider>
    );
    act(() => {
      fireEvent.click(getByTestId('check-soln-btn'));
    });
    const statusMessage = await screen.findAllByText("Something's Not Right...");
    expect(statusMessage).toHaveLength(1);
  });

  it('shows that you win when the puzzle is solved', async () => {
    render(
      <CurrentUserContext.Provider value={{userEmail:"bobsmith@gmail.com", userName:"Bob Smith"}}>
        <SudokuBoard 
          players={[]}
          playersLockingCells={{}}
          gridState={PIECES}
          puzzleId="1"
          solved={true}
          ref={getSocket()}
        />
      </CurrentUserContext.Provider>
    );
    const winMessage = await screen.findAllByText("You win!");
    expect(winMessage).toHaveLength(1);
  });
});