import React from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import styled from 'styled-components';
import { RootState } from '../../store/store';
import { logout } from '../../store/slices/authSlice';
import { toggleTheme, toggleSidebar } from '../../store/slices/uiSlice';
import Button from '../Common/Button';

const HeaderContainer = styled.header`
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: ${props => props.theme.spacing.md} ${props => props.theme.spacing.lg};
  background-color: ${props => props.theme.colors.surface};
  border-bottom: 1px solid ${props => props.theme.colors.border};
  box-shadow: ${props => props.theme.shadows.small};
  position: sticky;
  top: 0;
  z-index: 100;
`;

const LeftSection = styled.div`
  display: flex;
  align-items: center;
  gap: ${props => props.theme.spacing.md};
`;

const Logo = styled.h1`
  font-size: 1.5rem;
  font-weight: bold;
  color: ${props => props.theme.colors.primary};
  margin: 0;
`;

const MenuButton = styled.button`
  display: none;
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: ${props => props.theme.colors.text.primary};

  @media (max-width: ${props => props.theme.breakpoints.mobile}) {
    display: block;
  }
`;

const RightSection = styled.div`
  display: flex;
  align-items: center;
  gap: ${props => props.theme.spacing.md};
`;

const UserInfo = styled.div`
  display: flex;
  align-items: center;
  gap: ${props => props.theme.spacing.sm};
  color: ${props => props.theme.colors.text.secondary};

  @media (max-width: ${props => props.theme.breakpoints.mobile}) {
    display: none;
  }
`;

const ThemeToggle = styled.button`
  background: none;
  border: none;
  font-size: 1.2rem;
  cursor: pointer;
  padding: ${props => props.theme.spacing.sm};
  border-radius: ${props => props.theme.borderRadius};
  transition: background-color 0.2s;

  &:hover {
    background-color: ${props => props.theme.colors.border};
  }
`;

const Header: React.FC = () => {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const { user, isAuthenticated } = useSelector((state: RootState) => state.auth);
  const { theme } = useSelector((state: RootState) => state.ui);

  const handleLogout = () => {
    dispatch(logout());
    navigate('/login');
  };

  const handleToggleTheme = () => {
    dispatch(toggleTheme());
  };

  const handleToggleSidebar = () => {
    dispatch(toggleSidebar());
  };

  if (!isAuthenticated) {
    return null;
  }

  return (
    <HeaderContainer>
      <LeftSection>
        <MenuButton onClick={handleToggleSidebar}>
          ☰
        </MenuButton>
        <Logo>OpenEvolve</Logo>
      </LeftSection>
      
      <RightSection>
        <UserInfo>
          Welcome, {user?.name || user?.email}
        </UserInfo>
        
        <ThemeToggle onClick={handleToggleTheme}>
          {theme === 'light' ? '🌙' : '☀️'}
        </ThemeToggle>
        
        <Button variant="outline" size="small" onClick={handleLogout}>
          Logout
        </Button>
      </RightSection>
    </HeaderContainer>
  );
};

export default Header;