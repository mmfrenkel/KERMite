import React from 'react';
import { render, fireEvent } from "@testing-library/react";
import {
    BrowserRouter as Router,
    Route,
} from "react-router-dom";
import LeaderboardPage from '../../pages/Leaderboard/LeaderboardPage';
import HomePage from '../../pages/Home/HomePage';
import Header from './Header';
import CurrentUserContext from '../../context/CurrentUserContext';

afterEach(() => {
    jest.clearAllMocks();
});  

test('header shows less options when not logged in', async () => {
    const { queryByTestId } = render(
        <CurrentUserContext.Provider value={{isLoggedIn:false}}>
            <Router>
                <Header />
                <Route path="/mypuzzles">
                    <HomePage />
                </Route>
                <Route path="/leaderboard-view">
                    <LeaderboardPage />
                </Route>
            </Router>
        </CurrentUserContext.Provider>);
    expect(queryByTestId("nav-item")).toBeNull();
});

test('header shows all options when logged in', async () => {
    const { getAllByTestId } = render(
        <CurrentUserContext.Provider value={{isLoggedIn:true}}>
            <Router>
                <Header />
                <Route path="/mypuzzles">
                    <HomePage />
                </Route>
                <Route path="/leaderboard-view">
                    <LeaderboardPage />
                </Route>
            </Router>
        </CurrentUserContext.Provider>);
    expect(getAllByTestId("nav-item").length).toBe(2);
});

test('clicking outside nav elems does not redirect', async () => {
    const { getAllByTestId } = render(
        <CurrentUserContext.Provider value={{isLoggedIn:true}}>
            <Router>
                <Header />
                <Route path="/mypuzzles">
                    <HomePage />
                </Route>
                <Route path="/leaderboard-view">
                    <LeaderboardPage />
                </Route>
            </Router>
        </CurrentUserContext.Provider>);
    fireEvent.click(getAllByTestId('titleLogo')[0]);
    expect(getAllByTestId("titleLogo").length).toBe(1);
});

test('clicking on my puzzles redirects to homepage', async () => {
    const { getAllByTestId } = render(
        <CurrentUserContext.Provider value={{isLoggedIn:true}}>
            <Router>
                <Header />
                <Route path="/mypuzzles">
                    <HomePage />
                </Route>
                <Route path="/leaderboard-view">
                    <LeaderboardPage />
                </Route>
            </Router>
        </CurrentUserContext.Provider>);
    fireEvent.click(getAllByTestId('nav-item')[0]);
    expect(getAllByTestId("homepage").length).toBe(1);
});

test('clicking on leaderboard redirects to leaderboard', async () => {
    const { getAllByTestId } = render(
        <CurrentUserContext.Provider value={{isLoggedIn:true}}>
            <Router>
                <Header />
                <Route path="/mypuzzles">
                    <HomePage />
                </Route>
                <Route path="/leaderboard-view">
                    <LeaderboardPage />
                </Route>
            </Router>
        </CurrentUserContext.Provider>);
    fireEvent.click(getAllByTestId('nav-item')[1]);
    expect(getAllByTestId("leaderboard").length).toBe(1);
});