
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
  const url = `/${workout_date}/${order}/${discipline}/workout-selection`
  window.location.href = url;
});

document.querySelector('#spec-stack-add').addEventListener('click', (event) => {
  const url = document.querySelector('#modal-url').value;
  window.open(url)
  location.reload()
});
