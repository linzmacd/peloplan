
document.querySelector('a.nav-link.page-schedules').classList.add('active');

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
  const votesTooltip = `${(rating*100).toFixed(0)}% with ${votes} votes`

  let schedType = '';
  let schedBox = '';
  let id = '';
  let schedButtons = '';
  let schedDetails = '';
  if (props.schedType == 'specific') {
    schedType = 'Classes';
    schedBox = 'col-3 schedule-box classes'
    id = 'sched-type-classes';
    schedButtons = 'column sched-buttons-classes';
    schedDetails = 'sched-details-classes';
  }
  if (props.schedType == 'generic') {
    schedType = 'Template';
    schedBox = 'col-3 schedule-box template'
    id = 'sched-type-template';
    schedButtons = 'column sched-buttons-template';
    schedDetails = 'sched-details-template';
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
      setRating(newRating.rating);
      setVotes(newRating.votes);
      setUserRating(newRating.user_rating);
    });
  }
  function dislikeSchedule() {
    fetch(`/schedule-dislike/${storageId}`) 
    .then((response) => response.json())
    .then((newRating) => {
      setRating(newRating.rating);
      setVotes(newRating.votes);
      setUserRating(newRating.user_rating)
    });
  }
  return (
    <div className={schedBox}>
      <div className='row justify-content-center'>
        <div className='col-4' id={id}>
          {schedType.toUpperCase()}
        </div>  
      </div>
      <div className='row sched-content'>
        <div className='col-9'>
          <h4 className='sched-title'>{props.schedName}</h4>
          <p className='sched-creator'>by {props.creator}</p>
          <p>"{props.description}"</p>
          <br></br>
        </div>
        <div className='col-3'>
          <div className='row sched-details'>
            <span className={schedDetails}>{props.count}</span><br/>
            <span className='sched-details-sm'>workouts</span><br/>
            <span className={schedDetails}>{props.length}</span><br/>
            <span className='sched-details-sm'>day(s)</span>
          </div>
        </div>
      </div>
      <div className='row sched-button-box'>
        <div className={schedButtons}>
          <button title='Preview' onClick={previewSchedule}><i class="bi bi-zoom-in"></i></button>
          <button title='Load' onClick={loadSchedule}><i class="bi bi-calendar-week"></i></button>
          {'  '}<span title={votesTooltip}>{(rating*100).toFixed(0)}%</span>{'  '}
          <button title='Like' onClick={likeSchedule} id='thumb-up'><i className={thumbsUp}></i></button>
          <button title='Dislike' onClick={dislikeSchedule} id='thumb-down'><i className={thumbsDown}></i></button>
        </div>
      </div>
    </div>
  );
}

// Rendering Page
fetch('/get-public-schedules')
.then((response) => response.json())
.then((schedules) => {
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