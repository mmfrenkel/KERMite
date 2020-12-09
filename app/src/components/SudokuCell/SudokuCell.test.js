import React from 'react';
import { render, act, fireEvent } from "@testing-library/react";
import SudokuCell from './SudokuCell';
import CurrentUserContext from '../../context/CurrentUserContext';

describe('SudokuCell', () => {
  it('adds lock when cell is focused', async () => {
    const addLock = jest.fn();
    const {getAllByRole} = render(
      <CurrentUserContext.Provider value={{userEmail:"bobsmith@gmail.com", userName:"Bob Smith"}}>
        <SudokuCell 
          number={7}
          prefilled={false}
          addLock={addLock}
          removeLock={() => {}}
          x={7}
          y={7}
        />
      </CurrentUserContext.Provider>
    );
    const input = getAllByRole('textbox')[0];
    act(() => {
      fireEvent.focus(input);
    });
    expect(addLock).toHaveBeenCalled();
  });

  it('removes lock when cell is blurred', async () => {
    const removeLock = jest.fn();
    const {getAllByRole} = render(
      <CurrentUserContext.Provider value={{userEmail:"bobsmith@gmail.com", userName:"Bob Smith"}}>
        <SudokuCell 
          number={7}
          prefilled={false}
          addLock={() => {}}
          removeLock={removeLock}
          x={7}
          y={7}
        />
      </CurrentUserContext.Provider>
    );
    const input = getAllByRole('textbox')[0];
    act(() => {
      fireEvent.blur(input);
    });
    expect(removeLock).toHaveBeenCalled();
  });

  it('has thicker line styling on the left edge for every third column', async () => {
    const {getAllByRole} = render(
      <CurrentUserContext.Provider value={{userEmail:"bobsmith@gmail.com", userName:"Bob Smith"}}>
        <SudokuCell 
          number={7}
          prefilled={false}
          addLock={() => {}}
          removeLock={() => {}}
          x={3}
          y={7}
        />
      </CurrentUserContext.Provider>
    );
    const input = getAllByRole('textbox')[0];
    expect(input).toHaveStyle(`border-left: 3px solid black;`);
  });

  it('has thicker line styling on the top edge for every third row', async () => {
    const {getAllByRole} = render(
      <CurrentUserContext.Provider value={{userEmail:"bobsmith@gmail.com", userName:"Bob Smith"}}>
        <SudokuCell 
          number={7}
          prefilled={false}
          addLock={() => {}}
          removeLock={() => {}}
          x={3}
          y={3}
        />
      </CurrentUserContext.Provider>
    );
    const input = getAllByRole('textbox')[0];
    expect(input).toHaveStyle(`border-top: 3px solid black;`);
  });
});
