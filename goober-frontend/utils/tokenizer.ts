import { newStemmer } from 'snowball-stemmers';

/**
 * Tokenizes and stems text using `snowball-stemmers`.
 *
 * @param text - The text content to tokenize.
 * @param language - The language for stemming (default is 'english').
 * @returns An array of stemmed tokens extracted from the text.
 */
export function tokenize(text: string, language: string = 'english'): string[] {
  // Regular expression to match words with alphanumeric characters
  const regex = /\b\w+\b/g;

  // Extract tokens using the regex
  const tokens = text.match(regex) || [];

  // Initialize the Snowball stemmer for the given language
  const stemmer = newStemmer(language);

  // Apply stemming and convert tokens to lowercase
  const stemmedTokens = tokens.map((token) => stemmer.stem(token.toLowerCase()));

  return stemmedTokens;
}
