import { useState } from "react";

interface SearchBarProps {
  onSearch: (params: { url: string; query: string }) => void;
}

export default function SearchBar({ onSearch }: SearchBarProps) {
  const [url, setUrl] = useState("");
  const [query, setQuery] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (url && query) {
      onSearch({ url, query });
    }
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="flex flex-col items-center gap-3 max-w-2xl mx-auto"
    >
      <input
        type="url"
        placeholder="https://example.com"
        value={url}
        onChange={(e) => setUrl(e.target.value)}
        className="w-full border rounded-lg p-2 shadow-sm"
        required
      />
      <div className="flex w-full gap-2">
        <input
          type="text"
          placeholder="Search query..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="flex-grow border rounded-lg p-2 shadow-sm"
          required
        />
        <button
          type="submit"
          className="bg-blue-600 text-white px-6 py-2 rounded-lg shadow hover:bg-blue-700"
        >
          Search
        </button>
      </div>
    </form>
  );
}
