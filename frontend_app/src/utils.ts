export const getApiUrl = (): string => {
  const apiUrl = import.meta.env.VITE_API_URL;
  const apiPort = import.meta.env.VITE_API_PORT;

  if (!apiUrl || !apiPort) {
    throw new Error('VITE_API_URL and VITE_API_PORT must be defined');
  }

  return `${apiUrl}:${apiPort}`;
};
