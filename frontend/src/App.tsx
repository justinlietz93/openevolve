import React, { useEffect } from 'react';
import { Routes, Route } from 'react-router-dom';
import { useDispatch } from 'react-redux';
import styled, { ThemeProvider } from 'styled-components';
import { AppDispatch } from './store/store';
import { checkAuthStatus } from './store/slices/authSlice';
import { useTheme } from './hooks/useTheme';
import { lightTheme, darkTheme } from './styles/theme';
import Header from './components/Layout/Header';
import Sidebar from './components/Layout/Sidebar';
import Dashboard from './pages/Dashboard';
import Evolution from './pages/Evolution';
import Programs from './pages/Programs';
import Settings from './pages/Settings';
import Login from './pages/Login';
import ProtectedRoute from './components/Auth/ProtectedRoute';
import ErrorBoundary from './components/Common/ErrorBoundary';
import Toast from './components/Common/Toast';

const AppContainer = styled.div`
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background-color: ${props => props.theme.colors.background};
  color: ${props => props.theme.colors.text.primary};
`;

const MainContent = styled.div`
  display: flex;
  flex: 1;
`;

const ContentArea = styled.main`
  flex: 1;
  padding: ${props => props.theme.spacing.lg};
  overflow-y: auto;

  @media (max-width: 768px) {
    padding: ${props => props.theme.spacing.md};
  }
`;

function App() {
  const dispatch = useDispatch<AppDispatch>();
  const { theme, isDark } = useTheme();

  useEffect(() => {
    dispatch(checkAuthStatus());
  }, [dispatch]);

  return (
    <ThemeProvider theme={isDark ? darkTheme : lightTheme}>
      <ErrorBoundary>
        <AppContainer>
          <Header />
          <MainContent>
            <Sidebar />
            <ContentArea>
              <Routes>
                <Route path="/login" element={<Login />} />
                <Route path="/" element={
                  <ProtectedRoute>
                    <Dashboard />
                  </ProtectedRoute>
                } />
                <Route path="/evolution" element={
                  <ProtectedRoute>
                    <Evolution />
                  </ProtectedRoute>
                } />
                <Route path="/programs" element={
                  <ProtectedRoute>
                    <Programs />
                  </ProtectedRoute>
                } />
                <Route path="/settings" element={
                  <ProtectedRoute>
                    <Settings />
                  </ProtectedRoute>
                } />
              </Routes>
            </ContentArea>
          </MainContent>
          <Toast />
        </AppContainer>
      </ErrorBoundary>
    </ThemeProvider>
  );
}

export default App;