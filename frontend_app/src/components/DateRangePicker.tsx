import { DATE_RANGE } from '../constants';

interface DateRangePickerProps {
  dateFrom: string;
  dateTo: string;
  nWeeks: number;
  onDateFromChange: (date: string) => void;
  onDateToChange: (date: string) => void;
  onNWeeksChange: (nWeeks: number) => void;
  onSubmit: (e: React.FormEvent) => void;
  loading: boolean;
}

export const DateRangePicker = ({
  dateFrom,
  dateTo,
  nWeeks,
  onDateFromChange,
  onDateToChange,
  onNWeeksChange,
  onSubmit,
  loading,
}: DateRangePickerProps) => {
  return (
    <form onSubmit={onSubmit} className="bg-primary-light p-6 rounded-lg shadow-lg mb-6">
      <div className="flex flex-col md:flex-row gap-4">
        <div className="flex-1">
          <label className="block text-sm font-medium text-text-secondary mb-2">
            Date From:
          </label>
          <input
            type="date"
            value={dateFrom}
            onChange={(e) => onDateFromChange(e.target.value)}
            min={DATE_RANGE.MIN}
            max={DATE_RANGE.MAX}
            required
            className="w-full px-4 py-2 bg-primary border border-border text-text-primary rounded-md focus:ring-2 focus:ring-secondary focus:border-secondary [color-scheme:dark]"
          />
        </div>

        <div className="flex-1">
          <label className="block text-sm font-medium text-text-secondary mb-2">
            Date To:
          </label>
          <input
            type="date"
            value={dateTo}
            onChange={(e) => onDateToChange(e.target.value)}
            min={DATE_RANGE.MIN}
            max={DATE_RANGE.MAX}
            required
            className="w-full px-4 py-2 bg-primary border border-border text-text-primary rounded-md focus:ring-2 focus:ring-secondary focus:border-secondary [color-scheme:dark]"
          />
        </div>

        <div className="flex-1">
          <label className="block text-sm font-medium text-text-secondary mb-2">
            N-Week:
          </label>
          <input
            type="number"
            value={nWeeks}
            onChange={(e) => onNWeeksChange(Number(e.target.value))}
            min={1}
            max={8}
            required
            className="w-full px-4 py-2 bg-primary border border-border text-text-primary rounded-md focus:ring-2 focus:ring-secondary focus:border-secondary"
          />
        </div>

        <button
          type="submit"
          disabled={loading}
          className="md:mt-7 px-6 py-2 bg-secondary text-text-primary rounded-md hover:bg-secondary-hover disabled:bg-disabled cursor-pointer disabled:cursor-not-allowed transition-colors font-medium"
        >
          {loading ? 'Loading...' : 'Query Capacity'}
        </button>
      </div>
    </form>
  );
};
