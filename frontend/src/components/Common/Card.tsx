import React from 'react';
import styled from 'styled-components';

interface CardProps {
  children: React.ReactNode;
  padding?: 'small' | 'medium' | 'large';
  hover?: boolean;
  className?: string;
}

const StyledCard = styled.div<{ padding: string; hover: boolean }>`
  background-color: ${props => props.theme.colors.surface};
  border-radius: ${props => props.theme.borderRadius};
  box-shadow: ${props => props.theme.shadows.small};
  border: 1px solid ${props => props.theme.colors.border};
  transition: all 0.2s ease;

  ${props => {
    switch (props.padding) {
      case 'small':
        return `padding: ${props.theme.spacing.md};`;
      case 'large':
        return `padding: ${props.theme.spacing.xl};`;
      default:
        return `padding: ${props.theme.spacing.lg};`;
    }
  }}

  ${props => props.hover && `
    &:hover {
      box-shadow: ${props.theme.shadows.medium};
      transform: translateY(-2px);
    }
  `}
`;

const Card: React.FC<CardProps> = ({
  children,
  padding = 'medium',
  hover = false,
  className,
}) => {
  return (
    <StyledCard padding={padding} hover={hover} className={className}>
      {children}
    </StyledCard>
  );
};

export default Card;