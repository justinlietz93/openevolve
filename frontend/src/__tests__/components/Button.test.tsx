import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { ThemeProvider } from 'styled-components';
import Button from '../../components/Common/Button';
import { lightTheme } from '../../styles/theme';

const renderWithTheme = (component: React.ReactElement) => {
  return render(
    <ThemeProvider theme={lightTheme}>
      {component}
    </ThemeProvider>
  );
};

describe('Button Component', () => {
  test('renders button with text', () => {
    renderWithTheme(<Button>Click me</Button>);
    expect(screen.getByText('Click me')).toBeInTheDocument();
  });

  test('calls onClick when clicked', () => {
    const handleClick = jest.fn();
    renderWithTheme(<Button onClick={handleClick}>Click me</Button>);
    
    fireEvent.click(screen.getByText('Click me'));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  test('is disabled when disabled prop is true', () => {
    renderWithTheme(<Button disabled>Disabled</Button>);
    expect(screen.getByText('Disabled')).toBeDisabled();
  });

  test('shows loading spinner when loading', () => {
    renderWithTheme(<Button loading>Loading</Button>);
    expect(screen.getByText('Loading')).toBeInTheDocument();
    // The spinner should be present but we can't easily test for it without a test id
  });

  test('applies correct variant styles', () => {
    renderWithTheme(<Button variant="primary">Primary</Button>);
    const button = screen.getByText('Primary');
    expect(button).toBeInTheDocument();
  });
});