
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
    notes: document.querySelector('#save-notes').value
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

