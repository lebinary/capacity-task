import type { CapacityData } from '../types';

interface CapacityTableProps {
  data: CapacityData[];
  loading: boolean;
  error: string | null;
}

export const CapacityTable = ({ data, loading, error }: CapacityTableProps) => {
  if (loading) {
    return null;
  }

  if (error) {
    return <div className="bg-error-bg border border-error-border text-error-text px-4 py-3 rounded-md">{error}</div>;
  }

  if (data.length === 0) {
    return <div className="bg-info-bg border border-secondary text-info-text px-4 py-3 rounded-md text-center">Select date range and click Query Capacity</div>;
  }

  return (
    <div className="bg-primary-light rounded-lg shadow-lg overflow-hidden">
      <table className="min-w-full divide-y divide-border-divider">
        <thead className="bg-primary-dark">
          <tr>
            <th className="px-6 py-3 text-left text-xs font-medium text-text-secondary uppercase tracking-wider">Week Start Date</th>
            <th className="px-6 py-3 text-left text-xs font-medium text-text-secondary uppercase tracking-wider">Week No</th>
            <th className="px-6 py-3 text-left text-xs font-medium text-text-secondary uppercase tracking-wider">Offered Capacity (TEU)</th>
          </tr>
        </thead>
        <tbody className="bg-primary-light divide-y divide-border-divider">
          {data.map((row) => (
            <tr key={row.week_start_date} className="hover:bg-primary-dark transition-colors">
              <td className="px-6 py-4 whitespace-nowrap text-sm text-text-primary">{row.week_start_date}</td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-text-primary">{row.week_no}</td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-text-primary">{row.offered_capacity_teu.toLocaleString()}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};
