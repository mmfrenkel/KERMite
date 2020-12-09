import React from 'react';
import renderer from 'react-test-renderer';
import socketIOClient from 'socket.io-client';
import { render, act, screen, fireEvent, getByTestId, getAllByTestId } from "@testing-library/react";
import PuzzlePage from './PuzzlePage.js';
import CurrentUserContext from '../../context/CurrentUserContext';
import MockedSocket from 'socket.io-mock';
import {getMultiplayerPuzzleResponse} from '../../data/get_puzzle_response';

jest.mock("socket.io-client");
jest.mock('react-router-dom', () => ({
  ...jest.requireActual('react-router-dom'),
  useParams: () => ({
    puzzleId: '1',
  }),
  useRouteMatch: () => ({ url: '/puzzle' }),
}));

describe('PuzzlePage', () => {
  let socket;
  let fetchSpy;

  beforeEach(() => {
    fetchSpy = jest.spyOn(global, 'fetch');
    fetchSpy.mockImplementation(() => Promise.resolve(getMultiplayerPuzzleResponse()));
    socket = new MockedSocket();
    socketIOClient.mockReturnValue(socket);
  });
  
  afterEach(() => {
    jest.restoreAllMocks();
  });

  it('shows the chat in multiplayer mode', async () => {
    let component;
    
    await act(async () => {
      component = render(
        <CurrentUserContext.Provider value={{userEmail:"bobsmith@gmail.com", userName:"Bob Smith"}}>
          <PuzzlePage />
        </CurrentUserContext.Provider>
      );
    });
    const chatSection = component.getAllByTestId('chat-section');
    expect(chatSection).toHaveLength(1);
  });
});