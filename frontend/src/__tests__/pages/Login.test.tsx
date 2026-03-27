import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { Provider } from 'react-redux';
import { BrowserRouter } from 'react-router-dom';
import { configureStore } from '@reduxjs/toolkit';
import { ThemeProvider } from 'styled-components';
import Login from '../../pages/Login';
import authReducer from '../../store/slices/authSlice';
import { lightTheme } from '../../styles/theme';

// Mock the API
jest.mock('../../services/api', () => ({
  authAPI: {
    login: jest.fn(),
    register: jest.fn(),
  },
}));

const createMockStore = (initialState = {}) => {
  return configureStore({
    reducer: {
      auth: authReducer,
    },
    preloadedState: {
      auth: {
        user: null,
        token: null,
        isAuthenticated: false,
        loading: false,
        error: null,
        ...initialState,
      },
    },
  });
};

const renderWithProviders = (component: React.ReactElement, store: any) => {
  return render(
    <Provider store={store}>
      <BrowserRouter>
        <ThemeProvider theme={lightTheme}>
          {component}
        </ThemeProvider>
      </BrowserRouter>
    </Provider>
  );
};

describe('Login Page', () => {
  test('renders login form', () => {
    const store = createMockStore();
    renderWithProviders(<Login />, store);

    expect(screen.getByText('Welcome Back')).toBeInTheDocument();
    expect(screen.getByLabelText('Email')).toBeInTheDocument();
    expect(screen.getByLabelText('Password')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Sign In' })).toBeInTheDocument();
  });

  test('toggles to register form', () => {
    const store = createMockStore();
    renderWithProviders(<Login />, store);

    fireEvent.click(screen.getByText('Create Account'));

    expect(screen.getByText('Create Account')).toBeInTheDocument();
    expect(screen.getByLabelText('Full Name')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Create Account' })).toBeInTheDocument();
  });

  test('shows error message when login fails', () => {
    const store = createMockStore({ error: 'Invalid credentials' });
    renderWithProviders(<Login />, store);

    expect(screen.getByText('Invalid credentials')).toBeInTheDocument();
  });

  test('redirects when already authenticated', () => {
    const store = createMockStore({ isAuthenticated: true });
    renderWithProviders(<Login />, store);

    // The component should redirect, so the login form should not be visible
    expect(screen.queryByText('Welcome Back')).not.toBeInTheDocument();
  });
});