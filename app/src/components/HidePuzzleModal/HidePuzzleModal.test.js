import React from 'react';
import { render, fireEvent } from "@testing-library/react";
import HidePuzzleModal from './HidePuzzleModal';

afterEach(() => {
    jest.clearAllMocks();
});  

test('clicking yes calls hidePuzzle', async () => {
    const hidePuzzle = jest.fn();
    const setHideModalStatus = jest.fn();
    const {getByTestId} = render(<HidePuzzleModal setHideModalStatus={setHideModalStatus} hidePuzzle={hidePuzzle} />);
    fireEvent.click(getByTestId('yes-btn'));
    expect(hidePuzzle).toHaveBeenCalledTimes(1);
    expect(setHideModalStatus).toHaveBeenCalledTimes(0);
});

test('clicking no calls setModalOpenStatus', async () => {
    const hidePuzzle = jest.fn();
    const setHideModalStatus = jest.fn();
    const {getByTestId} = render(<HidePuzzleModal setHideModalStatus={setHideModalStatus} hidePuzzle={hidePuzzle} />);
    fireEvent.click(getByTestId('no-btn'));
    expect(hidePuzzle).toHaveBeenCalledTimes(0);
    expect(setHideModalStatus).toHaveBeenCalledTimes(1);
});