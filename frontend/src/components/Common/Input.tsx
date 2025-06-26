import React, { forwardRef } from 'react';
import styled, { css } from 'styled-components';

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  fullWidth?: boolean;
  variant?: 'outlined' | 'filled';
}

const InputContainer = styled.div<{ fullWidth?: boolean }>`
  display: flex;
  flex-direction: column;
  gap: ${props => props.theme.spacing.sm};
  width: ${props => props.fullWidth ? '100%' : 'auto'};
`;

const Label = styled.label`
  font-weight: 500;
  color: ${props => props.theme.colors.text.primary};
  font-size: 0.875rem;
`;

const StyledInput = styled.input<{ hasError?: boolean; variant?: string }>`
  padding: ${props => props.theme.spacing.md};
  border-radius: ${props => props.theme.borderRadius};
  font-size: 1rem;
  transition: all 0.2s ease;
  width: 100%;

  ${props => props.variant === 'filled' ? css`
    background-color: ${props.theme.colors.border};
    border: 1px solid transparent;
    
    &:focus {
      background-color: ${props.theme.colors.surface};
      border-color: ${props.theme.colors.primary};
    }
  ` : css`
    background-color: ${props.theme.colors.surface};
    border: 1px solid ${props.theme.colors.border};
    
    &:focus {
      border-color: ${props.theme.colors.primary};
      box-shadow: 0 0 0 2px ${props.theme.colors.primary}20;
    }
  `}

  ${props => props.hasError && css`
    border-color: ${props.theme.colors.error};
    
    &:focus {
      border-color: ${props.theme.colors.error};
      box-shadow: 0 0 0 2px ${props.theme.colors.error}20;
    }
  `}

  &:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }

  &::placeholder {
    color: ${props => props.theme.colors.text.secondary};
  }
`;

const ErrorText = styled.span`
  color: ${props => props.theme.colors.error};
  font-size: 0.875rem;
`;

const Input = forwardRef<HTMLInputElement, InputProps>(({
  label,
  error,
  fullWidth = false,
  variant = 'outlined',
  ...props
}, ref) => {
  return (
    <InputContainer fullWidth={fullWidth}>
      {label && <Label>{label}</Label>}
      <StyledInput
        ref={ref}
        hasError={!!error}
        variant={variant}
        {...props}
      />
      {error && <ErrorText>{error}</ErrorText>}
    </InputContainer>
  );
});

Input.displayName = 'Input';

export default Input;