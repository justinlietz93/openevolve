import React, { Component, ErrorInfo, ReactNode } from 'react';
import styled from 'styled-components';
import Button from './Button';

interface Props {
  children: ReactNode;
}

interface State {
  hasError: boolean;
  error?: Error;
}

const ErrorContainer = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 400px;
  padding: 2rem;
  text-align: center;
`;

const ErrorTitle = styled.h2`
  color: ${props => props.theme?.colors?.error || '#f44336'};
  margin-bottom: 1rem;
`;

const ErrorMessage = styled.p`
  color: ${props => props.theme?.colors?.text?.secondary || '#666'};
  margin-bottom: 2rem;
  max-width: 600px;
`;

const ErrorDetails = styled.details`
  margin-top: 1rem;
  padding: 1rem;
  background-color: ${props => props.theme?.colors?.surface || '#f5f5f5'};
  border-radius: 8px;
  max-width: 800px;
  
  summary {
    cursor: pointer;
    font-weight: bold;
    margin-bottom: 0.5rem;
  }
  
  pre {
    white-space: pre-wrap;
    font-size: 0.875rem;
    color: ${props => props.theme?.colors?.text?.secondary || '#666'};
  }
`;

class ErrorBoundary extends Component<Props, State> {
  public state: State = {
    hasError: false,
  };

  public static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('Uncaught error:', error, errorInfo);
  }

  private handleReload = () => {
    window.location.reload();
  };

  private handleReset = () => {
    this.setState({ hasError: false, error: undefined });
  };

  public render() {
    if (this.state.hasError) {
      return (
        <ErrorContainer>
          <ErrorTitle>Oops! Something went wrong</ErrorTitle>
          <ErrorMessage>
            We're sorry, but something unexpected happened. Please try refreshing the page or contact support if the problem persists.
          </ErrorMessage>
          
          <div style={{ display: 'flex', gap: '1rem' }}>
            <Button onClick={this.handleReload} variant="primary">
              Refresh Page
            </Button>
            <Button onClick={this.handleReset} variant="outline">
              Try Again
            </Button>
          </div>

          {this.state.error && (
            <ErrorDetails>
              <summary>Technical Details</summary>
              <pre>{this.state.error.stack}</pre>
            </ErrorDetails>
          )}
        </ErrorContainer>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;