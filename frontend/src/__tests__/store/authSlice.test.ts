import { configureStore } from '@reduxjs/toolkit';
import authReducer, { login, logout, clearError } from '../../store/slices/authSlice';

// Mock the API
jest.mock('../../services/api', () => ({
  authAPI: {
    login: jest.fn(),
    register: jest.fn(),
    verifyToken: jest.fn(),
  },
}));

describe('authSlice', () => {
  let store: any;

  beforeEach(() => {
    store = configureStore({
      reducer: {
        auth: authReducer,
      },
    });
  });

  test('should handle initial state', () => {
    const state = store.getState().auth;
    expect(state.user).toBeNull();
    expect(state.isAuthenticated).toBe(false);
    expect(state.loading).toBe(false);
    expect(state.error).toBeNull();
  });

  test('should handle logout', () => {
    store.dispatch(logout());
    const state = store.getState().auth;
    
    expect(state.user).toBeNull();
    expect(state.token).toBeNull();
    expect(state.isAuthenticated).toBe(false);
  });

  test('should handle clearError', () => {
    // First set an error state
    store.dispatch({ type: 'auth/login/rejected', payload: 'Test error' });
    expect(store.getState().auth.error).toBe('Test error');
    
    // Then clear it
    store.dispatch(clearError());
    expect(store.getState().auth.error).toBeNull();
  });
});