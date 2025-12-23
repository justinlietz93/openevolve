import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import { programsAPI } from '../../services/api';

interface Program {
  id: string;
  code: string;
  language: string;
  parentId?: string;
  generation: number;
  timestamp: string;
  iterationFound: number;
  metrics: Record<string, number>;
  complexity: number;
  diversity: number;
  metadata: any;
  island?: number;
}

interface ProgramsState {
  programs: Program[];
  selectedProgram: Program | null;
  loading: boolean;
  error: string | null;
  filters: {
    generation?: number;
    island?: number;
    metric?: string;
    minScore?: number;
  };
  sortBy: 'generation' | 'score' | 'timestamp';
  sortOrder: 'asc' | 'desc';
}

const initialState: ProgramsState = {
  programs: [],
  selectedProgram: null,
  loading: false,
  error: null,
  filters: {},
  sortBy: 'generation',
  sortOrder: 'desc',
};

export const fetchPrograms = createAsyncThunk(
  'programs/fetch',
  async (runId: string, { rejectWithValue }) => {
    try {
      const response = await programsAPI.getPrograms(runId);
      return response;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.message || 'Failed to fetch programs');
    }
  }
);

export const fetchProgramDetails = createAsyncThunk(
  'programs/fetchDetails',
  async (programId: string, { rejectWithValue }) => {
    try {
      const response = await programsAPI.getProgramDetails(programId);
      return response;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.message || 'Failed to fetch program details');
    }
  }
);

const programsSlice = createSlice({
  name: 'programs',
  initialState,
  reducers: {
    setSelectedProgram: (state, action: PayloadAction<Program | null>) => {
      state.selectedProgram = action.payload;
    },
    setFilters: (state, action: PayloadAction<Partial<ProgramsState['filters']>>) => {
      state.filters = { ...state.filters, ...action.payload };
    },
    setSorting: (state, action: PayloadAction<{ sortBy: ProgramsState['sortBy']; sortOrder: ProgramsState['sortOrder'] }>) => {
      state.sortBy = action.payload.sortBy;
      state.sortOrder = action.payload.sortOrder;
    },
    clearFilters: (state) => {
      state.filters = {};
    },
    clearError: (state) => {
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    builder
      // Fetch programs
      .addCase(fetchPrograms.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchPrograms.fulfilled, (state, action) => {
        state.loading = false;
        state.programs = action.payload;
      })
      .addCase(fetchPrograms.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      })
      // Fetch program details
      .addCase(fetchProgramDetails.fulfilled, (state, action) => {
        state.selectedProgram = action.payload;
      });
  },
});

export const { setSelectedProgram, setFilters, setSorting, clearFilters, clearError } = programsSlice.actions;
export default programsSlice.reducer;