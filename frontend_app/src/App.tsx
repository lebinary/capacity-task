import { useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { fetchCapacity } from './store/capacitySlice';
import type { AppDispatch, RootState } from './store/store';
import { DateRangePicker } from './components/DateRangePicker';
import { CapacityTable } from './components/CapacityTable';
import { DATE_RANGE } from './constants';

function App() {
  const [dateFrom, setDateFrom] = useState(DATE_RANGE.MIN);
  const [dateTo, setDateTo] = useState(DATE_RANGE.MAX);
  const [nWeeks, setNWeeks] = useState(4);
  const dispatch = useDispatch<AppDispatch>();
  const { data, loading, error } = useSelector((state: RootState) => state.capacity);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    dispatch(fetchCapacity({ dateFrom, dateTo, nWeeks }));
  };

  return (
    <div className="min-h-screen bg-primary py-8">
      <div className="max-w-7xl mx-auto px-4">
        <h1 className="text-4xl font-bold text-text-primary mb-8 text-center">
          Shipping Capacity Dashboard
        </h1>
        <DateRangePicker
          dateFrom={dateFrom}
          dateTo={dateTo}
          nWeeks={nWeeks}
          onDateFromChange={setDateFrom}
          onDateToChange={setDateTo}
          onNWeeksChange={setNWeeks}
          onSubmit={handleSubmit}
          loading={loading}
        />
        <CapacityTable data={data} loading={loading} error={error} />
      </div>
    </div>
  );
}

export default App;
