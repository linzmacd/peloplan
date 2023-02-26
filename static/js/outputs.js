
document.querySelector('a.nav-link.page-metrics').classList.add('active');

//  Output Chart
fetch('/get-outputs')
.then((response) => response.json())
.then ((data) => {
  const twentyOutputs = data.twenty
  const thirtyOutputs = data.thirty
  const fortyfiveOutputs = data.fortyfive
  const sixtyOutputs = data.sixty
  new Chart(document.querySelector('#graph-outputs'), {
    type: 'scatter',
    data: {
      datasets: [
        {
          label: '20 Min Ride',
          data: twentyOutputs,
          borderColor: 'rgba(255, 0, 0, 1)',
          backgroundColor: 'rgba(255, 0, 0, .25)',
          pointStyle: 'circle',
        },
        {
          label: '30 Min Ride',
          data: thirtyOutputs,
          borderColor: 'rgba(218, 165, 32, 1)',
          backgroundColor: 'rgba(218, 165, 32, .4)',
          pointStyle: 'circle'
        },
        {
          label: '45 Min Ride',
          data: fortyfiveOutputs,
          borderColor: 'rgba(0, 128, 0, 1)',
          backgroundColor: 'rgba(0, 128, 0, .25)',
          pointStyle: 'circle'
        },
        {
          label: '60 Min Ride',
          data: sixtyOutputs,
          borderColor: 'rgba(0, 0, 255, 1)',
          backgroundColor: 'rgba(0, 0 , 255 , .25)',
          pointStyle: 'circle'
        },   
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        x: {
          type: 'time',
          display: true,
        }
      },
      plugins: {
        tooltip: {
          callbacks: {
            label: function(content) {
              const date = new Date(content.raw.x).toLocaleDateString('en-us', {year:"numeric", month:"short", day:"numeric"})
              const tooltip = [`${content.dataset.label}`]
              tooltip.push([`${date}`]);
              tooltip.push([`Output: ${content.raw.y} KJ`]);
              return tooltip;
            }
          }
        }
      }
    }
  });
});