const BACKEND_ADDRESS = process.env.REACT_APP_BACKEND_ADDRESS ?? 'localhost';
const BACKEND_PORT = process.env.REACT_APP_BACKEND_PORT ?? '5000';

const backendRoot = `http://${BACKEND_ADDRESS}:${BACKEND_PORT}`;

const Endpoint = {
  register: () => `${backendRoot}/register`,
  getPuzzle: ({puzzleId}) => `${backendRoot}/puzzles/${puzzleId}`,
  getSolution: ({puzzleId}) => `${backendRoot}/puzzles/${puzzleId}/solution`,
  createPuzzle: ({difficulty, additionalPlayers, size = 3}) => `${backendRoot}/puzzles`,
  getPuzzles: () => `${backendRoot}/puzzles`,
  movePiece: ({puzzleId}) => `${backendRoot}/puzzles/${puzzleId}/piece`,
  getLeaderboard: () => `${backendRoot}/leaderboard`,
  hidePuzzle: ({hidePuzzleId}) => `${backendRoot}/puzzles/${hidePuzzleId}?hidden=True`,
  websocket: () => `ws://${BACKEND_ADDRESS}:${BACKEND_PORT}/`,
};

export default Endpoint;
