import React from 'react';
import { render, screen } from "@testing-library/react";
import ChatMessage from './ChatMessage';
import CurrentUserContext from '../../context/CurrentUserContext';

test('renders username when not user message', async () => {
    const message = {userName: "janedoe", messageString:"hello", userEmail:"janedoe@gmail.com"}
    render(
        <CurrentUserContext.Provider value={{userEmail:"bobsmith@gmail.com"}}>
            <ChatMessage message={message}/>
        </CurrentUserContext.Provider>
    );
    expect(screen.queryAllByText("janedoe").length).toBe(1);
});

test('does not render username when user message', async () => {
    const message = {userName: "janedoe", messageString:"hello", userEmail:"janedoe@gmail.com"}
    render(
        <CurrentUserContext.Provider value={{userEmail:"janedoe@gmail.com"}}>
            <ChatMessage message={message}/>
        </CurrentUserContext.Provider>
    );
    expect(screen.queryAllByText("janedoe").length).toBe(0);
});