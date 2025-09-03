import { useState } from "react";
import type { SearchResult } from "../types";

interface ResultCardProps {
  result: SearchResult;
}

export default function ResultCard({ result }: ResultCardProps) {
  const [showHtml, setShowHtml] = useState(false);

  return (
    <div className="border rounded-lg bg-white shadow p-4">
      <div className="flex justify-between items-center">
        <p className="font-medium">{result.uuid}</p>
        <span className="bg-green-100 text-green-700 px-2 py-1 rounded text-sm">
          {Math.round(result.distance * 100)}% match
        </span>
      </div>
      <p className="text-sm text-gray-500 mt-1">Path: {result.url}</p>

      <button
        onClick={() => setShowHtml(!showHtml)}
        className="text-blue-600 text-sm mt-2"
      >
        {showHtml ? "Hide HTML ▲" : "View HTML ▼"}
      </button>

      {showHtml && (
        <pre className="bg-gray-100 p-2 mt-2 rounded overflow-x-auto text-xs">
          {result.content}
        </pre>
      )}
    </div>
  );
}
