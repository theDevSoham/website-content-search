import { useState } from "react";
import SearchBar from "./components/SearchBar";
import ResultsList from "./components/ResultsList";
import type { SearchResult } from "./types";

function App() {
  const [results, setResults] = useState<SearchResult[]>([]);
  const [loading, setLoading] = useState(false);

  const handleSearch = async ({
    url,
    query,
  }: {
    url: string;
    query: string;
  }) => {
    setLoading(true);
    const baseUrl = import.meta.env.VITE_BASE_URL;
    try {
      const res = await fetch(`${baseUrl}/api/search`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url, query }),
      });

      const data = await res.json();
      // Adjust depending on your FastAPI response structure
      setResults(data.results || []);
    } catch (err) {
      console.error("Search failed:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <h1 className="text-3xl font-bold text-center mb-2">
        Website Content Search
      </h1>
      <p className="text-center text-gray-500 mb-6">
        Search through website content with precision
      </p>

      <SearchBar onSearch={handleSearch} />

      {loading && <p className="text-center mt-6">Loading...</p>}

      {!loading && results.length > 0 && <ResultsList results={results} />}
    </div>
  );
}

export default App;
