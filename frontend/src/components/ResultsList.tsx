import type { SearchResult } from "../types";
import ResultCard from "./ResultCard";

interface ResultsListProps {
  results: SearchResult[];
}

export default function ResultsList({ results }: ResultsListProps) {
  return (
    <div className="mt-8 space-y-4 max-w-3xl mx-auto">
      <h2 className="text-xl font-semibold">Search Results</h2>
      {results.map((result, idx) => (
        <ResultCard key={idx} result={result} />
      ))}
    </div>
  );
}
