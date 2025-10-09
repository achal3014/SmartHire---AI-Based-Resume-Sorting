// ResultsTable.jsx
import { TrendingUp } from "lucide-react";

const ResultsTable = ({ results }) => {
  if (!results.length) return null;

  const getScoreColor = (score) => {
    const numScore = parseFloat(score);
    if (numScore >= 80) return "text-emerald-700 bg-emerald-50";
    if (numScore >= 60) return "text-amber-700 bg-amber-50";
    return "text-slate-700 bg-slate-50";
  };

  return (
    <div className="mt-8">
      <div className="flex items-center mb-4">
        <TrendingUp className="w-5 h-5 mr-2 text-indigo-600" />
        <h2 className="text-lg font-semibold text-slate-800">Ranking Results</h2>
      </div>
      <div className="border border-slate-200 rounded-lg overflow-hidden">
        <table className="w-full">
          <thead className="bg-slate-100">
            <tr>
              <th className="px-4 py-3 text-left text-xs font-semibold text-slate-700 uppercase tracking-wider">
                Rank
              </th>
              <th className="px-4 py-3 text-left text-xs font-semibold text-slate-700 uppercase tracking-wider">
                Candidate Resume
              </th>
              <th className="px-4 py-3 text-left text-xs font-semibold text-slate-700 uppercase tracking-wider">
                Match Score
              </th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-slate-200">
            {results.map((r, idx) => (
              <tr key={idx} className="hover:bg-slate-50">
                <td className="px-4 py-3 text-sm font-medium text-slate-900">
                  #{idx + 1}
                </td>
                <td className="px-4 py-3 text-sm text-slate-700">{r.name}</td>
                <td className="px-4 py-3 text-sm">
                  <span
                    className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${getScoreColor(
                      r.score
                    )}`}
                  >
                    {r.score}%
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default ResultsTable;