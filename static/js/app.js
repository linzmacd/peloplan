// const schedule = []
// fetch('/peloplan/schedule')
//   .then((response) => response.json())
//   .then((schedule) => {
//     for (const workout in schedule) {
//       schedule.append({
//         id: workout.schedule_id,
//         title: workout.discipline,
//         body: workout.workout_id,
//         date: workout.sched_date,
//         location: workout.sched_order,
//       });
//     };
//   });

//   console.log(schedule)

// for (const workout in schedule) {

// }

const colors = {
  strength: 'black',
  yoga: 'green',
  meditation: 'green',
  cardio: 'goldenrod',
  stretching: 'green',
  cycling: 'red',
  outdoor: 'blue',
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
      if (info.event.url) {
        window.open(info.event.url);
      } else { 
        const discipline = info.event.discipline; // DO OTHER STUFF HERE
       }
    },
    dateClick: function(info) {
      alert('Clicked on: ' + info.dateStr);
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


      // FOR LOOP:
      // calendar.addEvent({
      //   title: 'new event',
      //   start: '2023-02-25'
      // });
// document.addEventListener('DOMContentLoaded', function() {
//   var calendarEl = document.getElementById('calendar');
//   var calendar = new FullCalendar.Calendar(calendarEl, {
//     initialView: 'dayGridMonth',
//     events: [list of events],
//     dateClick: function(info) {
//       alert('Clicked on: ' + info.dateStr);
//     }
//   });
//   calendar.render();
  
      // events: [
    //   {% for workout in schedule %}
    //   { 
    //     id: '{{ workout.schedule_id }}',
    //     title: '{{ workout.discipline }}',
    //     body: '{{ workout.workout_id }}',
    //     date: '{{ workout.sched_date}}',
    //     location: '{{ workout.sched_order }}',
    //   },
    //   {% endfor %}
    // ],
  
//   calendar.on('dateClick', function(info) {
//     const workout_date = info.dateStr;





//     // document.querySelector('#discipline-selection').style.display = '';
//     // let params = 'width=280,height=600,left=600,top=200';
//     // let newWindow = open('/disciplines', 'Disciplines', params);

//     // newWindow.onload = function() {
//     //   let html = `<div style='font-size:30px'>Welcome to W3Docs!</div>`;
//     //   newWindow.document.body.insertAdjacentHTML('afterbegin', html);}
    
// });
// });



{/* <script>
document.addEventListener('DOMContentLoaded', function() {
  var calendarEl = document.getElementById('calendar');
  var calendar = new FullCalendar.Calendar(calendarEl, {
    initialView: 'dayGridMonth',
    // events: [
    //   {% for workout in schedule %}
    //   { 
    //     id: '{{ workout.schedule_id }}',
    //     title: '{{ workout.discipline }}',
    //     body: '{{ workout.workout_id }}',
    //     date: '{{ workout.sched_date}}',
    //     location: '{{ workout.sched_order }}',
    //   },
    //   {% endfor %}
    // ],
    dateClick: function(info) {
      alert('Clicked on: ' + info.dateStr);
    }
  });
  calendar.render();
});
</script> */}

