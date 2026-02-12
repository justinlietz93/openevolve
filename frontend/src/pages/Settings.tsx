import React, { useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import styled from 'styled-components';
import { RootState } from '../store/store';
import { setTheme } from '../store/slices/uiSlice';
import Card from '../components/Common/Card';
import Button from '../components/Common/Button';
import Input from '../components/Common/Input';
import { useToast } from '../hooks/useToast';

const SettingsContainer = styled.div`
  display: flex;
  flex-direction: column;
  gap: ${props => props.theme.spacing.xl};
  max-width: 800px;
`;

const Title = styled.h1`
  color: ${props => props.theme.colors.text.primary};
  margin: 0 0 ${props => props.theme.spacing.lg} 0;
`;

const SettingSection = styled(Card)`
  display: flex;
  flex-direction: column;
  gap: ${props => props.theme.spacing.lg};
`;

const SectionTitle = styled.h2`
  color: ${props => props.theme.colors.text.primary};
  margin: 0;
  font-size: 1.25rem;
`;

const SettingRow = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: ${props => props.theme.spacing.md} 0;
  border-bottom: 1px solid ${props => props.theme.colors.border};

  &:last-child {
    border-bottom: none;
  }

  @media (max-width: ${props => props.theme.breakpoints.mobile}) {
    flex-direction: column;
    align-items: stretch;
    gap: ${props => props.theme.spacing.md};
  }
`;

const SettingInfo = styled.div`
  display: flex;
  flex-direction: column;
  gap: ${props => props.theme.spacing.xs};
`;

const SettingLabel = styled.h3`
  margin: 0;
  color: ${props => props.theme.colors.text.primary};
  font-size: 1rem;
`;

const SettingDescription = styled.p`
  margin: 0;
  color: ${props => props.theme.colors.text.secondary};
  font-size: 0.875rem;
`;

const Select = styled.select`
  padding: ${props => props.theme.spacing.sm} ${props => props.theme.spacing.md};
  border: 1px solid ${props => props.theme.colors.border};
  border-radius: ${props => props.theme.borderRadius};
  background-color: ${props => props.theme.colors.surface};
  color: ${props => props.theme.colors.text.primary};
  font-size: 0.875rem;
  min-width: 150px;
`;

const FormGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: ${props => props.theme.spacing.lg};
`;

const Settings: React.FC = () => {
  const dispatch = useDispatch();
  const { theme } = useSelector((state: RootState) => state.ui);
  const { user } = useSelector((state: RootState) => state.auth);
  const { showSuccess, showError } = useToast();

  const [profileData, setProfileData] = useState({
    name: user?.name || '',
    email: user?.email || '',
  });

  const [apiSettings, setApiSettings] = useState({
    openaiApiKey: '',
    defaultModel: 'gpt-4',
    temperature: 0.7,
    maxTokens: 4096,
  });

  const handleThemeChange = (newTheme: 'light' | 'dark') => {
    dispatch(setTheme(newTheme));
    showSuccess(`Theme changed to ${newTheme} mode`);
  };

  const handleProfileSave = () => {
    // TODO: Implement profile update API call
    showSuccess('Profile updated successfully');
  };

  const handleApiSettingsSave = () => {
    // TODO: Implement API settings save
    showSuccess('API settings saved successfully');
  };

  const handleProfileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setProfileData({
      ...profileData,
      [e.target.name]: e.target.value,
    });
  };

  const handleApiSettingsChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setApiSettings({
      ...apiSettings,
      [name]: name === 'temperature' || name === 'maxTokens' ? Number(value) : value,
    });
  };

  return (
    <SettingsContainer>
      <Title>Settings</Title>

      <SettingSection>
        <SectionTitle>Appearance</SectionTitle>
        
        <SettingRow>
          <SettingInfo>
            <SettingLabel>Theme</SettingLabel>
            <SettingDescription>
              Choose between light and dark mode
            </SettingDescription>
          </SettingInfo>
          
          <Select
            value={theme}
            onChange={(e) => handleThemeChange(e.target.value as 'light' | 'dark')}
          >
            <option value="light">Light</option>
            <option value="dark">Dark</option>
          </Select>
        </SettingRow>
      </SettingSection>

      <SettingSection>
        <SectionTitle>Profile</SectionTitle>
        
        <FormGrid>
          <Input
            label="Name"
            name="name"
            value={profileData.name}
            onChange={handleProfileChange}
            fullWidth
          />
          
          <Input
            label="Email"
            name="email"
            type="email"
            value={profileData.email}
            onChange={handleProfileChange}
            fullWidth
          />
        </FormGrid>
        
        <div>
          <Button variant="primary" onClick={handleProfileSave}>
            Save Profile
          </Button>
        </div>
      </SettingSection>

      <SettingSection>
        <SectionTitle>API Configuration</SectionTitle>
        
        <FormGrid>
          <Input
            label="OpenAI API Key"
            name="openaiApiKey"
            type="password"
            value={apiSettings.openaiApiKey}
            onChange={handleApiSettingsChange}
            placeholder="sk-..."
            fullWidth
          />
          
          <div>
            <label>Default Model</label>
            <Select
              name="defaultModel"
              value={apiSettings.defaultModel}
              onChange={handleApiSettingsChange}
            >
              <option value="gpt-4">GPT-4</option>
              <option value="gpt-3.5-turbo">GPT-3.5 Turbo</option>
              <option value="claude-3-opus">Claude 3 Opus</option>
              <option value="claude-3-sonnet">Claude 3 Sonnet</option>
            </Select>
          </div>
          
          <Input
            label="Temperature"
            name="temperature"
            type="number"
            step="0.1"
            min="0"
            max="2"
            value={apiSettings.temperature}
            onChange={handleApiSettingsChange}
            fullWidth
          />
          
          <Input
            label="Max Tokens"
            name="maxTokens"
            type="number"
            value={apiSettings.maxTokens}
            onChange={handleApiSettingsChange}
            fullWidth
          />
        </FormGrid>
        
        <div>
          <Button variant="primary" onClick={handleApiSettingsSave}>
            Save API Settings
          </Button>
        </div>
      </SettingSection>

      <SettingSection>
        <SectionTitle>Evolution Defaults</SectionTitle>
        
        <SettingRow>
          <SettingInfo>
            <SettingLabel>Default Population Size</SettingLabel>
            <SettingDescription>
              Default population size for new evolution runs
            </SettingDescription>
          </SettingInfo>
          
          <Input
            type="number"
            defaultValue={100}
            style={{ width: '150px' }}
          />
        </SettingRow>
        
        <SettingRow>
          <SettingInfo>
            <SettingLabel>Default Max Iterations</SettingLabel>
            <SettingDescription>
              Default maximum iterations for new evolution runs
            </SettingDescription>
          </SettingInfo>
          
          <Input
            type="number"
            defaultValue={1000}
            style={{ width: '150px' }}
          />
        </SettingRow>
        
        <SettingRow>
          <SettingInfo>
            <SettingLabel>Auto-save Checkpoints</SettingLabel>
            <SettingDescription>
              Automatically save evolution checkpoints
            </SettingDescription>
          </SettingInfo>
          
          <Select defaultValue="enabled">
            <option value="enabled">Enabled</option>
            <option value="disabled">Disabled</option>
          </Select>
        </SettingRow>
      </SettingSection>
    </SettingsContainer>
  );
};

export default Settings;