import React, { useCallback, useMemo, useContext, useState, forwardRef } from 'react'
import CurrentUserContext from '../../context/CurrentUserContext';


async function getSolution({ accessToken, puzzleId, onSuccess }) {
  const requestOptions = {
    method: 'GET',
    headers: { Authorization: `Bearer ${accessToken}` },
  };
  const response = await fetch(`/puzzles/${puzzleId}/solution`, requestOptions)
  //const response = await Promise.resolve(getSolvedSolutionResponse());
  const json = await response.json();
  onSuccess(json);
}

export default function CheckSolutionBtn(props) {
  const { accessToken, userEmail } = useContext(CurrentUserContext);
  const [solved, setSolved] = useState(props.solved);
  const [checked, setChecked] = useState(false);

  if (!props.gridState) {
    return null;
  }

  return(
    props.solved ? 
    <h2 className="puzzleStatusText">You win!</h2> :
    <div>
      <button className="checkSolutionBtn" onClick={() => {
        getSolution({
          accessToken,
          puzzleId: props.puzzleId,
          onSuccess: json => setSolved(json.discrepancy.length === 0),
        })
        setChecked(true)
      }}>
        Check Answer
      </button>
      {checked ? (
        solved ? 
          <h2 className="puzzleStatusText">You win!</h2> : 
          <h2 className="puzzleStatusText">Something's Not Right...</h2>
        ) : null}
    </div>
  );
}