import React from 'react';
import styled, { css } from 'styled-components';

interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'outline' | 'danger';
  size?: 'small' | 'medium' | 'large';
  disabled?: boolean;
  loading?: boolean;
  fullWidth?: boolean;
  children: React.ReactNode;
  onClick?: () => void;
  type?: 'button' | 'submit' | 'reset';
}

const getVariantStyles = (variant: string, theme: any) => {
  switch (variant) {
    case 'primary':
      return css`
        background-color: ${theme.colors.primary};
        color: white;
        border: 1px solid ${theme.colors.primary};

        &:hover:not(:disabled) {
          background-color: ${theme.colors.primary}dd;
        }
      `;
    case 'secondary':
      return css`
        background-color: ${theme.colors.secondary};
        color: white;
        border: 1px solid ${theme.colors.secondary};

        &:hover:not(:disabled) {
          background-color: ${theme.colors.secondary}dd;
        }
      `;
    case 'outline':
      return css`
        background-color: transparent;
        color: ${theme.colors.primary};
        border: 1px solid ${theme.colors.primary};

        &:hover:not(:disabled) {
          background-color: ${theme.colors.primary};
          color: white;
        }
      `;
    case 'danger':
      return css`
        background-color: ${theme.colors.error};
        color: white;
        border: 1px solid ${theme.colors.error};

        &:hover:not(:disabled) {
          background-color: ${theme.colors.error}dd;
        }
      `;
    default:
      return css`
        background-color: ${theme.colors.surface};
        color: ${theme.colors.text.primary};
        border: 1px solid ${theme.colors.border};

        &:hover:not(:disabled) {
          background-color: ${theme.colors.border};
        }
      `;
  }
};

const getSizeStyles = (size: string, theme: any) => {
  switch (size) {
    case 'small':
      return css`
        padding: ${theme.spacing.sm} ${theme.spacing.md};
        font-size: 0.875rem;
      `;
    case 'large':
      return css`
        padding: ${theme.spacing.lg} ${theme.spacing.xl};
        font-size: 1.125rem;
      `;
    default:
      return css`
        padding: ${theme.spacing.md} ${theme.spacing.lg};
        font-size: 1rem;
      `;
  }
};

const StyledButton = styled.button<ButtonProps>`
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: ${props => props.theme.spacing.sm};
  border-radius: ${props => props.theme.borderRadius};
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  text-decoration: none;
  white-space: nowrap;
  
  ${props => getVariantStyles(props.variant || 'primary', props.theme)}
  ${props => getSizeStyles(props.size || 'medium', props.theme)}
  
  ${props => props.fullWidth && css`
    width: 100%;
  `}
  
  &:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }
  
  &:focus {
    outline: 2px solid ${props => props.theme.colors.primary};
    outline-offset: 2px;
  }
`;

const Spinner = styled.div`
  width: 16px;
  height: 16px;
  border: 2px solid transparent;
  border-top: 2px solid currentColor;
  border-radius: 50%;
  animation: spin 1s linear infinite;

  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
`;

const Button: React.FC<ButtonProps> = ({
  children,
  loading = false,
  disabled = false,
  type = 'button',
  ...props
}) => {
  return (
    <StyledButton
      {...props}
      type={type}
      disabled={disabled || loading}
    >
      {loading && <Spinner />}
      {children}
    </StyledButton>
  );
};

export default Button;