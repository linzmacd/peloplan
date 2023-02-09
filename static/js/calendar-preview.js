
const colors = {
  strength: 'black',
  yoga: 'purple',
  meditation: 'green',
  cardio: 'goldenrod',
  stretching: 'green',
  cycling: 'red',
  outdoor: 'gray',
  running: 'blue',
  walking: 'blue',
  'bootcamp': 'blue',
  'bike_bootcamp': 'red',
  caesar: 'lightcoral',
  'caesar_bootcamp': 'lightcoral'
}

const initialDate =  document.querySelector('#initial-date').value;
const storageId = document.querySelector('#storage-id').value
const url = `/preview-schedule/${storageId}/data`;

document.addEventListener('DOMContentLoaded', function() {
  var calendarEl = document.getElementById('calendar');
  var calendar = new FullCalendar.Calendar(calendarEl, {
    height: 700,
    initialView: 'dayGridMonth',
    initialDate: initialDate,
    headerToolbar: {
      left: '', 
      center: 'title',
      right: 'dayGridWeek today prev,next'
    },
    timeZone: 'local',
    fixedWeekCount: false,
    dayMaxEventRows: true,
    eventOrder: 'order',
    eventClick: function(info) {
      info.jsEvent.preventDefault();
      if (info.event.url) {
        window.open(info.event.url)
      };
    }
  });
  fetch(url)
    .then((response) => response.json())
    .then((schedule) => {
      console.log(schedule)
      for (const workout of schedule) {
        const disciplineColor = colors[workout['discipline']]
        const event = {
          start: workout.sched_date,
          order: workout.sched_order,
          discipline: workout.discipline,
          title: workout.title,
          url: workout.url,
          backgroundColor: disciplineColor,
          borderColor: disciplineColor,
          textColor: 'white',
          };
        calendar.addEvent(event);
      };
      calendar.render();
    });
});