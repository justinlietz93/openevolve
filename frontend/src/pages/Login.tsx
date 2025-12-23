import React, { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { Navigate } from 'react-router-dom';
import styled from 'styled-components';
import { AppDispatch, RootState } from '../store/store';
import { login, register, clearError } from '../store/slices/authSlice';
import Button from '../components/Common/Button';
import Input from '../components/Common/Input';
import Card from '../components/Common/Card';

const LoginContainer = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background: linear-gradient(135deg, ${props => props.theme.colors.primary}20, ${props => props.theme.colors.secondary}20);
  padding: ${props => props.theme.spacing.lg};
`;

const LoginCard = styled(Card)`
  width: 100%;
  max-width: 400px;
`;

const Title = styled.h1`
  text-align: center;
  margin-bottom: ${props => props.theme.spacing.xl};
  color: ${props => props.theme.colors.text.primary};
`;

const Form = styled.form`
  display: flex;
  flex-direction: column;
  gap: ${props => props.theme.spacing.lg};
`;

const ToggleText = styled.p`
  text-align: center;
  margin-top: ${props => props.theme.spacing.lg};
  color: ${props => props.theme.colors.text.secondary};
`;

const ToggleLink = styled.button`
  background: none;
  border: none;
  color: ${props => props.theme.colors.primary};
  cursor: pointer;
  text-decoration: underline;
  font-size: inherit;
`;

const ErrorMessage = styled.div`
  color: ${props => props.theme.colors.error};
  text-align: center;
  margin-bottom: ${props => props.theme.spacing.md};
`;

const Login: React.FC = () => {
  const dispatch = useDispatch<AppDispatch>();
  const { isAuthenticated, loading, error } = useSelector((state: RootState) => state.auth);
  
  const [isRegister, setIsRegister] = useState(false);
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    name: '',
  });

  useEffect(() => {
    dispatch(clearError());
  }, [isRegister, dispatch]);

  if (isAuthenticated) {
    return <Navigate to="/" replace />;
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    if (isRegister) {
      dispatch(register(formData));
    } else {
      dispatch(login({ email: formData.email, password: formData.password }));
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const toggleMode = () => {
    setIsRegister(!isRegister);
    setFormData({ email: '', password: '', name: '' });
  };

  return (
    <LoginContainer>
      <LoginCard>
        <Title>
          {isRegister ? 'Create Account' : 'Welcome Back'}
        </Title>
        
        {error && <ErrorMessage>{error}</ErrorMessage>}
        
        <Form onSubmit={handleSubmit}>
          {isRegister && (
            <Input
              label="Full Name"
              type="text"
              name="name"
              value={formData.name}
              onChange={handleInputChange}
              required
              fullWidth
            />
          )}
          
          <Input
            label="Email"
            type="email"
            name="email"
            value={formData.email}
            onChange={handleInputChange}
            required
            fullWidth
          />
          
          <Input
            label="Password"
            type="password"
            name="password"
            value={formData.password}
            onChange={handleInputChange}
            required
            fullWidth
          />
          
          <Button
            type="submit"
            loading={loading}
            fullWidth
            size="large"
          >
            {isRegister ? 'Create Account' : 'Sign In'}
          </Button>
        </Form>
        
        <ToggleText>
          {isRegister ? 'Already have an account?' : "Don't have an account?"}{' '}
          <ToggleLink onClick={toggleMode}>
            {isRegister ? 'Sign In' : 'Create Account'}
          </ToggleLink>
        </ToggleText>
      </LoginCard>
    </LoginContainer>
  );
};

export default Login;