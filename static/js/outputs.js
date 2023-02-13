document.addEventListener('DOMContentLoaded', function() {
  // const days = ['2023-02-01','2023-02-02','2023-02-03','2023-02-04','2023-02-05','2023-02-06','2023-02-07',]
  // const outputs = [10,20,30,40,50,60,70]
  // const days = ['2023-02-01','2023-02-02','2023-02-03','2023-02-04','2023-02-05','2023-02-06','2023-02-07',]
  // const outputs = [{x:'2023-02-01', y:10},{x:'2023-02-02', y:20},{x:'2023-02-03', y:30}]
  // const days2 = ['2023-02-02','2023-02-03','2023-02-06']
  // const outputs2 = [{x:'2023-02-02', y:30},{x:'2023-02-05', y:40},{x:'2023-02-07',  y:50}]
  
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
        // labels: days,
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
});





  // fetch(`/get-outputs`)
  // .then((response) => response.json())
  // .then((metrics) => {
  //   console.log(metrics)
    // const discData = metrics['discipline_data'];
    // const pieLabels = [];
    // const pieData = [];
    // const pieColors = [];
    // for (const discipline of disciplines) {
    //   if (discData[discipline]) {
    //     pieLabels.push(titles[discipline]);
    //     if (measure == 'duration') {
    //       pieData.push(discData[discipline]/60);
    //     } else {
    //       pieData.push(discData[discipline]);
    //     }
    //     pieColors.push(colors[discipline]);
    //   }
    // };

//   });
// });


