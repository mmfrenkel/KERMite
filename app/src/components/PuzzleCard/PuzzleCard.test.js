import React from 'react';
import { render, screen, fireEvent } from "@testing-library/react";
import PuzzleCard from './PuzzleCard';

afterEach(() => {
    jest.clearAllMocks();
});  

test('renders correct text according to params', async () => {
    const puzzle = {
        puzzle_id: 2, 
        completed: true, 
        difficulty: 0.5, 
        point_value: 80,
    };
    render(<PuzzleCard puzzle={puzzle}/>);
    const title = await screen.findAllByText(/Puzzle 2/);
    expect(title).toHaveLength(1);
    const completedStatus = await screen.findAllByText(/Completed/);
    expect(completedStatus).toHaveLength(1);
    const difficulty = await screen.findAllByText(/Difficulty: Intermediate/);
    expect(difficulty).toHaveLength(1);
    const points = await screen.findAllByText(/Point Value: 80/);
    expect(points).toHaveLength(1);
});

test('renders incomplete message', async () => {
    const puzzle = {
        puzzle_id: 2, 
        completed: false, 
        difficulty: 0.5, 
        point_value: 80,
    };
    render(<PuzzleCard puzzle={puzzle}/>);
    const completedStatus = await screen.findAllByText(/In Progress/);
    expect(completedStatus).toHaveLength(1);
});

test('puzzle card click calls function', async () => {
    const puzzle = {
        puzzle_id: 2, 
        completed: false, 
        difficulty: 0.5, 
        point_value: 80,
    };
    const mockFn = jest.fn();
    const {getByTestId} = render(<PuzzleCard puzzle={puzzle} onClick={mockFn}/>);
    fireEvent.click(getByTestId('puzzle-card'));
    expect(mockFn).toHaveBeenCalledTimes(1);
    mockFn.mockClear();
});

test('hide button click calls functions', async () => {
    const puzzle = {
        puzzle_id: 2, 
        completed: false, 
        difficulty: 0.5, 
        point_value: 80,
    };
    const divClick = jest.fn();
    const setHidePuzzleId = jest.fn();
    const setHideModalStatus = jest.fn();
    const {getByTestId} = render(<PuzzleCard puzzle={puzzle} onClick={divClick} setHideModalStatus={setHideModalStatus} setHidePuzzleId={setHidePuzzleId}/>);
    fireEvent.click(getByTestId('hideButton'));
    expect(setHidePuzzleId).toHaveBeenCalledTimes(1);
    expect(setHideModalStatus).toHaveBeenCalledTimes(1);
    expect(divClick).toHaveBeenCalledTimes(0);
});