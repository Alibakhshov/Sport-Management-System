'use strict'

// Monthly Growth Revenue
var optionOne = {
  series: [
    {
      name: 'Growth',
      data: dp2
    },{
      name: 'Actual',
      data: dp1
    },{
      name: 'Plan',
      data: dp3
    }
  ],
  chart: {
    type: 'area',
    height: 300,
    parentHeightOffset: 0,
    stacked: true,
    toolbar: {
      show: false
    }
  },
  colors: ['#5575dc', '#81adee', '#ccd1ed'],
  dataLabels: {
    enabled: false
  },
  grid: {
    borderColor: 'rgba(72,94,144, 0.07)',
    padding: {
      top: -20
    },
    yaxis: {
      lines: {
        show: false
      }
    }
  },
  stroke: {
    curve: 'smooth',
    width: 1.5
  },
  fill: {
    type: 'gradient',
    gradient: {
      opacityFrom: 0.35,
      opacityTo: 0.65,
    }
  },
  legend: {
    show: false
  },
  tooltip: {
    enabled: false
  },
  yaxis: {
    max: 200,
    tickAmount: 6,
    show: false
  },
  xaxis: {
    type: 'numeric',
    tickAmount: 13,
    labels: {
      style: {
        colors: '#6e7985',
        fontSize: '11px'
      }
    }
  },
};

var chartOne = new ApexCharts(document.querySelector('#apexChart1'), optionOne);
chartOne.render();

// Account Retention
var optionTwo = {
  series: [{
    data: [10, 12, 18, 25, 15, 30, 40, 10, 20, 12, 16, 60, 20, 15, 10, 60, 50, 40, 80, 100, 30, 40, 10, 20, 12, 16, 60, 20, 15, 60, 20, 15, 10, 60, 50, 40, 30, 40, 10, 20]
  },{
    data: [-10, -12, -18, -25, -15, -30, -40, -10, -20, -12, -16, -60, -20, -15, -10, -60, -50, -40, -80, -40, -30, -40, -10, -20, -12, -16, -60, -20, -15, -60, -20, -15, -10, -60, -50, -40, -30, -40, -10, -20]
  }],
  chart: {
    type: 'bar',
    height: 180,
    parentHeightOffset: 0,
    stacked: true,
    toolbar: {
      show: false
    }
  },
  colors: ['#506fd9', '#85b6ff'],
  grid: {
    borderColor: 'rgba(72,94,144, 0.07)',
    padding: {
      top: -20
    },
    yaxis: {
      lines: {
        show: false
      }
    }
  },
  plotOptions: {
    bar: {
      horizontal: false,
      columnWidth: '60%',
      endingShape: 'rounded'
    },
  },
  dataLabels: {
    enabled: false
  },
  stroke: {
    show: true,
    width: 2,
    colors: ['transparent']
  },
  yaxis: {
    show: false
  },
  xaxis: {
    type: 'numeric',
    tickAmount: 10,
    decimalsInFloat: 0,
    labels: {
      style: {
        colors: '#6e7985',
        fontSize: '10px'
      }
    }
  },
  fill: {
    opacity: 1
  },
  legend: {
    show: false
  },
  tooltip: {
    enabled: false
  }
};

var chartTwo = new ApexCharts(document.querySelector('#apexChart2'), optionTwo);
chartTwo.render();

// Real Time Sales
var ctx1 = document.getElementById('chartBar1').getContext('2d');
var bar1 = new Chart(ctx1, {
  type: 'bar',
  data: {
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
    datasets: [{
      data: [20, 60, 50, 45, 50, 60, 70, 40, 45, 35, 25, 30],
      backgroundColor: '#506fd9',
      barPercentage: 0.5
    }, {
      data: [10, 40, 30, 40, 60, 55, 45, 35, 30, 20, 15, 20],
      backgroundColor: '#85b6ff',
      barPercentage: 0.5
    }]
  },
  options: {
    indexAxis: 'y',
    maintainAspectRatio: false,
    responsive: true,
    plugins: {
      legend: {
        display: false
      }
    },
    scales: {
      x: {
        beginAtZero:true,
        max: 100,
        grid: {
          borderColor: '#e2e5ec',
          color: '#f3f5f9'
        },
        ticks: {
          color: '#212830',
          font: {
            size: 10,
            weight: '500'
          }
        }
      },
      y: {
        grid: {
          borderWidth: 0,
          color: '#f3f5f9'
        },
        ticks: {
          color: '#212830',
          font: {
            size: 12
          }
        }
      }
    }
  }
});


// Sales Revenue
$('#vmap').vectorMap({
  map: 'usa_en',
  backgroundColor: '#fff',
  borderColor: '#fff',
  color: '#d9dde7',
  selectedColor: null,
  hoverColor: null,
  hoverOpacity: 0.8,
  enableZoom: false,
  showTooltip: true,
  colors: {
    ca: '#85b6ff',
    tx: '#506fd9',
    mo: '#0dcaf0',
    co: '#33d685',
    ny: '#ea4c89'
  }
});


// Dark skin integration
function switchDark(enabled) {

  if(enabled) {
    bar1.options.scales['x'].grid.color = '#222b41';
    bar1.options.scales['x'].ticks.color = 'rgba(255,255,255,.65)';
    bar1.options.scales['x'].grid.borderColor = '#222b41';
    bar1.options.scales['y'].grid.color = '#222b41';
    bar1.options.scales['y'].ticks.color = 'rgba(255,255,255,.65)';

    $('#vmap').vectorMap('set', 'backgroundColor', '#192030');

  } else {

    bar1.options.scales['x'].grid.color = '#edeff6';
    bar1.options.scales['x'].ticks.color = '#42484e';
    bar1.options.scales['x'].grid.borderColor = '#edeff6';
    bar1.options.scales['y'].grid.color = '#edeff6';
    bar1.options.scales['y'].ticks.color = '#42484e';

    $('#vmap').vectorMap('set', 'backgroundColor', '#fff');
  }

  bar1.update();
}

if(skinMode) { switchDark(true); }

// Switch between light and dark
$('#skinMode .nav-link').bind('click', function(e){
  var mode = $(this).text().toLowerCase();
  if(mode == 'dark') {
    switchDark(true);
  } else {
    switchDark(false);
  }
});
