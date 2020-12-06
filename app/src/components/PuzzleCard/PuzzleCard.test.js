import React from 'react';
import { render, screen } from "@testing-library/react";
import PuzzleCard from './PuzzleCard';

test('renders correct text according to params', async () => {
    const puzzle = {
        puzzle_id: 2, 
        completed: true, 
        difficulty: 0.5, 
        point_value: 80,
    };
    render(<PuzzleCard accessToken="mockToken"
        puzzle={puzzle}
    />);
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
    render(<PuzzleCard accessToken="mockToken"
        puzzle={puzzle}
    />);
    const completedStatus = await screen.findAllByText(/In Progress/);
    expect(completedStatus).toHaveLength(1);
});