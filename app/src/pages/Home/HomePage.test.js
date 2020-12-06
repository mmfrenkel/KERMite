import React from 'react';
import { render, screen, waitFor, fireEvent, within } from "@testing-library/react";
import { act } from 'react-dom/test-utils';
import HomePage from './HomePage';
import PuzzlePage from '../Puzzle/PuzzlePage';
import { FULL_PUZZLES, EMPTY_PUZZLES } from '../../data/mock_puzzles_data.js';
import {
    BrowserRouter as Router,
    Route,
} from "react-router-dom";
import { getPuzzleResponse } from '../../data/get_puzzle_response';

function setupFetchStub(mockResponse) {
    return function fetchStub(_url) {
      return Promise.resolve({
        json: () => Promise.resolve(mockResponse),
      })
    }
}

function setupUndefinedFetchStub() {
    return function fetchStub(_url) {
      return Promise.resolve({
        json: () => Promise.resolve({ }),
      })
    }
}

function setupPuzzleFetchStub() {
    return function fetchStub(_url) {
      return Promise.resolve({
        json: () => Promise.resolve(getPuzzleResponse),
      })
    }
}

test('renders start new puzzle button', async() => {
    jest.spyOn(global, "fetch").mockImplementation(setupFetchStub(EMPTY_PUZZLES));
    act(() => {
        render(<Router><HomePage /></Router>);
    });    
    const buttonMessage = await screen.findAllByText(/Start new puzzle/);
    expect(buttonMessage).toHaveLength(1);
    global.fetch.mockClear();
});

test('renders no puzzles message', async() => {
    jest.spyOn(global, "fetch").mockImplementation(setupFetchStub(EMPTY_PUZZLES));
    act(() => {
        render(<Router><HomePage /></Router>);
    });    
    const emptyMessage = await screen.findAllByText(/You do not currently have any puzzles./);
    expect(emptyMessage).toHaveLength(1);
    global.fetch.mockClear();
});

test('renders puzzle cards for user with >0 puzzles', async() => {
    jest.spyOn(global, "fetch").mockImplementation(setupFetchStub(FULL_PUZZLES));
    act(() => {
        render(<Router><HomePage /></Router>);
    });    
    const puzzleCardsContainer = screen.queryByTestId('puzzle-cards');
    expect(puzzleCardsContainer).not.toBeNull();
    await waitFor(() => expect((screen.getAllByTestId("puzzle-card")).length).toBe(3));
    global.fetch.mockClear();
});

test('renders empty page if response undefined', async() => {
    jest.spyOn(global, "fetch").mockImplementation(setupUndefinedFetchStub());
    act(() => {
        render(<Router><HomePage /></Router>);
    });
    const emptyMessage = await screen.findAllByText(/You do not currently have any puzzles./);
    expect(emptyMessage).toHaveLength(1);
    global.fetch.mockClear();
});

test('clicking delete button on puzzle opens modal', async() => {
    jest.spyOn(global, "fetch").mockImplementation(setupFetchStub(FULL_PUZZLES));
    act(() => {
        render(<Router><HomePage /></Router>);
    });
    await waitFor(() => expect((screen.getAllByTestId("puzzle-card")).length).toBe(3));
    fireEvent.click(screen.getAllByTestId('hideButton')[0]);
    const modalContent = screen.getByTestId('hide-modal');
    expect(modalContent).not.toBeNull();
    global.fetch.mockClear();
});

test('clicking yes on hide modal triggers fetch', async() => {
    const fetch = jest.spyOn(global, "fetch").mockImplementation(setupFetchStub(FULL_PUZZLES));
    act(() => {
        render(<Router><HomePage /></Router>);
    });
    await waitFor(() => expect((screen.getAllByTestId("puzzle-card")).length).toBe(3));
    expect(fetch).toHaveBeenCalledTimes(1);
    fireEvent.click(screen.getAllByTestId('hideButton')[0]);
    fireEvent.click(screen.getByTestId('yes-btn'));
    expect(fetch).toHaveBeenCalledTimes(2);
    global.fetch.mockClear();
});

