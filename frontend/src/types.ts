export interface SearchResult {
  uuid: string;
  url: string;
  chunk_index: number;
  tokens: number;
  content: string;
  distance: number;
}
