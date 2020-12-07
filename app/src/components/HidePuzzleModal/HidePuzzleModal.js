import './HidePuzzleModal.css';
import React from 'react';
import { withStyles } from '@material-ui/core/styles';

function getModalStyle() {
    const top = 50;
    const left = 50;
  
    return {
      top: `${top}%`,
      left: `${left}%`,
      transform: `translate(-${top}%, -${left}%)`,
    };
  }
  
const styles = theme => ({
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

class HidePuzzleModal extends React.Component {
    constructor(props) {
      super(props);
      this.state = {
        modalStyle: getModalStyle(),
      };
    }

    render() {
      const {classes} = this.props;
      return (
          <div style={this.state.modalStyle} className={classes.paper} data-testid="hide-modal">
            <h2 className="modal-title">Delete puzzle {this.props.puzzleId}</h2>
            <div className="modal-section">
              <p>
                Are you sure you want to delete this puzzle?
                This action cannot be undone
              </p>
            </div>
          <button className="btn" data-testid="yes-btn" onClick={this.props.hidePuzzle}>Yes</button>
          <button className="btn" data-testid="no-btn" onClick={() => this.props.setHideModalStatus(false)}>No</button>
        </div>
      );
    }
};

export default withStyles(styles)(HidePuzzleModal);