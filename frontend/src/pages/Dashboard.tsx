import React, { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import styled from 'styled-components';
import { AppDispatch, RootState } from '../store/store';
import { fetchEvolutionRuns } from '../store/slices/evolutionSlice';
import Card from '../components/Common/Card';
import Button from '../components/Common/Button';
import LoadingSpinner from '../components/Common/LoadingSpinner';

const DashboardContainer = styled.div`
  display: flex;
  flex-direction: column;
  gap: ${props => props.theme.spacing.xl};
`;

const Header = styled.div`
  display: flex;
  justify-content: between;
  align-items: center;
  margin-bottom: ${props => props.theme.spacing.lg};
`;

const Title = styled.h1`
  color: ${props => props.theme.colors.text.primary};
  margin: 0;
`;

const StatsGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: ${props => props.theme.spacing.lg};
`;

const StatCard = styled(Card)`
  text-align: center;
`;

const StatValue = styled.div`
  font-size: 2rem;
  font-weight: bold;
  color: ${props => props.theme.colors.primary};
  margin-bottom: ${props => props.theme.spacing.sm};
`;

const StatLabel = styled.div`
  color: ${props => props.theme.colors.text.secondary};
  font-size: 0.875rem;
`;

const RecentRuns = styled.div`
  display: flex;
  flex-direction: column;
  gap: ${props => props.theme.spacing.md};
`;

const RunItem = styled(Card)`
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: ${props => props.theme.spacing.md};
`;

const RunInfo = styled.div`
  display: flex;
  flex-direction: column;
  gap: ${props => props.theme.spacing.xs};
`;

const RunName = styled.h3`
  margin: 0;
  color: ${props => props.theme.colors.text.primary};
`;

const RunStatus = styled.span<{ status: string }>`
  font-size: 0.875rem;
  padding: ${props => props.theme.spacing.xs} ${props => props.theme.spacing.sm};
  border-radius: 12px;
  font-weight: 500;

  ${props => {
    switch (props.status) {
      case 'running':
        return `
          background-color: ${props.theme.colors.success}20;
          color: ${props.theme.colors.success};
        `;
      case 'completed':
        return `
          background-color: ${props.theme.colors.primary}20;
          color: ${props.theme.colors.primary};
        `;
      case 'failed':
        return `
          background-color: ${props.theme.colors.error}20;
          color: ${props.theme.colors.error};
        `;
      default:
        return `
          background-color: ${props.theme.colors.warning}20;
          color: ${props.theme.colors.warning};
        `;
    }
  }}
`;

const Dashboard: React.FC = () => {
  const dispatch = useDispatch<AppDispatch>();
  const { runs, loading } = useSelector((state: RootState) => state.evolution);

  useEffect(() => {
    dispatch(fetchEvolutionRuns());
  }, [dispatch]);

  const runningRuns = runs.filter(run => run.status === 'running').length;
  const completedRuns = runs.filter(run => run.status === 'completed').length;
  const totalPrograms = runs.reduce((acc, run) => acc + run.currentIteration, 0);
  const bestScore = Math.max(...runs.map(run => run.bestScore), 0);

  if (loading) {
    return <LoadingSpinner size="large" />;
  }

  return (
    <DashboardContainer>
      <Header>
        <Title>Dashboard</Title>
      </Header>

      <StatsGrid>
        <StatCard>
          <StatValue>{runningRuns}</StatValue>
          <StatLabel>Active Runs</StatLabel>
        </StatCard>
        
        <StatCard>
          <StatValue>{completedRuns}</StatValue>
          <StatLabel>Completed Runs</StatLabel>
        </StatCard>
        
        <StatCard>
          <StatValue>{totalPrograms.toLocaleString()}</StatValue>
          <StatLabel>Total Programs</StatLabel>
        </StatCard>
        
        <StatCard>
          <StatValue>{bestScore.toFixed(3)}</StatValue>
          <StatLabel>Best Score</StatLabel>
        </StatCard>
      </StatsGrid>

      <div>
        <h2>Recent Evolution Runs</h2>
        <RecentRuns>
          {runs.slice(0, 5).map(run => (
            <RunItem key={run.id} hover>
              <RunInfo>
                <RunName>{run.name}</RunName>
                <div>
                  Iteration {run.currentIteration} / {run.maxIterations} • 
                  Best Score: {run.bestScore.toFixed(3)}
                </div>
              </RunInfo>
              <RunStatus status={run.status}>
                {run.status.charAt(0).toUpperCase() + run.status.slice(1)}
              </RunStatus>
            </RunItem>
          ))}
          
          {runs.length === 0 && (
            <Card>
              <div style={{ textAlign: 'center', padding: '2rem' }}>
                <p>No evolution runs yet. Start your first evolution to see results here.</p>
                <Button variant="primary">Start Evolution</Button>
              </div>
            </Card>
          )}
        </RecentRuns>
      </div>
    </DashboardContainer>
  );
};

export default Dashboard;