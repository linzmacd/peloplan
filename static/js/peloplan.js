
document.querySelector('a.nav-link.page-monthly').classList.add('active');

const colors = {
  strength: 'rgba(0, 0, 0, 1)',
  yoga: 'rgba(128, 0, 128, 1)',
  meditation: 'rgba(0, 128, 0, 1)',
  cardio: 'rgba(218, 165, 32, 1)',
  stretching: 'rgba(0, 128, 0, .5)',
  cycling: 'rgba(255, 0, 0, 1)',
  outdoor: 'gray',
  running: 'rgba(0, 0, 255, 1)',
  walking: 'rgba(0, 0, 255, .66)',
  'bootcamp': 'rgba(0, 0, 255, .33)',
  'bike_bootcamp': 'rgba(255, 0, 0, .65)',
  caesar: 'rgba(240, 128, 128, 1)',
  'caesar_bootcamp': 'rgba(240, 128, 128, .75)'
};

const completedBG = {
  true: 'white',
  false: 'lightgray'
}

const initialDate =  document.querySelector('#initial-date').value;

document.addEventListener('DOMContentLoaded', function() {
  var calendarEl = document.getElementById('calendar');
  var calendar = new FullCalendar.Calendar(calendarEl, {
    height: 700,
    initialView: 'dayGridMonth',
    initialDate: initialDate,
    timeZone: 'local',
    fixedWeekCount: false,
    dayMaxEventRows: true,
    customButtons: {
      save: {
        text: 'Save',
        click: function() {
          let saveModal = new bootstrap.Modal(document.getElementById('save-modal'));
          saveModal.show();
        }
      },
      load: {
        text: 'Load',
        click: function() {
          let loadModal = new bootstrap.Modal(document.getElementById('load-modal'));
          loadModal.show();
        }
      },
      delete: {
        text: 'Delete',
        click: function() {
          let deleteRangeModal = new bootstrap.Modal(document.getElementById('delete-range-modal'));
          deleteRangeModal.show();
        }
      }
    },
    headerToolbar: {
      left: 'save load delete', // 'dayGridMonth dayGridWeek listWeek',
      center: 'title',
      right: 'today prev,next'
    },
    dateClick: function(info) {
      const workout_date = document.querySelector('#modal-workout-date').value = info.dateStr;
      fetch(`/get-order/${workout_date}`)
        .then((response) => response.json())
        .then((order) => {
          const disciplineButtons = document.querySelectorAll('.disciplines .btn-primary');
          for (const disciplineButton of disciplineButtons) {
            disciplineButton.classList.remove('selected');
            disciplineButton.classList.remove('dimmed');
          };
          document.querySelector('#modal-workout-order').value = order;
        });
        let disciplinesModal = new bootstrap.Modal(document.getElementById('disciplines-modal'));
        disciplinesModal.show();
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
      } else if (info.event.title.toLowerCase() == info.event.extendedProps.displayDiscipline) {
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
      const completed = workout.completed;
      const workoutDate = new Date(new Date(workout.date));
      const todayDate = new Date(new Date().setHours(-8, 0, 0, 0));
      const bygone = (workoutDate < todayDate);
      const disciplineColor = colors[workout.discipline];
      const background = {
        true: 'lightgray',
        false: colors[workout.discipline] 
      };
      const font = {
        true: 'white',
        false: colors[workout.discipline]
      };
      const event = {
        id: workout.id,
        start: workout.date,
        order: workout.order,
        discipline: workout.discipline,
        displayDiscipline: workout.display_discipline,
        title: workout.title,
        instructor: workout.instructor,
        completed: workout.completed,
        url: workout.url,
        backgroundColor: completed ? 'white' : background[bygone],
        borderColor: completed ? disciplineColor : font[bygone],
        textColor: completed ? disciplineColor : 'white',
        };
      calendar.addEvent(event);
    };
    calendar.render();
  });
});


// Disciplines Modal
const disciplineButtons = document.querySelectorAll('.disciplines .btn-primary');
for (const disciplineButton of disciplineButtons) {
  disciplineButton.addEventListener('click', () => {
    const selectedButtons = document.querySelectorAll('.disciplines .btn-primary');
    for (const selectedButton of selectedButtons) {
      selectedButton.classList.remove('selected');
      selectedButton.classList.add('dimmed');
    };
    disciplineButton.classList.add('selected');
    disciplineButton.classList.remove('dimmed');
    document.querySelector('#add-discipline').removeAttribute('disabled');
    document.querySelector('#select-workout').removeAttribute('disabled');
  });
};

