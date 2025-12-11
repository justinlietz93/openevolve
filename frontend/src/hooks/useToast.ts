import { useDispatch } from 'react-redux';
import { addToast } from '../store/slices/uiSlice';

export const useToast = () => {
  const dispatch = useDispatch();

  const showToast = (message: string, type: 'success' | 'error' | 'warning' | 'info' = 'info', duration?: number) => {
    dispatch(addToast({ message, type, duration }));
  };

  const showSuccess = (message: string, duration?: number) => {
    showToast(message, 'success', duration);
  };

  const showError = (message: string, duration?: number) => {
    showToast(message, 'error', duration);
  };

  const showWarning = (message: string, duration?: number) => {
    showToast(message, 'warning', duration);
  };

  const showInfo = (message: string, duration?: number) => {
    showToast(message, 'info', duration);
  };

  return {
    showToast,
    showSuccess,
    showError,
    showWarning,
    showInfo,
  };
};