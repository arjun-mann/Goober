import type { NextApiRequest, NextApiResponse } from 'next';
import getSearchResults from '../../utils/query';

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed. Use POST.' });
  }

  const { query } = req.body;

  if (!query) {
    return res.status(400).json({ error: 'Query parameter is required.' });
  }

  console.log(`Received query: ${query}`);

  try {
    const urls = await getSearchResults(query);
    res.status(200).json(urls);
  } catch (error) {
    console.error('Error in search logic:', error);
    res.status(500).json({ error: 'Internal server error.' });
  }
}
