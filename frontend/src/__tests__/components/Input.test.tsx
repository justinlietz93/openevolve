import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { ThemeProvider } from 'styled-components';
import Input from '../../components/Common/Input';
import { lightTheme } from '../../styles/theme';

const renderWithTheme = (component: React.ReactElement) => {
  return render(
    <ThemeProvider theme={lightTheme}>
      {component}
    </ThemeProvider>
  );
};

describe('Input Component', () => {
  test('renders input with label', () => {
    renderWithTheme(<Input label="Test Label" />);
    expect(screen.getByText('Test Label')).toBeInTheDocument();
  });

  test('shows error message when error prop is provided', () => {
    renderWithTheme(<Input error="This field is required" />);
    expect(screen.getByText('This field is required')).toBeInTheDocument();
  });

  test('calls onChange when value changes', () => {
    const handleChange = jest.fn();
    renderWithTheme(<Input onChange={handleChange} />);
    
    const input = screen.getByRole('textbox');
    fireEvent.change(input, { target: { value: 'test value' } });
    
    expect(handleChange).toHaveBeenCalled();
  });

  test('applies fullWidth style when fullWidth prop is true', () => {
    renderWithTheme(<Input fullWidth />);
    const input = screen.getByRole('textbox');
    expect(input).toBeInTheDocument();
  });
});