import React from 'react';
import { useSelector } from 'react-redux';
import { NavLink, useLocation } from 'react-router-dom';
import styled from 'styled-components';
import { RootState } from '../../store/store';

const SidebarContainer = styled.aside<{ collapsed: boolean }>`
  width: ${props => props.collapsed ? '60px' : '250px'};
  background-color: ${props => props.theme.colors.surface};
  border-right: 1px solid ${props => props.theme.colors.border};
  transition: width 0.3s ease;
  overflow: hidden;
  
  @media (max-width: ${props => props.theme.breakpoints.mobile}) {
    position: fixed;
    left: ${props => props.collapsed ? '-250px' : '0'};
    top: 70px;
    height: calc(100vh - 70px);
    z-index: 50;
    width: 250px;
  }
`;

const NavList = styled.nav`
  padding: ${props => props.theme.spacing.md} 0;
`;

const NavItem = styled(NavLink)<{ collapsed: boolean }>`
  display: flex;
  align-items: center;
  padding: ${props => props.theme.spacing.md} ${props => props.theme.spacing.lg};
  color: ${props => props.theme.colors.text.secondary};
  text-decoration: none;
  transition: all 0.2s;
  white-space: nowrap;

  &:hover {
    background-color: ${props => props.theme.colors.border};
    color: ${props => props.theme.colors.text.primary};
  }

  &.active {
    background-color: ${props => props.theme.colors.primary};
    color: white;
  }

  .icon {
    font-size: 1.2rem;
    margin-right: ${props => props.collapsed ? '0' : props.theme.spacing.md};
    min-width: 20px;
  }

  .label {
    opacity: ${props => props.collapsed ? '0' : '1'};
    transition: opacity 0.3s ease;
  }
`;

const Sidebar: React.FC = () => {
  const { isAuthenticated } = useSelector((state: RootState) => state.auth);
  const { sidebarCollapsed } = useSelector((state: RootState) => state.ui);
  const location = useLocation();

  if (!isAuthenticated) {
    return null;
  }

  const navItems = [
    { path: '/', icon: '📊', label: 'Dashboard' },
    { path: '/evolution', icon: '🧬', label: 'Evolution' },
    { path: '/programs', icon: '📝', label: 'Programs' },
    { path: '/settings', icon: '⚙️', label: 'Settings' },
  ];

  return (
    <SidebarContainer collapsed={sidebarCollapsed}>
      <NavList>
        {navItems.map((item) => (
          <NavItem
            key={item.path}
            to={item.path}
            collapsed={sidebarCollapsed}
            className={location.pathname === item.path ? 'active' : ''}
          >
            <span className="icon">{item.icon}</span>
            <span className="label">{item.label}</span>
          </NavItem>
        ))}
      </NavList>
    </SidebarContainer>
  );
};

export default Sidebar;