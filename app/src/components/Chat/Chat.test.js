import React from 'react';
import { render, screen, fireEvent } from "@testing-library/react";
import Chat from './Chat';
import CurrentUserContext from '../../context/CurrentUserContext';

test('renders list of messages', async () => {
    const message = {userName: "janedoe", messageString:"hello", userEmail:"janedoe@gmail.com"};
    const messages = [message, message, message, message, message, message, message, message, message, message];
    render(
        <CurrentUserContext.Provider value={{userEmail:"bobsmith@gmail.com", userName:"Bob Smith"}}>
            <Chat messages={messages}/>
        </CurrentUserContext.Provider>
    );
    expect(screen.queryAllByTestId("chat-message").length).toBe(10);
});

test('renders one message', async () => {
    const message = {userName: "janedoe", messageString:"hello", userEmail:"janedoe@gmail.com"};
    const messages = [message];
    render(
        <CurrentUserContext.Provider value={{userEmail:"bobsmith@gmail.com", userName:"Bob Smith"}}>
            <Chat messages={messages}/>
        </CurrentUserContext.Provider>
    );
    expect(screen.queryAllByTestId("chat-message").length).toBe(1);
});


test('renders no messages', async () => {
    const messages = []
    render(
        <CurrentUserContext.Provider value={{userEmail:"bobsmith@gmail.com", userName:"Bob Smith"}}>
            <Chat messages={messages}/>
        </CurrentUserContext.Provider>
    );
    expect(screen.queryAllByTestId("chat-message").length).toBe(0);
});

test('emits socket event when nonempty message entered', async () => {
    const messages = [];
    const emit = jest.fn();
    const socket = {
        current: {
            emit: emit,
        }
    };
    const {getAllByRole} = render(
        <CurrentUserContext.Provider value={{userEmail:"bobsmith@gmail.com", userName:"Bob Smith"}}>
            <Chat messages={messages} ref={socket} />
        </CurrentUserContext.Provider>
    );
    const inputBox = getAllByRole('textbox')[0];
    fireEvent.change(inputBox, { target: { value: 'hello' } });
    fireEvent.keyDown(inputBox, { key: "Enter", code: 13, charCode: 13 }); 
    expect(emit).toHaveBeenCalledTimes(1);
});

test('does not emit socket event when empty message entered', async () => {
    const messages = [];
    const emit = jest.fn();
    const socket = {
        current: {
            emit: emit,
        }
    };
    const {getAllByRole} = render(
        <CurrentUserContext.Provider value={{userEmail:"bobsmith@gmail.com", userName:"Bob Smith"}}>
            <Chat messages={messages} ref={socket} />
        </CurrentUserContext.Provider>
    );
    const inputBox = getAllByRole('textbox')[0];
    fireEvent.change(inputBox, { target: { value: '' } });
    fireEvent.keyDown(inputBox, { key: "Enter", code: 13, charCode: 13 }); 
    expect(emit).toHaveBeenCalledTimes(0);
});

test('does not emit socket event if key pressed is not enter', async () => {
    const messages = [];
    const emit = jest.fn();
    const socket = {
        current: {
            emit: emit,
        }
    };
    const {getAllByRole} = render(
        <CurrentUserContext.Provider value={{userEmail:"bobsmith@gmail.com", userName:"Bob Smith"}}>
            <Chat messages={messages} ref={socket} />
        </CurrentUserContext.Provider>
    );
    const inputBox = getAllByRole('textbox')[0];
    fireEvent.change(inputBox, { target: { value: '' } });
    fireEvent.keyDown(inputBox, { key: "Space", code: 13, charCode: 13 }); 
    expect(emit).toHaveBeenCalledTimes(0);
});