
const addWorkoutButtons = document.querySelectorAll('.add-workout');
for (const addWorkoutButton of addWorkoutButtons) {
  addWorkoutButton.addEventListener('click', () => {
    const workout_date = document.querySelector('#workout-date').value
    const sched_order = document.querySelector('#sched-order').value
    const discipline = document.querySelector('#filter-discipline').value
    const workout_id = addWorkoutButton.value
    const url = `/add-class/${workout_date}/${sched_order}/${discipline}/${workout_id}`
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
    event.preventDefault();
    const queryFilters = {
      discipline: document.querySelector('#filter-discipline').value,
      duration: document.querySelector('#filter-duration').value,
      instructor: document.querySelector('#filter-instructor').value,
      category: document.querySelector('#filter-category').value,
      bookmarked: document.querySelector('#filter-bookmarked').checked,
      completed: document.querySelector('#filter-completed').checked,
      sortby: document.querySelector('#filter-sortby').value,
    };
    const url = `/workout-selection/filter`
    fetch(url, {
      method: 'POST',
      body: JSON.stringify(queryFilters),
      headers: {
        'Content-Type': 'application/json',
      },
    })
    .then((response) => response.json())
    .then((results) => {
      document.querySelector('#filter-page').value = results.page;
      document.querySelector('#filter-page-max').value = results.page_count;
      const instructors = {}
      for (const instructor of results.instructors) {
        instructors[instructor.id] = instructor.name;
      };
      document.querySelector('#query-results').innerHTML = ''      
      for (const result of results.data) {
        document.querySelector('#query-results').insertAdjacentHTML('beforeend', `
        <div class='row workout-box'>
          <div class='col-4'>
            <img src="${result.image_url}" width=300px>
          </div>
          <div class='col-5 workout-details'>
            <div class='row workout-header'>
              <span id='workout-title'>${result.title}</span><br/>
              <span id='workout-inst'>${instructors[result.instructor_id]}</span><br/>
            </div>
            <span id='workout-desc'>${result.description}</span><br/>
          </div>
          <div class='col-2 workout-stats'>
            <span class='workout-stat'>${result.total_workouts.toLocaleString('en-US')}</span><br/>
            <span class='workout-text'>members</span><br/>
            <span class='workout-stat'>${(result.overall_rating_avg*100).toFixed(1)}% </span>
            <span class='workout-text-sm'>/${result.overall_rating_count.toLocaleString('en-US')}</span><br/>
            <span class='workout-text'>rating</span><br/>
            <span class='workout-stat'>${result.difficulty_rating_avg.toFixed(2)}</span>
            <span class='workout-text-sm'>/${result.difficulty_rating_count.toLocaleString('en-US')}</span><br/>
            <span class='workout-text'>difficulty</span><br/>
          </div>
          <div class='col-1'>
            <button class='add-workout' title='Add Workout' value=${result['id']}>
              <i class="bi bi-calendar-week"></i>
            </button>
          </div>
        </div>
        `);
      };
      const addWorkoutButtons = document.querySelectorAll('.add-workout');
      for (const addWorkoutButton of addWorkoutButtons) {
        addWorkoutButton.addEventListener('click', (event) => {
          event.preventDefault();
          const workout_date = document.querySelector('#workout-date').value
          const sched_order = document.querySelector('#sched-order').value
          const discipline = document.querySelector('#filter-discipline').value
          const workout_id = addWorkoutButton.value
          const url = `/add-class/${workout_date}/${sched_order}/${discipline}/${workout_id}`
          window.location.href = url
        });
      };
      if (results.page == (results.page_count - 1)) {
        document.querySelector('#next-page').setAttribute('disabled', '');
      };
    });
  });
};

const changePageButtons = document.querySelectorAll('.change-page')
for (const changePageButton of changePageButtons) {
  changePageButton.addEventListener('click', (event) => {
    event.preventDefault();
    document.querySelector('.outer-scroll').scrollTop = 0;
    const pageChange = changePageButton.value;
    const page = document.querySelector('#filter-page').value;
    const newPage = parseInt(page) + parseInt(pageChange);
    const queryFilters = {
      discipline: document.querySelector('#filter-discipline').value,
      duration: document.querySelector('#filter-duration').value,
      instructor: document.querySelector('#filter-instructor').value,
      category: document.querySelector('#filter-category').value,
      bookmarked: document.querySelector('#filter-bookmarked').checked,
      completed: document.querySelector('#filter-completed').checked,
      sortby: document.querySelector('#filter-sortby').value,
      page: newPage
    };
    const url = `/workout-selection/change-page`
    fetch(url, {
      method: 'POST',
      body: JSON.stringify(queryFilters),
      headers: {
        'Content-Type': 'application/json',
      },
    })
    .then((response) => response.json())
    .then((results) => {
      document.querySelector('#filter-page').value = results.page;
      document.querySelector('#filter-page-max').value = results.page_count;
      const instructors = {}
      for (const instructor of results.instructors) {
        instructors[instructor.id] = instructor.name;
      };
      document.querySelector('#query-results').innerHTML = '';
      for (const result of results.data) {
        document.querySelector('#query-results').insertAdjacentHTML('beforeend', `
        <div class='row workout-box'>
          <div class='col-4'>
            <img src="${result.image_url}" width=300px>
          </div>
          <div class='col-5 workout-details'>
            <div class='row workout-header'>
              <span id='workout-title'>${result.title}</span><br/>
              <span id='workout-inst'>${instructors[result.instructor_id]}</span><br/>
            </div>
            <span id='workout-desc'>${result.description}</span><br/>
          </div>
          <div class='col-2 workout-stats'>
            <span class='workout-stat'>${result.total_workouts.toLocaleString('en-US')}</span><br/>
            <span class='workout-text'>members</span><br/>
            <span class='workout-stat'>${(result.overall_rating_avg*100).toFixed(1)}% </span>
            <span class='workout-text-sm'>/${result.overall_rating_count.toLocaleString('en-US')}</span><br/>
            <span class='workout-text'>rating</span><br/>
            <span class='workout-stat'>${result.difficulty_rating_avg.toFixed(2)}</span>
            <span class='workout-text-sm'>/${result.difficulty_rating_count.toLocaleString('en-US')}</span><br/>
            <span class='workout-text'>difficulty</span><br/>
          </div>
          <div class='col-1'>
            <button class='add-workout' title='Add Workout' value=${result['id']}>
              <i class="bi bi-calendar-week"></i>
            </button>
          </div>
        </div>
        `);
      };
      const addWorkoutButtons = document.querySelectorAll('.add-workout');
      for (const addWorkoutButton of addWorkoutButtons) {
        addWorkoutButton.addEventListener('click', (event) => {
          event.preventDefault();
          const workout_date = document.querySelector('#workout-date').value
          const sched_order = document.querySelector('#sched-order').value
          const discipline = document.querySelector('#filter-discipline').value
          const workout_id = addWorkoutButton.value
          const url = `/add-class/${workout_date}/${sched_order}/${discipline}/${workout_id}`
          window.location.href = url
        });
      };
      if (results.page == 0) {
        document.querySelector('#prev-page').setAttribute('disabled', '');
      } else {
        document.querySelector('#prev-page').removeAttribute('disabled');
      };
      if (results.page == (results.page_count - 1)) {
        document.querySelector('#next-page').setAttribute('disabled', '');
      } else {
        document.querySelector('#next-page').removeAttribute('disabled');
      };
    });
  });
};




