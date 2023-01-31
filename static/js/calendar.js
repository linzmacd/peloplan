
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
      for (const key in schedule) {
        const completed = schedule[key]['completed'];
        const workoutDate = new Date(new Date(schedule[key]['date']))
        const todayDate = new Date(new Date().setHours(-8, 0, 0, 0));
        const bygone = (workoutDate < todayDate);
        console.log(schedule[key]['title'])
        console.log(workoutDate)
        console.log(todayDate)
        // console.log(bygone)
        // const completedFC = {
        //   true: colors[schedule[key]['discipline']],
        //   false: 'white'
        // }
        const disciplineColor = colors[schedule[key]['discipline']]
        const background = {
          true: "lightgray",
          false: colors[schedule[key]['discipline']] 
        }
        const font = {
          true: 'white',
          false: colors[schedule[key]['discipline']]
        }
        const event = {
          start: schedule[key]['date'],
          order: schedule[key]['order'],
          discipline: schedule[key]['discipline'],
          title: schedule[key]['title'],
          instructor: schedule[key]['instructor'],
          url: schedule[key]['url'],
          // backgroundColor: bygone ? completedBG[completed] : colors[schedule[key]['discipline']],
          // borderColor: bygone ? completedFC[completed] : 'white',
          // textColor: bygone ? completedFC[completed] : 'white',
          backgroundColor: completed ? 'white' : background[bygone],
          borderColor: completed ? disciplineColor : font[bygone],
          textColor: completed ? disciplineColor : 'white',
          };
        calendar.addEvent(event);
      };
      calendar.render();
    });
  });
