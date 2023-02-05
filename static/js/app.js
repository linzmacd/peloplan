
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
  const workout_date = document.querySelector('#modal-workout-date').value
  const sched_order = document.querySelector('#modal-workout-order').value
  const discipline = document.querySelector('.disciplines .selected').value
  fetch(`/add_generic/${workout_date}/${sched_order}/${discipline}`)
  .then(location.reload())
});

const selectWorkoutButton = document.querySelector('#select-workout');
selectWorkoutButton.addEventListener('click', () => {
  const workout_date = document.querySelector('#modal-workout-date').value
  const sched_order = document.querySelector('#modal-workout-order').value
  const discipline = document.querySelector('.selected').value
  const url = `/workout-selection/${workout_date}/${sched_order}/${discipline}`
  window.location.href = url
});

// Generic Workout & Specific Workout Modals
const upButtons = document.querySelectorAll('.modal-up');
for (const upButton of upButtons) {
  upButton.addEventListener('click', (event) => {
    const sched_id = document.querySelector('#modal-sched-id').value;
    fetch(`/move-up/${sched_id}`)
      .then(location.reload())
  });
};

const downButtons = document.querySelectorAll('.modal-down');
for (const downButton of downButtons) {
  downButton.addEventListener('click', (event) => {
    const sched_id = document.querySelector('#modal-sched-id').value;
    fetch(`/move-down/${sched_id}`)
      .then(location.reload())
  });
};

const deleteButtons = document.querySelectorAll('.modal-delete');
for (const deleteButton of deleteButtons) {
  deleteButton.addEventListener('click', (event) => {
    const sched_id = document.querySelector('#modal-sched-id').value;
    fetch(`/delete/${sched_id}`)
      .then(location.reload())
  });
};

document.querySelector('#gen-select-class').addEventListener('click', (event) => {
  const workout_date = document.querySelector('#modal-workout-date').value;
  const order = document.querySelector('#modal-workout-order').value;
  const discipline = document.querySelector('#modal-discipline').value;
  const url = `/workout-selection/${workout_date}/${order}/${discipline}`
  window.location.href = url;
});

document.querySelector('#spec-stack-add').addEventListener('click', (event) => {
  const url = document.querySelector('#modal-url').value;
  window.open(url)
  location.reload()
});
