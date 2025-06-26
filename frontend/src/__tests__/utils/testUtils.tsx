import React from 'react';
import { render } from '@testing-library/react';
import { Provider } from 'react-redux';
import { BrowserRouter } from 'react-router-dom';
import { ThemeProvider } from 'styled-components';
import { configureStore } from '@reduxjs/toolkit';
import authReducer from '../../store/slices/authSlice';
import evolutionReducer from '../../store/slices/evolutionSlice';
import programsReducer from '../../store/slices/programsSlice';
import uiReducer from '../../store/slices/uiSlice';
import { lightTheme } from '../../styles/theme';

export const createMockStore = (initialState = {}) => {
  return configureStore({
    reducer: {
      auth: authReducer,
      evolution: evolutionReducer,
      programs: programsReducer,
      ui: uiReducer,
    },
    preloadedState: initialState,
  });
};

export const renderWithProviders = (
  component: React.ReactElement,
  {
    store = createMockStore(),
    theme = lightTheme,
    ...renderOptions
  } = {}
) => {
  const Wrapper = ({ children }: { children: React.ReactNode }) => (
    <Provider store={store}>
      <BrowserRouter>
        <ThemeProvider theme={theme}>
          {children}
        </ThemeProvider>
      </BrowserRouter>
    </Provider>
  );

  return render(component, { wrapper: Wrapper, ...renderOptions });
};

export * from '@testing-library/react';