import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import { evolutionAPI } from '../../services/api';

interface EvolutionRun {
  id: string;
  name: string;
  status: 'running' | 'paused' | 'completed' | 'failed';
  currentIteration: number;
  maxIterations: number;
  bestScore: number;
  startTime: string;
  endTime?: string;
  config: any;
}

interface EvolutionState {
  runs: EvolutionRun[];
  currentRun: EvolutionRun | null;
  loading: boolean;
  error: string | null;
}

const initialState: EvolutionState = {
  runs: [],
  currentRun: null,
  loading: false,
  error: null,
};

export const fetchEvolutionRuns = createAsyncThunk(
  'evolution/fetchRuns',
  async (_, { rejectWithValue }) => {
    try {
      const response = await evolutionAPI.getRuns();
      return response;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.message || 'Failed to fetch evolution runs');
    }
  }
);

export const startEvolution = createAsyncThunk(
  'evolution/start',
  async (config: any, { rejectWithValue }) => {
    try {
      const response = await evolutionAPI.startRun(config);
      return response;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.message || 'Failed to start evolution');
    }
  }
);

export const stopEvolution = createAsyncThunk(
  'evolution/stop',
  async (runId: string, { rejectWithValue }) => {
    try {
      const response = await evolutionAPI.stopRun(runId);
      return response;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.message || 'Failed to stop evolution');
    }
  }
);

const evolutionSlice = createSlice({
  name: 'evolution',
  initialState,
  reducers: {
    setCurrentRun: (state, action: PayloadAction<EvolutionRun>) => {
      state.currentRun = action.payload;
    },
    updateRunStatus: (state, action: PayloadAction<{ id: string; status: EvolutionRun['status'] }>) => {
      const run = state.runs.find(r => r.id === action.payload.id);
      if (run) {
        run.status = action.payload.status;
      }
      if (state.currentRun?.id === action.payload.id) {
        state.currentRun.status = action.payload.status;
      }
    },
    clearError: (state) => {
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    builder
      // Fetch runs
      .addCase(fetchEvolutionRuns.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchEvolutionRuns.fulfilled, (state, action) => {
        state.loading = false;
        state.runs = action.payload;
      })
      .addCase(fetchEvolutionRuns.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      })
      // Start evolution
      .addCase(startEvolution.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(startEvolution.fulfilled, (state, action) => {
        state.loading = false;
        state.runs.push(action.payload);
        state.currentRun = action.payload;
      })
      .addCase(startEvolution.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      })
      // Stop evolution
      .addCase(stopEvolution.fulfilled, (state, action) => {
        const run = state.runs.find(r => r.id === action.payload.id);
        if (run) {
          run.status = action.payload.status;
        }
        if (state.currentRun?.id === action.payload.id) {
          state.currentRun = action.payload;
        }
      });
  },
});

export const { setCurrentRun, updateRunStatus, clearError } = evolutionSlice.actions;
export default evolutionSlice.reducer;