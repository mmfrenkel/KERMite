import React from 'react';
import { render, screen } from "@testing-library/react";
import Chat from './Chat';
import CurrentUserContext from '../../context/CurrentUserContext';

test('renders list of messages', async () => {
    const message = {userName: "janedoe", messageString:"hello", userEmail:"janedoe@gmail.com"}
    const messages = [message, message, message, message, message, message, message, message, message, message]
    render(
        <CurrentUserContext.Provider value={{userEmail:"bobsmith@gmail.com", userName:"Bob Smith"}}>
            <Chat messages={messages}/>
        </CurrentUserContext.Provider>
    );
    expect(screen.queryAllByTestId("chat-message").length).toBe(10);
});