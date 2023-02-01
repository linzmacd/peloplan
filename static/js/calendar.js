
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
    initialView: 'dayGridMonth',
    initialDate: initialDate,
    timeZone: 'local',
    fixedWeekCount: false,
    dayMaxEventRows: true,
    dateClick: function(info) {
      const workout_date = info.dateStr;
      const url = `/${workout_date}/discipline-selection`
      window.location.href = url;
    },
    eventOrder: 'order',
    eventClick: function(info) {
      info.jsEvent.preventDefault();
      if (info.event.url != 0) {
        window.open(info.event.url);
      } else {
        const date = info.event.start;
        const workout_date = date.toISOString().substr(0,10);
        const order = info.event.extendedProps.order;
        const discipline = info.event.extendedProps.discipline;
        const url = `/${workout_date}/${order}/${discipline}/workout-selection`
        window.location.href = url;
       }
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
        // console.log(workout['title'])
        // console.log(workoutDate)
        // console.log(todayDate)
        // console.log(bygone)
        const disciplineColor = colors[workout['discipline']]
        const background = {
          true: "lightgray",
          false: colors[workout['discipline']] 
        }
        const font = {
          true: 'white',
          false: colors[workout['discipline']]
        }
        const event = {
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
