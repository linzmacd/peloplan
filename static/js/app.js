
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
  'bike bootcamp': 'red'
}

document.addEventListener('DOMContentLoaded', function() {
  var calendarEl = document.getElementById('calendar');
  var calendar = new FullCalendar.Calendar(calendarEl, {
    initialView: 'dayGridMonth',
    timeZone: 'local',
    eventOrder: 'order',
    eventClick: function(info) {
      info.jsEvent.preventDefault();
      if (info.event.url != 0) {
        window.open(info.event.url);
      } else { 
        const date = info.event.start;
        const workout_date = date.toISOString().substr(0,10);
        const discipline = info.event.title.toLowerCase();
        const url = `/${workout_date}/${discipline}/workout-selection`
        window.location.href = url;
       }
    },
    dateClick: function(info) {
      const workout_date = info.dateStr;
      const url = `/${workout_date}/discipline-selection`
      window.location.href = url;
    }
  });
  fetch('/peloplan/schedule')
    .then((response) => response.json())
    .then((schedule) => {
      for (const key in schedule) {
        const completed = schedule[key]['completed'];
        const event = {
          start: schedule[key]['date'],
          order: schedule[key]['order'],
          discipline: schedule[key]['discipline'],
          title: schedule[key]['title'],
          instructor: schedule[key]['instructor'],
          url: schedule[key]['url'],
          backgroundColor: completed ? 'white' : colors[schedule[key]['discipline']],
          borderColor: colors[schedule[key]['discipline']],
          textColor: completed ? colors[schedule[key]['discipline']] : 'white',
          };
        calendar.addEvent(event);
      };
      calendar.render();
    });
  });
