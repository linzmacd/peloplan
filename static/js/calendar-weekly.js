
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
  'tread bootcamp': 'blue',
  'bike bootcamp': 'red',
  caesar: 'lightcoral',
  'caesar_bootcamp': 'lightcoral'
}

const completedBG = {
  true: 'white',
  false: 'lightgray'
}

const initialDate =  document.querySelector('#initial-date').value;

document.addEventListener('DOMContentLoaded', function() {
  var calendarEl = document.getElementById('calendar');
  var calendar = new FullCalendar.Calendar(calendarEl, {
    height: 300,
    initialView: 'dayGridWeek',
    headerToolbar: {
      left: 'title',
      center: '',
      right: 'today prev,next'
    },
    initialDate: initialDate,
    timeZone: 'local',
    dateClick: function(info) {
      const workout_date = info.dateStr;
      const url = `/${workout_date}/discipline-selection`
      window.location.href = url;
    },
    eventOrder: 'order',
    eventClick: function(info) {
      info.jsEvent.preventDefault();
      const date = info.event.start;
      document.querySelector('#modal-workout-date').value = date.toISOString().substr(0,10);
      document.querySelector('#modal-workout-order').value  = info.event.extendedProps.order;
      document.querySelector('#modal-discipline').value  = info.event.extendedProps.discipline;
      document.querySelector('#modal-sched-id').value = info.event.id;
      document.querySelector('#modal-url').value = info.event.url;
      if (info.event.extendedProps.completed == true) {
        window.open(info.event.url)
      } else if (info.event.title.toLowerCase() == info.event.extendedProps.discipline) {
        document.querySelector('#generic-modal-title').innerText = info.event.title + ' Workout';
        let genericModal = new bootstrap.Modal(document.getElementById('generic-modal'));
        genericModal.show();
      } else {
        document.querySelector('#specific-modal-title').innerText = info.event.title;
        let specificModal = new bootstrap.Modal(document.getElementById('specific-modal'));
        specificModal.show();
      };
    }
  });
  fetch('/peloplan/schedule')
    .then((response) => response.json())
    .then((schedule) => {
      for (const workout of schedule) {
        const completed = workout['completed']
        console.log(workout['title'])
        console.log(completed)
        const workoutDate = new Date(new Date(workout['date']))
        const todayDate = new Date(new Date().setHours(-8, 0, 0, 0));
        const bygone = (workoutDate < todayDate);
        const disciplineColor = colors[workout['discipline']]
        const background = {
          true: 'lightgray',
          false: colors[workout['discipline']] 
        }
        const font = {
          true: 'white',
          false: colors[workout['discipline']]
        }
        const event = {
          id: workout['id'],
          start: workout['date'],
          order: workout['order'],
          discipline: workout['discipline'],
          title: workout['title'],
          instructor: workout['instructor'],
          url: workout['url'],
          backgroundColor: completed ? 'white' : background[bygone],
          borderColor: completed ? disciplineColor : font[bygone],
          textColor: completed ? disciplineColor : 'white',
          };
        calendar.addEvent(event);
      };
      calendar.render();
    });
  });
