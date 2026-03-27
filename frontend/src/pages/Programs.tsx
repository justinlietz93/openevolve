import React, { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import styled from 'styled-components';
import { AppDispatch, RootState } from '../store/store';
import { fetchPrograms, setSelectedProgram, setFilters, setSorting } from '../store/slices/programsSlice';
import Card from '../components/Common/Card';
import Button from '../components/Common/Button';
import Input from '../components/Common/Input';
import LoadingSpinner from '../components/Common/LoadingSpinner';

const ProgramsContainer = styled.div`
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

const FiltersContainer = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: ${props => props.theme.spacing.md};
  margin-bottom: ${props => props.theme.spacing.lg};
`;

const ProgramsGrid = styled.div`
  display: grid;
  grid-template-columns: 1fr 400px;
  gap: ${props => props.theme.spacing.lg};

  @media (max-width: ${props => props.theme.breakpoints.tablet}) {
    grid-template-columns: 1fr;
  }
`;

const ProgramsList = styled.div`
  display: flex;
  flex-direction: column;
  gap: ${props => props.theme.spacing.md};
`;

const ProgramCard = styled(Card)<{ selected: boolean }>`
  cursor: pointer;
  transition: all 0.2s ease;
  border: 2px solid ${props => props.selected ? props.theme.colors.primary : 'transparent'};

  &:hover {
    transform: translateY(-2px);
    box-shadow: ${props => props.theme.shadows.medium};
  }
`;

const ProgramHeader = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: ${props => props.theme.spacing.sm};
`;

const ProgramId = styled.h3`
  margin: 0;
  color: ${props => props.theme.colors.text.primary};
  font-family: monospace;
`;

const ProgramMeta = styled.div`
  display: flex;
  gap: ${props => props.theme.spacing.md};
  color: ${props => props.theme.colors.text.secondary};
  font-size: 0.875rem;
  margin-bottom: ${props => props.theme.spacing.sm};
`;

const MetricsGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: ${props => props.theme.spacing.sm};
`;

const MetricItem = styled.div`
  display: flex;
  flex-direction: column;
  gap: ${props => props.theme.spacing.xs};
`;

const MetricLabel = styled.span`
  font-size: 0.75rem;
  color: ${props => props.theme.colors.text.secondary};
  text-transform: uppercase;
`;

const MetricValue = styled.span`
  font-weight: 500;
  color: ${props => props.theme.colors.text.primary};
`;

const ProgramDetails = styled(Card)`
  position: sticky;
  top: ${props => props.theme.spacing.lg};
  height: fit-content;
`;

const CodeBlock = styled.pre`
  background-color: ${props => props.theme.colors.border};
  padding: ${props => props.theme.spacing.md};
  border-radius: ${props => props.theme.borderRadius};
  overflow-x: auto;
  font-size: 0.875rem;
  line-height: 1.4;
  max-height: 400px;
  overflow-y: auto;
`;

const Select = styled.select`
  padding: ${props => props.theme.spacing.sm} ${props => props.theme.spacing.md};
  border: 1px solid ${props => props.theme.colors.border};
  border-radius: ${props => props.theme.borderRadius};
  background-color: ${props => props.theme.colors.surface};
  color: ${props => props.theme.colors.text.primary};
  font-size: 0.875rem;
`;

const Programs: React.FC = () => {
  const dispatch = useDispatch<AppDispatch>();
  const { programs, selectedProgram, loading, filters, sortBy, sortOrder } = useSelector(
    (state: RootState) => state.programs
  );
  
  const [selectedRunId, setSelectedRunId] = useState('');

  useEffect(() => {
    if (selectedRunId) {
      dispatch(fetchPrograms(selectedRunId));
    }
  }, [dispatch, selectedRunId]);

  const handleProgramSelect = (program: any) => {
    dispatch(setSelectedProgram(program));
  };

  const handleFilterChange = (key: string, value: any) => {
    dispatch(setFilters({ [key]: value }));
  };

  const handleSortChange = (newSortBy: any) => {
    const newSortOrder = sortBy === newSortBy && sortOrder === 'desc' ? 'asc' : 'desc';
    dispatch(setSorting({ sortBy: newSortBy, sortOrder: newSortOrder }));
  };

  // Filter and sort programs
  const filteredPrograms = programs.filter(program => {
    if (filters.generation && program.generation !== filters.generation) return false;
    if (filters.island && program.island !== filters.island) return false;
    if (filters.minScore && (!program.metrics.combined_score || program.metrics.combined_score < filters.minScore)) return false;
    return true;
  });

  const sortedPrograms = [...filteredPrograms].sort((a, b) => {
    let aValue, bValue;
    
    switch (sortBy) {
      case 'score':
        aValue = a.metrics.combined_score || 0;
        bValue = b.metrics.combined_score || 0;
        break;
      case 'timestamp':
        aValue = new Date(a.timestamp).getTime();
        bValue = new Date(b.timestamp).getTime();
        break;
      default:
        aValue = a.generation;
        bValue = b.generation;
    }
    
    return sortOrder === 'desc' ? bValue - aValue : aValue - bValue;
  });

  if (loading) {
    return <LoadingSpinner size="large" />;
  }

  return (
    <ProgramsContainer>
      <Header>
        <Title>Programs</Title>
        <Input
          label="Evolution Run ID"
          value={selectedRunId}
          onChange={(e) => setSelectedRunId(e.target.value)}
          placeholder="Enter run ID to load programs"
        />
      </Header>

      {selectedRunId && (
        <>
          <FiltersContainer>
            <div>
              <label>Generation</label>
              <Input
                type="number"
                value={filters.generation || ''}
                onChange={(e) => handleFilterChange('generation', e.target.value ? Number(e.target.value) : undefined)}
                placeholder="Filter by generation"
              />
            </div>
            
            <div>
              <label>Island</label>
              <Input
                type="number"
                value={filters.island || ''}
                onChange={(e) => handleFilterChange('island', e.target.value ? Number(e.target.value) : undefined)}
                placeholder="Filter by island"
              />
            </div>
            
            <div>
              <label>Min Score</label>
              <Input
                type="number"
                step="0.01"
                value={filters.minScore || ''}
                onChange={(e) => handleFilterChange('minScore', e.target.value ? Number(e.target.value) : undefined)}
                placeholder="Minimum score"
              />
            </div>
            
            <div>
              <label>Sort By</label>
              <Select value={sortBy} onChange={(e) => handleSortChange(e.target.value)}>
                <option value="generation">Generation</option>
                <option value="score">Score</option>
                <option value="timestamp">Time</option>
              </Select>
            </div>
          </FiltersContainer>

          <ProgramsGrid>
            <ProgramsList>
              {sortedPrograms.map(program => (
                <ProgramCard
                  key={program.id}
                  selected={selectedProgram?.id === program.id}
                  onClick={() => handleProgramSelect(program)}
                  hover
                >
                  <ProgramHeader>
                    <ProgramId>{program.id}</ProgramId>
                    <Button variant="outline" size="small">
                      View Code
                    </Button>
                  </ProgramHeader>
                  
                  <ProgramMeta>
                    <span>Gen: {program.generation}</span>
                    <span>Island: {program.island}</span>
                    <span>Iteration: {program.iterationFound}</span>
                  </ProgramMeta>
                  
                  <MetricsGrid>
                    {Object.entries(program.metrics).map(([key, value]) => (
                      <MetricItem key={key}>
                        <MetricLabel>{key}</MetricLabel>
                        <MetricValue>{typeof value === 'number' ? value.toFixed(4) : value}</MetricValue>
                      </MetricItem>
                    ))}
                  </MetricsGrid>
                </ProgramCard>
              ))}
              
              {sortedPrograms.length === 0 && (
                <Card>
                  <div style={{ textAlign: 'center', padding: '3rem' }}>
                    <h3>No Programs Found</h3>
                    <p>No programs match your current filters.</p>
                  </div>
                </Card>
              )}
            </ProgramsList>

            {selectedProgram && (
              <ProgramDetails>
                <h3>Program Details</h3>
                
                <div style={{ marginBottom: '1rem' }}>
                  <strong>ID:</strong> {selectedProgram.id}
                </div>
                
                <div style={{ marginBottom: '1rem' }}>
                  <strong>Generation:</strong> {selectedProgram.generation}
                </div>
                
                <div style={{ marginBottom: '1rem' }}>
                  <strong>Parent:</strong> {selectedProgram.parentId || 'None'}
                </div>
                
                <div style={{ marginBottom: '1rem' }}>
                  <strong>Language:</strong> {selectedProgram.language}
                </div>
                
                <h4>Metrics</h4>
                <MetricsGrid style={{ marginBottom: '1rem' }}>
                  {Object.entries(selectedProgram.metrics).map(([key, value]) => (
                    <MetricItem key={key}>
                      <MetricLabel>{key}</MetricLabel>
                      <MetricValue>{typeof value === 'number' ? value.toFixed(4) : value}</MetricValue>
                    </MetricItem>
                  ))}
                </MetricsGrid>
                
                <h4>Code</h4>
                <CodeBlock>{selectedProgram.code}</CodeBlock>
              </ProgramDetails>
            )}
          </ProgramsGrid>
        </>
      )}
    </ProgramsContainer>
  );
};

export default Programs;