test('clicking yes closes hide modal', async() => {
    jest.spyOn(global, "fetch").mockImplementation(setupFetchStub(FULL_PUZZLES));
    act(() => {
        render(<Router><HomePage /></Router>);
    });
    await waitFor(() => expect((screen.getAllByTestId("puzzle-card")).length).toBe(3));
    fireEvent.click(screen.getAllByTestId('hideButton')[0]);
    fireEvent.click(screen.getByTestId('yes-btn'));
    await waitFor(() => expect(screen.queryByTestId('hide-modal')).toBeNull());
    global.fetch.mockClear();
});

test('clicking no on hide modal does not call fetch', async() => {
    const fetch = jest.spyOn(global, "fetch").mockImplementation(setupFetchStub(FULL_PUZZLES));
    act(() => {
        render(<Router><HomePage /></Router>);
    });
    await waitFor(() => expect((screen.getAllByTestId("puzzle-card")).length).toBe(3));
    expect(fetch).toHaveBeenCalledTimes(1);
    fireEvent.click(screen.getAllByTestId('hideButton')[0]);
    fireEvent.click(screen.getByTestId('no-btn'));
    expect(fetch).toHaveBeenCalledTimes(1);
    global.fetch.mockClear();
});

test('clicking no closes hide modal', async() => {
    jest.spyOn(global, "fetch").mockImplementation(setupFetchStub(FULL_PUZZLES));
    act(() => {
        render(<Router><HomePage /></Router>);
    });
    await waitFor(() => expect((screen.getAllByTestId("puzzle-card")).length).toBe(3));
    fireEvent.click(screen.getAllByTestId('hideButton')[0]);
    fireEvent.click(screen.getByTestId('no-btn'));
    await waitFor(() => expect(screen.queryByTestId('hide-modal')).toBeNull());
    global.fetch.mockClear();
});

test('create game button opens create modal', async() => {
    jest.spyOn(global, "fetch").mockImplementation(setupFetchStub(EMPTY_PUZZLES));
    act(() => {
        render(<Router><HomePage /></Router>);
    });
    fireEvent.click(screen.getByText('Start new puzzle'));
    const modalContent = screen.getByTestId('create-modal');
    expect(modalContent).not.toBeNull();
    global.fetch.mockClear();
});

test('creating game with modal calls fetch', async() => {
    jest.spyOn(global, "fetch").mockImplementation(setupPuzzleFetchStub());
    act(() => {
        render(<Router><HomePage /></Router>);
    });    
    expect(fetch).toHaveBeenCalledTimes(1);
    fireEvent.click(screen.getByText('Start new puzzle'));
    const modalContent = within(screen.getByTestId('create-modal'));
    fireEvent.mouseDown(modalContent.getAllByRole('button')[0]);
    const listbox = within(screen.getAllByRole('listbox', {hidden: true})[0]);
    fireEvent.click(listbox.getByText(/Warmup/i));
    fireEvent.click(modalContent.getAllByTestId('create-btn')[0]);
    expect(fetch).toHaveBeenCalledTimes(2);
});

test('creating game with modal redirects', async() => {
    jest.spyOn(global, "fetch").mockImplementation(setupPuzzleFetchStub());
    act(() => {
        render(
            <Router>
                <HomePage />
                <Route path="/puzzle/:puzzleId">
                    <PuzzlePage />
                </Route>
            </Router>
        );
    });    
    act(() => fireEvent.click(screen.getByText('Start new puzzle')));
    const modalContent = within(screen.getByTestId('create-modal'));
    act(() => fireEvent.click(modalContent.getAllByTestId('create-btn')[0]));
    const puzzlePage = screen.getAllByTestId('puzzle-page');
    expect(puzzlePage.length).toBe(1);
});
