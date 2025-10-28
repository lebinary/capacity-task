import { DATE_RANGE } from '../constants';

interface DateRangePickerProps {
  dateFrom: string;
  dateTo: string;
  onDateFromChange: (date: string) => void;
  onDateToChange: (date: string) => void;
  onSubmit: (e: React.FormEvent) => void;
  loading: boolean;
}

export const DateRangePicker = ({
  dateFrom,
  dateTo,
  onDateFromChange,
  onDateToChange,
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
