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

  it('has a white background color for undefined playerData', () => {
    const {getByRole} = render(
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
    const input = getByRole('textbox');
    expect(input).toHaveStyle(`background-color: white;`);
  });

  it('has a white background color if playerData specified with missing index', () => {
    const {getByRole} = render(
      <CurrentUserContext.Provider value={{userEmail:"bobsmith@gmail.com", userName:"Bob Smith"}}>
        <SudokuCell 
          number={7}
          prefilled={false}
          addLock={() => {}}
          removeLock={() => {}}
          x={3}
          y={3}
          playerData={{index: -1, player: {first_name: 'Chuck', last_name: 'Green', id: 2}}}
        />
      </CurrentUserContext.Provider>
    );
    const input = getByRole('textbox');
    expect(input).toHaveStyle(`background-color: white;`);
  });

  it('does not have a white background color if playerData specified', () => {
    const {getByRole} = render(
      <CurrentUserContext.Provider value={{userEmail:"bobsmith@gmail.com", userName:"Bob Smith"}}>
        <SudokuCell 
          number={7}
          prefilled={false}
          addLock={() => {}}
          removeLock={() => {}}
          x={3}
          y={3}
          playerData={{index: 1, player: {first_name: 'Chuck', last_name: 'Green', id: 2}}}
        />
      </CurrentUserContext.Provider>
    );
    const input = getByRole('textbox');
    expect(input).not.toHaveStyle(`background-color: white;`);
  });
});
