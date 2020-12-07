import './CreatePuzzleModalContent.css';
import React from 'react';
import { withStyles } from '@material-ui/core/styles';
import Select from '@material-ui/core/Select';
import MenuItem from '@material-ui/core/MenuItem';
import TextField from '@material-ui/core/TextField';

function getModalStyle() {
  const top = 50;
  const left = 50;

  return {
    top: `${top}%`,
    left: `${left}%`,
    transform: `translate(-${top}%, -${left}%)`,
  };
}

const styles = (theme) => ({
  paper: {
    color: 'rgb(43, 43, 43)',
    display: 'flex',
    flexDirection: 'column',
    position: 'absolute',
    width: 400,
    backgroundColor: theme.palette.background.paper,
    border: '2px solid #000',
    boxShadow: theme.shadows[5],
    padding: theme.spacing(2, 4, 3),
  },
});

const difficultyValues = {
  'Warmup': 0.2,
  'Beginner': 0.3,
  'Easy': 0.4,
  'Intermediate': 0.5,
  'Advanced': 0.6,
  'Expert': 0.7,
  'Master': 0.8,
};

class CreatePuzzleModal extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      selectedDifficulty: difficultyValues['Easy'],
      additionalPlayers: [],
      modalStyle: getModalStyle(),
    };
  }

  render() {
    const { classes } = this.props;
    const { selectedDifficulty, modalStyle, additionalPlayers } = this.state;
    return (
      <div style={modalStyle} className={classes.paper} data-testid="create-modal">
        <h2 className="modal-title">Start new puzzle</h2>
        <div className="modal-section">
          <p className="label">
            Difficulty Level:
          </p>
          <Select
            value={selectedDifficulty}
            onChange={(event) => {
              this.setState({ selectedDifficulty: event.target.value });
            }}
            displayEmpty
            className="select-options"
            data-testid="difficulty-options"
          >
            {
              Object.entries(difficultyValues).map(([difficultyLabel, value]) => (
                <MenuItem key={difficultyLabel} value={value}>{difficultyLabel}</MenuItem>
              ))
            }
          </Select>
        </div>
        <div className="modal-section">
          <p className="label">Invite Friends: </p>
          <TextField
            id="standard-multiline-flexible"
            label="Emails"
            placeholder="joe@gmail.com, mary@gmail.com"
            onChange={event => {
              const additionalPlayers = event.target.value.replace(' ', '').split(',').filter(player => player);
              this.setState({ additionalPlayers });
            }}
            style={{ width: 255, marginLeft: '29px' }}
            error={Boolean(additionalPlayers.length && additionalPlayers.some(player => !/@.*\./.test(player)))}
          />
        </div>
        <button
          className="submit-new-game"
          data-testid="create-btn"
          onClick={() => this.props.createGame({ difficulty: selectedDifficulty, additionalPlayers })}>
          Create
        </button>
      </div>
    );
  }
};

export default withStyles(styles)(CreatePuzzleModal);