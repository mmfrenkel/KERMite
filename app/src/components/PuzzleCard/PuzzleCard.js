import './PuzzleCard.css';
import PropTypes from 'prop-types';

export default function PuzzleCard(props) {
  const puzzle = props.puzzle;
  const difficulty_dict = { 
    0.2:'Warmup', 
    0.3:'Beginner', 
    0.4:'Easy', 
    0.5:'Intermediate', 
    0.6:'Advanced', 
    0.7:'Expert', 
    0.8:'Master', 
  };
  return (
    <div
      className="puzzle-card"
      data-testid="puzzle-card"
      onClick={() => props.onClick(puzzle.puzzle_id)}
    >
      <div className="main-info">
        <div className="title">Puzzle {puzzle.puzzle_id}</div>
        <div className="status">{puzzle.completed ? "Completed" : "In Progress"}</div>
      </div>
      <div className="details">
        <div className="detail">Difficulty: {difficulty_dict[puzzle.difficulty]}</div>
        <div className="detail">Point Value: {puzzle.point_value}</div>
      </div>
    </div>
  );
}

PuzzleCard.defaultProps = {
  puzzle: null,
  onClick: null,
};

PuzzleCard.propTypes = {
  puzzle: PropTypes.shape({
    puzzle_id: PropTypes.number.isRequired,
    difficulty: PropTypes.number.isRequired,
    completed: PropTypes.bool.isRequired,
    point_value: PropTypes.number.isRequired,
    pieces: PropTypes.arrayOf(PropTypes.shape({
      x_coordinate: PropTypes.number.isRequired,
      y_coordinate: PropTypes.number.isRequired,
      static_piece: PropTypes.bool.isRequired,
      value: PropTypes.number,
    })),
    players: PropTypes.arrayOf(PropTypes.shape({
      id: PropTypes.number.isRequired,
      first_name: PropTypes.string.isRequired,
      last_name: PropTypes.string.isRequired,
      email: PropTypes.string.isRequired,
    })),
  }),
  onClick: PropTypes.func,
};
