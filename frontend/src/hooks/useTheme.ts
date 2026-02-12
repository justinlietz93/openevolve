import { useSelector, useDispatch } from 'react-redux';
import { RootState } from '../store/store';
import { setTheme, toggleTheme } from '../store/slices/uiSlice';

export const useTheme = () => {
  const dispatch = useDispatch();
  const theme = useSelector((state: RootState) => state.ui.theme);

  const setCurrentTheme = (newTheme: 'light' | 'dark') => {
    dispatch(setTheme(newTheme));
  };

  const toggleCurrentTheme = () => {
    dispatch(toggleTheme());
  };

  return {
    theme,
    isDark: theme === 'dark',
    setTheme: setCurrentTheme,
    toggleTheme: toggleCurrentTheme,
  };
};