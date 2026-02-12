import React, { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import styled from 'styled-components';
import { AppDispatch, RootState } from '../store/store';
import { fetchEvolutionRuns, startEvolution, stopEvolution } from '../store/slices/evolutionSlice';
import Card from '../components/Common/Card';
import Button from '../components/Common/Button';
import Input from '../components/Common/Input';
import LoadingSpinner from '../components/Common/LoadingSpinner';
import { useToast } from '../hooks/useToast';

const EvolutionContainer = styled.div`
  display: flex;
  flex-direction: column;
  gap: ${props => props.theme.spacing.xl};
`;

const Header = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: ${props => props.theme.spacing.lg};

  @media (max-width: ${props => props.theme.breakpoints.mobile}) {
    flex-direction: column;
    gap: ${props => props.theme.spacing.md};
    align-items: stretch;
  }
`;

const Title = styled.h1`
  color: ${props => props.theme.colors.text.primary};
  margin: 0;
`;

const ConfigForm = styled.form`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: ${props => props.theme.spacing.lg};
  margin-bottom: ${props => props.theme.spacing.lg};
`;

const RunsList = styled.div`
  display: flex;
  flex-direction: column;
  gap: ${props => props.theme.spacing.md};
`;

const RunCard = styled(Card)`
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: ${props => props.theme.spacing.lg};

  @media (max-width: ${props => props.theme.breakpoints.mobile}) {
    flex-direction: column;
    gap: ${props => props.theme.spacing.md};
    align-items: stretch;
  }
`;

const RunInfo = styled.div`
  display: flex;
  flex-direction: column;
  gap: ${props => props.theme.spacing.sm};
  flex: 1;
`;

const RunName = styled.h3`
  margin: 0;
  color: ${props => props.theme.colors.text.primary};
`;

const RunDetails = styled.div`
  color: ${props => props.theme.colors.text.secondary};
  font-size: 0.875rem;
`;

const ProgressBar = styled.div`
  width: 100%;
  height: 8px;
  background-color: ${props => props.theme.colors.border};
  border-radius: 4px;
  overflow: hidden;
  margin: ${props => props.theme.spacing.sm} 0;
`;

const ProgressFill = styled.div<{ progress: number }>`
  height: 100%;
  background-color: ${props => props.theme.colors.primary};
  width: ${props => props.progress}%;
  transition: width 0.3s ease;
`;

const RunActions = styled.div`
  display: flex;
  gap: ${props => props.theme.spacing.sm};

  @media (max-width: ${props => props.theme.breakpoints.mobile}) {
    justify-content: stretch;
    
    button {
      flex: 1;
    }
  }
`;

const StatusBadge = styled.span<{ status: string }>`
  padding: ${props => props.theme.spacing.xs} ${props => props.theme.spacing.sm};
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 500;
  text-transform: uppercase;

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

const Evolution: React.FC = () => {
  const dispatch = useDispatch<AppDispatch>();
  const { runs, loading } = useSelector((state: RootState) => state.evolution);
  const { showSuccess, showError } = useToast();

  const [showNewRunForm, setShowNewRunForm] = useState(false);
  const [newRunConfig, setNewRunConfig] = useState({
    name: '',
    maxIterations: 1000,
    populationSize: 100,
    primaryModel: 'gpt-4',
    temperature: 0.7,
  });

  useEffect(() => {
    dispatch(fetchEvolutionRuns());
  }, [dispatch]);

  const handleStartEvolution = async (e: React.FormEvent) => {
    e.preventDefault();
    
    try {
      await dispatch(startEvolution(newRunConfig)).unwrap();
      setShowNewRunForm(false);
      setNewRunConfig({
        name: '',
        maxIterations: 1000,
        populationSize: 100,
        primaryModel: 'gpt-4',
        temperature: 0.7,
      });
      showSuccess('Evolution run started successfully!');
    } catch (error) {
      showError('Failed to start evolution run');
    }
  };

  const handleStopEvolution = async (runId: string) => {
    try {
      await dispatch(stopEvolution(runId)).unwrap();
      showSuccess('Evolution run stopped');
    } catch (error) {
      showError('Failed to stop evolution run');
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setNewRunConfig(prev => ({
      ...prev,
      [name]: name === 'maxIterations' || name === 'populationSize' || name === 'temperature' 
        ? Number(value) 
        : value,
    }));
  };

  if (loading && runs.length === 0) {
    return <LoadingSpinner size="large" />;
  }

  return (
    <EvolutionContainer>
      <Header>
        <Title>Evolution Runs</Title>
        <Button 
          variant="primary" 
          onClick={() => setShowNewRunForm(!showNewRunForm)}
        >
          {showNewRunForm ? 'Cancel' : 'New Evolution Run'}
        </Button>
      </Header>

      {showNewRunForm && (
        <Card>
          <h3>Start New Evolution Run</h3>
          <ConfigForm onSubmit={handleStartEvolution}>
            <Input
              label="Run Name"
              name="name"
              value={newRunConfig.name}
              onChange={handleInputChange}
              required
              fullWidth
            />
            
            <Input
              label="Max Iterations"
              name="maxIterations"
              type="number"
              value={newRunConfig.maxIterations}
              onChange={handleInputChange}
              required
              fullWidth
            />
            
            <Input
              label="Population Size"
              name="populationSize"
              type="number"
              value={newRunConfig.populationSize}
              onChange={handleInputChange}
              required
              fullWidth
            />
            
            <Input
              label="Primary Model"
              name="primaryModel"
              value={newRunConfig.primaryModel}
              onChange={handleInputChange}
              required
              fullWidth
            />
            
            <Input
              label="Temperature"
              name="temperature"
              type="number"
              step="0.1"
              min="0"
              max="2"
              value={newRunConfig.temperature}
              onChange={handleInputChange}
              required
              fullWidth
            />
            
            <div style={{ gridColumn: '1 / -1' }}>
              <Button type="submit" variant="primary" loading={loading}>
                Start Evolution
              </Button>
            </div>
          </ConfigForm>
        </Card>
      )}

      <div>
        <h2>Evolution Runs</h2>
        <RunsList>
          {runs.map(run => {
            const progress = (run.currentIteration / run.maxIterations) * 100;
            
            return (
              <RunCard key={run.id}>
                <RunInfo>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                    <RunName>{run.name}</RunName>
                    <StatusBadge status={run.status}>{run.status}</StatusBadge>
                  </div>
                  
                  <RunDetails>
                    Started: {new Date(run.startTime).toLocaleString()}
                  </RunDetails>
                  
                  <RunDetails>
                    Progress: {run.currentIteration} / {run.maxIterations} iterations
                  </RunDetails>
                  
                  <ProgressBar>
                    <ProgressFill progress={progress} />
                  </ProgressBar>
                  
                  <RunDetails>
                    Best Score: {run.bestScore.toFixed(4)}
                  </RunDetails>
                </RunInfo>
                
                <RunActions>
                  {run.status === 'running' && (
                    <Button 
                      variant="danger" 
                      size="small"
                      onClick={() => handleStopEvolution(run.id)}
                    >
                      Stop
                    </Button>
                  )}
                  
                  <Button variant="outline" size="small">
                    View Details
                  </Button>
                </RunActions>
              </RunCard>
            );
          })}
          
          {runs.length === 0 && (
            <Card>
              <div style={{ textAlign: 'center', padding: '3rem' }}>
                <h3>No Evolution Runs</h3>
                <p>Start your first evolution run to begin optimizing your code.</p>
                <Button 
                  variant="primary" 
                  onClick={() => setShowNewRunForm(true)}
                >
                  Create First Run
                </Button>
              </div>
            </Card>
          )}
        </RunsList>
      </div>
    </EvolutionContainer>
  );
};

export default Evolution;