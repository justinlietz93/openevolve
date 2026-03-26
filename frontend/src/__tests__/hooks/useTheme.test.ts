import { renderHook, act } from '@testing-library/react';
import { Provider } from 'react-redux';
import { configureStore } from '@reduxjs/toolkit';
import { useTheme } from '../../hooks/useTheme';
import uiReducer from '../../store/slices/uiSlice';

const createMockStore = (initialState = {}) => {
  return configureStore({
    reducer: {
      ui: uiReducer,
    },
    preloadedState: {
      ui: {
        theme: 'light',
        sidebarCollapsed: false,
        toasts: [],
        loading: { global: false },
        ...initialState,
      },
    },
  });
};

const wrapper = ({ children, store }: any) => (
  <Provider store={store}>{children}</Provider>
);

describe('useTheme hook', () => {
  test('should return current theme', () => {
    const store = createMockStore();
    const { result } = renderHook(() => useTheme(), {
      wrapper: ({ children }) => wrapper({ children, store }),
    });

    expect(result.current.theme).toBe('light');
    expect(result.current.isDark).toBe(false);
  });

  test('should toggle theme', () => {
    const store = createMockStore();
    const { result } = renderHook(() => useTheme(), {
      wrapper: ({ children }) => wrapper({ children, store }),
    });

    act(() => {
      result.current.toggleTheme();
    });

    expect(result.current.theme).toBe('dark');
    expect(result.current.isDark).toBe(true);
  });

  test('should set specific theme', () => {
    const store = createMockStore();
    const { result } = renderHook(() => useTheme(), {
      wrapper: ({ children }) => wrapper({ children, store }),
    });

    act(() => {
      result.current.setTheme('dark');
    });

    expect(result.current.theme).toBe('dark');
    expect(result.current.isDark).toBe(true);
  });
});