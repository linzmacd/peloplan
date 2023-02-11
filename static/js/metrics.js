
if (document.querySelector('#metrics-measure').value == 'duration') {
  document.querySelector('#filter-metrics-measure').innerHTML = `
    <option id='option-duration' value='duration'>Minutes</option>
    <option id='option-count' value='count'>Class Count</option>
    `
  document.querySelector('#option-duration').classList.add('selected')
} else {
  document.querySelector('#filter-metrics-measure').innerHTML = `
  <option id='option-count' value='count'>Class Count</option>
  <option id='option-duration'  value='duration'>Minutes</option>
  `
document.querySelector('#option-count').classList.add('selected')
}

const disciplines = ['strength', 'yoga', 'running', 'walking', 
'bootcamp', 'meditation', 'stretching', 'cardio', 
'cycling', 'bike_bootcamp', 'caesar', 'caesar_bootcamp'];

const titles = {
  strength: 'Strength',
  yoga: 'Yoga',
  meditation: 'Meditation',
  cardio: 'Cardio',
  stretching: 'Stretching',
  cycling: 'Cycling',
  running: 'Running',
  walking: 'Walking',
  'bootcamp': 'Tread Bootcamp',
  'bike_bootcamp': 'Bike Bootcamp',
  caesar: 'Rowing',
  'caesar_bootcamp': 'Rowing Bootcamp'
};
const colors = {
  strength: 'rgba(0, 0, 0, 1)',
  yoga: 'rgba(128, 0, 128, 1)',
  meditation: 'rgba(0, 128, 0, 1)',
  cardio: 'rgba(218, 165, 32, 1)',
  stretching: 'rgba(0, 128, 0, .5)',
  cycling: 'rgba(255, 0, 0, 1)',
  running: 'rgba(0, 0, 255, 1)',
  walking: 'rgba(0, 0, 255, .66)',
  'bootcamp': 'rgba(0, 0, 255, .33)',
  'bike_bootcamp': 'rgba(255, 0, 0, .65)',
  caesar: 'rgba(240, 128, 128, 1)',
  'caesar_bootcamp': 'rgba(240, 128, 128, .75)'
};

document.addEventListener('DOMContentLoaded', function() {
  date = document.querySelector('#metrics-date').value;
  measure = document.querySelector('#metrics-measure').value;
  fetch(`/get-metrics/${date}/${measure}`)
  .then((response) => response.json())
  .then((metrics) => {
    console.log(metrics)
    const discData = metrics['discipline_data'];
    const pieLabels = [];
    const pieData = [];
    const pieColors = [];
    for (const discipline of disciplines) {
      if (discData[discipline]) {
        pieLabels.push(titles[discipline]);
        if (measure == 'duration') {
          pieData.push(discData[discipline]/60);
        } else {
          pieData.push(discData[discipline]);
        }
        pieColors.push(colors[discipline]);
      }
    };
    new Chart(document.querySelector('#pie-disciplines'), {
      type: 'doughnut',
      data: {
        labels: pieLabels,
        datasets: [{
          labels: pieLabels,
          data: pieData,
          backgroundColor: pieColors,
          hoverOffset: 20
        }],
      },
      options: {
        plugins: {
          legend: {
            display: true,
            position: 'right',
          }
        }
      }
    });
    const instData = metrics['instructor_data'];
    const barLabels = [];
    const barData = [];
    const barColors = [];
    let count = 1;
    let otherSum = 0
    for (const pair of instData) {
      const instructor = pair[0]
      const stat = pair[1]
      if (count < 12) {
        barLabels.push(instructor);
        if (measure == 'duration') {
          barData.push(stat/60)
        } else {
          barData.push(stat);
        };
        barColors.push(colors[disciplines[count]]);
      } else {
        otherSum += pair[1];
      }
      count++;
    };
    if (otherSum) {
      barLabels.push('Other');
      if (measure == 'duration') {
        barData.push(otherSum/60)
      } else {
        barData.push(otherSum);
      };
      barColors.push(colors[disciplines[count]])
    };
    new Chart(document.querySelector('#bar-instructors'), {
      type: 'doughnut',
      data: {
        labels: barLabels,
        datasets: [{
          labels: barLabels,
          data: barData,
          backgroundColor: barColors,
          hoverBackgroundColor: barColors,
          hoverOffset: 20
        }],
      },
      options: {
        plugins: {
          legend: {
            display: true,
            position: 'right',
          },
        },
      },
    });
  });
});

const metricsFilters = document.querySelectorAll('.metrics-filter')
for (const metricsFilter of metricsFilters) {
  metricsFilter.addEventListener('change', (event) => {
    event.preventDefault();
    const date = document.querySelector('#filter-metrics-date').value;
    const measure = document.querySelector('#filter-metrics-measure').value;
    const url = `/workout-stats/${date}/${measure}`;
    window.location.href = url
  });
};
