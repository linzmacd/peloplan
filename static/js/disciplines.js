
const disciplineButtons = document.querySelectorAll('.btn-primary');
for (const disciplineButton of disciplineButtons) {
  disciplineButton.addEventListener('click', () => {
    const selectedButtons = document.querySelectorAll('.btn-primary');
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

const workout_date = document.querySelector('#workout-date').value
const sched_order = document.querySelector('#sched-order').value

const addDisciplineButton = document.querySelector('#add-discipline');
addDisciplineButton.addEventListener('click', () => {
  // const workout_date = document.querySelector('#workout-date').value
  // const sched_order = document.querySelector('#sched-order').value
  const discipline = document.querySelector('.selected').value
  const url = `/${workout_date}/${sched_order}/${discipline}`
  window.location.href = url
});

const selectWorkoutButton = document.querySelector('#select-workout');
selectWorkoutButton.addEventListener('click', () => {
  // const workout_date = document.querySelector('#workout-date').value
  // const sched_order = document.querySelector('#sched-order').value
  const discipline = document.querySelector('.selected').value
  const url = `/${workout_date}/${sched_order}/${discipline}/workout-selection`
  window.location.href = url
});