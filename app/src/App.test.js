import { render, within } from '@testing-library/react';
import App from './App';
import React from 'react';

// Renders login page if not logged in
test('App renders a <LoginPage />', () => {
  const { getByTestId } = render(<App />);
  const app = getByTestId('app')
  const loginPageImg = within(app).getAllByTestId('login-page')
  expect(loginPageImg.length).toBe(1);
});