const addDisciplineButton = document.querySelector('#add-discipline');
addDisciplineButton.addEventListener('click', () => {
  const workout_date = document.querySelector('#modal-workout-date').value;
  const sched_order = document.querySelector('#modal-workout-order').value;
  const discipline = document.querySelector('.disciplines .selected').value;
  fetch(`/add-generic/${workout_date}/${sched_order}/${discipline}`)
  .then(() => {
    document.querySelector('#initial-date').value = workout_date;
    window.location.href = '/peloplan';
  })
});

const selectWorkoutButton = document.querySelector('#select-workout');
selectWorkoutButton.addEventListener('click', () => {
  const workout_date = document.querySelector('#modal-workout-date').value;
  const sched_order = document.querySelector('#modal-workout-order').value;
  const discipline = document.querySelector('.selected').value
  const url = `/workout-selection/${workout_date}/${sched_order}/${discipline}`
  window.location.href = url
});

// Generic Workout & Specific Workout Modals
const upButtons = document.querySelectorAll('.modal-up');
for (const upButton of upButtons) {
  upButton.addEventListener('click', (event) => {
    event.preventDefault();
    const workout_date = document.querySelector('#modal-workout-date').value;
    const sched_id = document.querySelector('#modal-sched-id').value;
    fetch(`/move-up/${workout_date}/${sched_id}`)
    .then(window.location.href = '/redirect/peloplan')
  });
};

const downButtons = document.querySelectorAll('.modal-down');
for (const downButton of downButtons) {
  downButton.addEventListener('click', (event) => {
    event.preventDefault();
    const workout_date = document.querySelector('#modal-workout-date').value;
    const sched_id = document.querySelector('#modal-sched-id').value;
    fetch(`/move-down/${workout_date}/${sched_id}`)
    .then(window.location.href = '/redirect/peloplan')
  });
};

const deleteButtons = document.querySelectorAll('.modal-delete');
for (const deleteButton of deleteButtons) {
  deleteButton.addEventListener('click', (event) => {
    event.preventDefault();
    const workout_date = document.querySelector('#modal-workout-date').value;
    const sched_id = document.querySelector('#modal-sched-id').value;
    fetch(`/delete/${workout_date}/${sched_id}`)
    .then(window.location.href = '/redirect/peloplan')
  });
};

document.querySelector('#gen-select-class').addEventListener('click', (event) => {
  event.preventDefault();
  const workout_date = document.querySelector('#modal-workout-date').value;
  const order = document.querySelector('#modal-workout-order').value;
  const discipline = document.querySelector('#modal-discipline').value;
  const url = `/workout-selection/${workout_date}/${order}/${discipline}`
  window.location.href = url;
});

document.querySelector('#spec-change').addEventListener('click', (event) => {
  event.preventDefault();
  const workout_date = document.querySelector('#modal-workout-date').value;
  const order = document.querySelector('#modal-workout-order').value;
  const discipline = document.querySelector('#modal-discipline').value;
  const url = `/workout-selection/${workout_date}/${order}/${discipline}`
  window.location.href = url;
});

document.querySelector('#spec-stack-add').addEventListener('click', (event) => {
  event.preventDefault();
  const url = document.querySelector('#modal-url').value;
  window.open(url)
  location.reload()
});

// Save Schedule Modal
document.querySelector('#save-schedule').addEventListener('click', (event) => {
  event.preventDefault();
  let visibility = 'private';
  if (document.querySelector('#save-public').checked) {
    visibility = 'public';
  }
  const formInputs = {
    visibility: visibility,
    schedName: document.querySelector('#save-sched-name').value,
    startDate: document.querySelector('#save-start-date').value,
    endDate: document.querySelector('#save-end-date').value,
    saveType: document.querySelector('#save-type').value,
    description: document.querySelector('#save-description').value
  }
  fetch('/save-schedule', {
    method: 'POST',
    body: JSON.stringify(formInputs),
    headers: {
      'Content-Type': 'application/json',
    },
  })
  .then(location.reload())
});

// Load Schedule Modal
document.querySelector('#load-schedule').addEventListener('click', (event) => {
  event.preventDefault();
  const formInputs = {
    storageId: document.querySelector('#load-storage-id').value,
    startDate: document.querySelector('#load-start-date').value,
  }
  fetch('/load-schedule', {
    method: 'POST',
    body: JSON.stringify(formInputs),
    headers: {
      'Content-Type': 'application/json',
    },
  })
  .then(location.reload())
});

// Delete Range Modal
document.querySelector('#delete-range').addEventListener('click', (event) => {
  event.preventDefault();
  const formInputs = {
    startDate: document.querySelector('#delete-start-date').value,
    endDate: document.querySelector('#delete-end-date').value,
  }
  fetch('/delete-range', {
    method: 'POST',
    body: JSON.stringify(formInputs),
    headers: {
      'Content-Type': 'application/json',
    },
  })
  .then(location.reload())
});

