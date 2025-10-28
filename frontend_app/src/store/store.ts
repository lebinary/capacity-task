import { configureStore } from '@reduxjs/toolkit';
import capacityReducer from './capacitySlice';

export const store = configureStore({
  reducer: {
    capacity: capacityReducer,
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
