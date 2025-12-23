import { configureStore } from '@reduxjs/toolkit';
import authReducer from './slices/authSlice';
import evolutionReducer from './slices/evolutionSlice';
import programsReducer from './slices/programsSlice';
import uiReducer from './slices/uiSlice';

export const store = configureStore({
  reducer: {
    auth: authReducer,
    evolution: evolutionReducer,
    programs: programsReducer,
    ui: uiReducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: {
        ignoredActions: ['persist/PERSIST'],
      },
    }),
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;