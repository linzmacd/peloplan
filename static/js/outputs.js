
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
          label: '20 Mins',
          data: twentyOutputs,
          borderColor: 'rgba(255, 0, 0, 1)',
          backgroundColor: 'rgba(255, 0, 0, .25)',
          pointStyle: 'circle'
        },
        {
          label: '30 Mins',
          data: thirtyOutputs,
          borderColor: 'rgba(218, 165, 32, 1)',
          backgroundColor: 'rgba(218, 165, 32, .4)',
          pointStyle: 'circle'
        },
        {
          label: '45 Mins',
          data: fortyfiveOutputs,
          borderColor: 'rgba(0, 128, 0, 1)',
          backgroundColor: 'rgba(0, 128, 0, .25)',
          pointStyle: 'circle'
        },
        {
          label: '60 Mins',
          data: sixtyOutputs,
          borderColor: 'rgba(0, 0, 255, 1)',
          backgroundColor: 'rgba(0, 0 , 255 , .25)',
          pointStyle: 'circle'
        },   
      ],
    },
    options: {
      scales: {
        x: {
          type: 'timeseries',
        }
      },
      plugins: {
        tooltips: {
          callbacks: {
            label: function(context) {
              let label = context.parsed.y;
              return label
            }
          }
        }
      }
    }
  });
});