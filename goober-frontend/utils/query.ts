import fs from 'fs';
import path from 'path';
import { tokenize } from './tokenizer';

interface UrlMapping {
  [key: string]: [string, string, string];
}

interface Tags {
  [key: string]: Array<[number, string, number]>;
}

export default async function getSearchResults(query: string): Promise<string[]> {
  const docs = 55391; // Number of documents in your dataset
  const indexPath = path.join(process.cwd(), '../final_indicies');
  const urlMappingFile = path.join(process.cwd(), '../url_mapping.json');

  console.log('Index Path:', indexPath);
  console.log('URL Mapping Path:', urlMappingFile);

  // Initialize structures
  const q: Record<string, number> = {};
  const tokenFreq: Array<[string, number]> = [];
  const results: string[] = [];

  try {
    // Load URL mapping file
    const mapping: UrlMapping = JSON.parse(fs.readFileSync(urlMappingFile, 'utf8'));

    // Load index file
    const tags: Tags = JSON.parse(fs.readFileSync(path.join(indexPath, '../final_indicies/index_0.json'), 'utf8'));

    // Tokenize the query
    const tokens = tokenize(query);

    // Compute token frequencies
    tokens.forEach((token) => {
      if (tags[token]) {
        tokenFreq.push([token, tags[token].length]);
      }
    });

    // Sort tokens by frequency (ascending)
    tokenFreq.sort((a, b) => a[1] - b[1]);

    // Compute scores for documents
    for (let i = 0; i < tokenFreq.length; i++) {
      const token = tokenFreq[i][0];

      if (i === 0) {
        // Process the first token (most specific)
        for (let j = 0; j < 50; j++) {
          try {
            const posting = tags[token][j];
            q[posting[0]] = posting[2]; // Initialize score for this document
          } catch (error) {
            continue;
          }
        }
      } else {
        // Process subsequent tokens
        tags[token].forEach((posting) => {
          if (q[posting[0]]) {
            q[posting[0]] += posting[2]; // Increment the score
          }
        });
      }
    }

    // Sort results by score (descending) and take the top 10
    const sortedResults = Object.entries(q)
      .sort(([, scoreA], [, scoreB]) => scoreB - scoreA)
      .slice(0, 10)
      .map(([docId]) => docId);

    // Map document IDs to URLs
    sortedResults.forEach((docId) => {
      const url = mapping[docId]?.[0];
      if (url) {
        results.push(url);
      }
    });

    return results;
  } catch (error) {
    console.error('Error in getSearchResults:', error);
    throw new Error('Internal Server Error');
  }
}
