import React from 'react';
import { render, act, screen, fireEvent } from "@testing-library/react";
import SudokuBoard from './SudokuBoard';
import CurrentUserContext from '../../context/CurrentUserContext';
import {PIECES} from '../../data/get_puzzle_response'

function getSocket({emitFn = jest.fn()} = {}) {
  return {
    current: {emit: emitFn},
  };
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

  it.skip('emits add_lock event when nonempty number is entered', () => {
    const emit = jest.fn();
    const socket = getSocket({emitFn: emit});
    const {getAllByRole} = render(
      <CurrentUserContext.Provider value={{userEmail:"bobsmith@gmail.com", userName:"Bob Smith"}}>
        <SudokuBoard 
          players={[]}
          playersLockingCells={{}}
          gridState={PIECES}
          puzzleId={'1'}
          solved={false}
          ref={socket}
        />
      </CurrentUserContext.Provider>
    );
    const inputBox = getAllByRole('textbox')[0];
    act(() => {
      fireEvent.change(inputBox, { target: { value: 7 } });
    });
    expect(emit).toHaveBeenCalledWith('add_lock', expect.any(Function));
  });
})