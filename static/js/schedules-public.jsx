// Schedule List Component
function ScheduleList(props) {
  const scheduleList = [];
  for (const schedule of props.schedules) {
    scheduleList.push(
      <Schedule key={schedule.storage_id}
                schedName={schedule.sched_name}
                creator={schedule.creator}
                description={schedule.description}
                schedType={schedule.sched_type}
                length={schedule.length}
                count={schedule.count}
                rating={schedule.rating}
                votes={schedule.votes}
                userRating={schedule.user_rating}
                storageId={schedule.storage_id} />
    );
  }
  return (
    <div id='schedule-parent-box'>{scheduleList}</div>
  )
}

// Schedule Component
function Schedule(props) {
  const [rating, setRating] = React.useState(props.rating);
  const [votes, setVotes] = React.useState(props.votes)
  const [userRating, setUserRating] = React.useState(props.userRating);
  const storageId = props.storageId;
  const schedName = props.schedName;

  let schedType = '';
  if (props.schedType == 'specific') {
    schedType = 'Class Schedule';
  }
  if (props.schedType == 'generic') {
    schedType = 'Schedule Template';
  }
  let thumbsUp = 'bi bi-hand-thumbs-up';
  let thumbsDown = 'bi bi-hand-thumbs-down';
  if (userRating === 1) {
    thumbsUp = 'bi bi-hand-thumbs-up-fill';
  } else if (userRating === 0) {
    thumbsDown = 'bi bi-hand-thumbs-down-fill';
  }
  function previewSchedule() {
    const url = `/preview-schedule/${storageId}`;
    window.open(url)
  }
  function loadSchedule() {
    document.querySelector('#load-modal-title').innerText = schedName;  
    document.querySelector('#load-modal-title').dataset.id = storageId;
    let loadModal = new bootstrap.Modal(document.getElementById('load-modal'));
    loadModal.show();
  }
  function likeSchedule() {
    fetch(`/schedule-like/${storageId}`)
    .then((response) => response.json())
    .then((newRating) => {
      console.log(newRating)
      setRating(newRating.rating);
      setVotes(newRating.votes);
      setUserRating(newRating.user_rating);
    });
  }
  function dislikeSchedule() {
    fetch(`/schedule-dislike/${storageId}`) 
    .then((response) => response.json())
    .then((newRating) => {
      console.log(newRating)
      setRating(newRating.rating);
      setVotes(newRating.votes);
      setUserRating(newRating.user_rating)
    });
  }
  return (
    <div className='col-3 content-box' align='left'>
      <h4>{props.schedName}</h4>
      <p>{schedType.toUpperCase()}<br/>
        by {props.creator}</p>
      <p>"{props.description}"</p>
      <p>Length: {props.length} days <br/>
      Workouts: {props.count} <br/>
      Rating: {(rating*100).toFixed(2)}% ({votes} votes)</p>
      <button onClick={previewSchedule}>Preview</button>
      <button onClick={loadSchedule}>Load</button>
      <button onClick={likeSchedule} id='thumb-up'><i className={thumbsUp}></i></button>
      <button onClick={dislikeSchedule} id='thumb-down'><i className={thumbsDown}></i></button>
    </div>
  );
}

// Rendering Page
fetch('/get-public-schedules')
.then((response) => response.json())
.then((schedules) => {
  console.log(schedules)
  ReactDOM.render(<ScheduleList schedules={schedules}/>, document.querySelector('#root'));
})

// Load Schedule Modal
document.querySelector('#load-schedule').addEventListener('click', (event) => {
  event.preventDefault();
  const formInputs = {
    storageId: document.querySelector('#load-modal-title').dataset.id,
    startDate: document.querySelector('#load-start-date').value,
  }
  fetch('/load-schedule', {
    method: 'POST',
    body: JSON.stringify(formInputs),
    headers: {
      'Content-Type': 'application/json',
    },
  })
  .then((response) => {
    window.location.href = '/peloplan'
  });
});