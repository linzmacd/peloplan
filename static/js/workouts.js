
const addWorkoutButtons = document.querySelectorAll('.add-workout');
console.log(addWorkoutButtons);
for (const addWorkoutButton of addWorkoutButtons) {
  addWorkoutButton.addEventListener('click', () => {
    const workout_date = document.querySelector('#workout-date').value
    const sched_order = document.querySelector('#sched-order').value
    const discipline = document.querySelector('#filter-discipline').value
    const workout_id = addWorkoutButton.value
    const url = `/${workout_date}/${sched_order}/${discipline}/${workout_id}`
    window.location.href = url
  });
};

// const applyFiltersButton = document.querySelector('#apply-filters');
// applyFiltersButton.addEventListener('click', (event) => {
//   event.preventDefault();
//   const formInputs = {
//     workout_date: document.querySelector('#workout-date').value,
//     discipline: document.querySelector('#filter-discipline').value,
//     duration: document.querySelector('#filter-duration').value,
//     instructor: document.querySelector('#filter-instructor').value,
//     category: document.querySelector('#filter-category').value,
//     bookmarked: document.querySelector('#filter-bookmarked').value,
//     completed: document.querySelector('#filter-completed').value,
//     sortby: document.querySelector('#filter-sortby').value
//   };
//   console.log(formInputs);
//   fetch('/<workout_date>/<discipline>/workout-selection', {
//     method: 'POST',
//     body: JSON.stringify(formInputs),
//     headers: {
//       'Content-Type': 'application/json',
//     },
//   })
//     .then((response) => response.json())
//     .then((responseJson) => {
//       alert(responseJson.status);
//     });
// });