
const addWorkoutButtons = document.querySelectorAll('.add-workout');
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

const durationFilter = document.querySelector('#filter-duration');
const instructorFilter = document.querySelector('#filter-instructor');
const categoryFilter = document.querySelector('#filter-category');
const bookmarkedFilter = document.querySelector('#filter-bookmarked');
const completedFilter = document.querySelector('#filter-completed');
const sortbyFilter = document.querySelector('#filter-sortby');

const filterButtons = [durationFilter, instructorFilter, categoryFilter, 
      bookmarkedFilter, completedFilter, sortbyFilter]

for (const filterButton of filterButtons) {
  filterButton.addEventListener('change', (event) => {
    event.preventDefault;
    const workout_date = document.querySelector('#workout-date').value;
    const sched_order = document.querySelector('#sched-order').value;
    const discipline = document.querySelector('#filter-discipline').value
    const queryFilters = {
      discipline: document.querySelector('#filter-discipline').value,
      duration: document.querySelector('#filter-duration').value,
      instructor: document.querySelector('#filter-instructor').value,
      category: document.querySelector('#filter-category').value,
      bookmarked: document.querySelector('#filter-bookmarked').checked,
      completed: document.querySelector('#filter-completed').checked,
      sortby: document.querySelector('#filter-sortby').value
    };
    const url = `/workout-selection/${workout_date}/${sched_order}/${discipline}`
    fetch(url, {
      method: 'POST',
      body: JSON.stringify(queryFilters),
      headers: {
        'Content-Type': 'application/json',
      },
    })
    .then((response) => response.json())
    .then((results) => {
      const instructors = {}
      for (const instructor of results['instructors']) {
        instructors[instructor['id']] = instructor['name']
      };
      document.querySelector('#query-results').innerHTML = ''      
      for (const result of results['data']) {
        document.querySelector('#query-results').insertAdjacentHTML('beforeend', `
        <div class='row align-items-center' style='padding: 5px; margin: 5px; border: 1px solid black'>
          <div class='col-4'>
            <img src="${result['image_url']}" height=170px>
          </div>
          <div class='col-5'>
            <h3>${result['title']}</h3>
            ${instructors[result['instructor_id']]}<br>
            ${result['description']}<br>
            Total Riders: ${result['total_workouts'].toLocaleString('en-US')}<br>
            Rating: ${(result['overall_rating_avg']*100).toFixed(2)}%
            (${result['overall_rating_count'].toLocaleString('en-US')} votes)<br>
            Difficulty: ${result['difficulty_rating_avg'].toFixed(2)}
            (${result['difficulty_rating_count'].toLocaleString('en-US')} votes)<br>
          </div>
          <div class='col-2'>
            <button class='add-workout' value="${result['id']}"> Add to Calendar </button>
          </div>
        </div>
        `);
      };
      const addWorkoutButtons = document.querySelectorAll('.add-workout');
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
    });
  });
};






