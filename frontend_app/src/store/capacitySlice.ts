import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import axios from 'axios';
import type { CapacityData } from '../types';
import { getApiUrl } from '../utils';

interface CapacityState {
  data: CapacityData[];
  loading: boolean;
  error: string | null;
}

const initialState: CapacityState = {
  data: [],
  loading: false,
  error: null,
};

export const fetchCapacity = createAsyncThunk(
  'capacity/fetch',
  async ({ dateFrom, dateTo }: { dateFrom: string; dateTo: string }) => {
    const apiUrl = getApiUrl();
    const response = await axios.get<CapacityData[]>(`${apiUrl}/capacity`, {
      params: { date_from: dateFrom, date_to: dateTo },
    });
    return response.data;
  }
);

const capacitySlice = createSlice({
  name: 'capacity',
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchCapacity.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchCapacity.fulfilled, (state, action) => {
        state.loading = false;
        state.data = action.payload;
      })
      .addCase(fetchCapacity.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || 'Failed to fetch data';
      });
  },
});

export default capacitySlice.reducer;
