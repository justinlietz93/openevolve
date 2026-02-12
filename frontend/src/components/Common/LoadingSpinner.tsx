import React from 'react';
import styled, { keyframes } from 'styled-components';

interface LoadingSpinnerProps {
  size?: 'small' | 'medium' | 'large';
  color?: string;
}

const spin = keyframes`
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
`;

const Spinner = styled.div<{ size: string; color?: string }>`
  border: 3px solid ${props => props.theme.colors.border};
  border-top: 3px solid ${props => props.color || props.theme.colors.primary};
  border-radius: 50%;
  animation: ${spin} 1s linear infinite;

  ${props => {
    switch (props.size) {
      case 'small':
        return 'width: 20px; height: 20px;';
      case 'large':
        return 'width: 48px; height: 48px;';
      default:
        return 'width: 32px; height: 32px;';
    }
  }}
`;

const Container = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  padding: ${props => props.theme.spacing.lg};
`;

const LoadingSpinner: React.FC<LoadingSpinnerProps> = ({
  size = 'medium',
  color,
}) => {
  return (
    <Container>
      <Spinner size={size} color={color} />
    </Container>
  );
};

export default LoadingSpinner;