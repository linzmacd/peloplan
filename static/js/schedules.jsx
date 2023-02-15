
// style={{paddingBlock: 5, margin: 5, borderBlock: 1, borderBlockStyle: solid, borderBlockColor: black}}

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
                storageId={schedule.storage_id} />
    );
  }
  return (
    <div>{scheduleList}</div>
  )
}

function Schedule(props) {
  const [rating, setRating] = React.useState(props.rating)

  let schedType = '';
  if (props.schedType == 'specific') {
    schedType = 'Class Schedule';
  }
  if (props.schedType == 'generic') {
    schedType = 'Schedule Template';
  }
  const storageId = props.storageId
  function previewSchedule() {
    const url = `/preview-schedule/${storageId}`;
    window.open(url)
  }
  function loadSchedule() {
    document.querySelector('#modal-storage-id').value = storageId;  
    let loadModal = new bootstrap.Modal(document.getElementById('load-modal'));
    loadModal.show();
  }
  function deleteSchedule() {
    document.querySelector('#modal-storage-id').value = storageId;  
    let deleteModal = new bootstrap.Modal(document.getElementById('delete-modal'));
    deleteModal.show();
  }
  function likeSchedule() {
    fetch(`/schedule-like/${storageId}`)
    .then((response) => response.json())
    .then((newRating) => {
      console.log(newRating)
      setRating(newRating.rating);
    });
  }
  function dislikeSchedule() {
    fetch(`/schedule-dislike/${storageId}`) 
    .then((response) => response.json())
    .then((newRating) => {
      console.log(newRating)
      setRating(newRating.rating);
    });
  }
  return (
    <div className='col-3 content-box' align='left'>
      <h4>{props.schedName}</h4>
      <p>BY {props.creator.toUpperCase()}</p>
      <p>"{props.description}"</p>
      <p>{schedType}<br/>
      Length: {props.length} days <br/>
      Workouts: {props.count} <br/>
      Rating: {(rating*100).toFixed(2)}% </p>
      <button onClick={previewSchedule}>Preview</button>
      <button onClick={loadSchedule}>Load</button>
      <button onClick={deleteSchedule}>Delete</button>
      <button onClick={likeSchedule}><i className='bi bi-hand-thumbs-up'></i></button>
      <button onClick={dislikeSchedule}><i className='bi bi-hand-thumbs-down'></i></button>
    </div>
  );
}

fetch('/get-public-schedules')
.then((response) => response.json())
.then((schedules) => {
  console.log(schedules);
  ReactDOM.render(<ScheduleList schedules={schedules}/>, document.querySelector('#root'));
})
