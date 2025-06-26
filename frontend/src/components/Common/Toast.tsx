import React, { useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import styled, { keyframes } from 'styled-components';
import { RootState } from '../../store/store';
import { removeToast } from '../../store/slices/uiSlice';

const slideIn = keyframes`
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
`;

const slideOut = keyframes`
  from {
    transform: translateX(0);
    opacity: 1;
  }
  to {
    transform: translateX(100%);
    opacity: 0;
  }
`;

const ToastContainer = styled.div`
  position: fixed;
  top: 80px;
  right: 20px;
  z-index: 1000;
  display: flex;
  flex-direction: column;
  gap: ${props => props.theme.spacing.sm};
  max-width: 400px;

  @media (max-width: ${props => props.theme.breakpoints.mobile}) {
    right: 10px;
    left: 10px;
    max-width: none;
  }
`;

const ToastItem = styled.div<{ type: string }>`
  padding: ${props => props.theme.spacing.md};
  border-radius: ${props => props.theme.borderRadius};
  box-shadow: ${props => props.theme.shadows.medium};
  animation: ${slideIn} 0.3s ease-out;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: ${props => props.theme.spacing.md};

  ${props => {
    switch (props.type) {
      case 'success':
        return `
          background-color: ${props.theme.colors.success};
          color: white;
        `;
      case 'error':
        return `
          background-color: ${props.theme.colors.error};
          color: white;
        `;
      case 'warning':
        return `
          background-color: ${props.theme.colors.warning};
          color: white;
        `;
      default:
        return `
          background-color: ${props.theme.colors.primary};
          color: white;
        `;
    }
  }}
`;

const ToastMessage = styled.span`
  flex: 1;
  font-weight: 500;
`;

const CloseButton = styled.button`
  background: none;
  border: none;
  color: inherit;
  cursor: pointer;
  font-size: 1.2rem;
  padding: 0;
  opacity: 0.8;
  transition: opacity 0.2s;

  &:hover {
    opacity: 1;
  }
`;

const getToastIcon = (type: string) => {
  switch (type) {
    case 'success':
      return '✓';
    case 'error':
      return '✕';
    case 'warning':
      return '⚠';
    default:
      return 'ℹ';
  }
};

const Toast: React.FC = () => {
  const dispatch = useDispatch();
  const toasts = useSelector((state: RootState) => state.ui.toasts);

  useEffect(() => {
    toasts.forEach(toast => {
      if (toast.duration) {
        const timer = setTimeout(() => {
          dispatch(removeToast(toast.id));
        }, toast.duration);

        return () => clearTimeout(timer);
      }
    });
  }, [toasts, dispatch]);

  const handleClose = (id: string) => {
    dispatch(removeToast(id));
  };

  if (toasts.length === 0) {
    return null;
  }

  return (
    <ToastContainer>
      {toasts.map(toast => (
        <ToastItem key={toast.id} type={toast.type}>
          <span>{getToastIcon(toast.type)}</span>
          <ToastMessage>{toast.message}</ToastMessage>
          <CloseButton onClick={() => handleClose(toast.id)}>
            ×
          </CloseButton>
        </ToastItem>
      ))}
    </ToastContainer>
  );
};

export default Toast;