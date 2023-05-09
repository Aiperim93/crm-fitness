import {stats} from "./config.js";

$(document).ready(function() {
  const container = document.getElementById("stats");
  $('#start-date').val(localStorage.getItem('start-date'));
  $('#end-date').val(localStorage.getItem('end-date'));


function formatDate(date) {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
}


function loadChartData(start_date, end_date) {
  if (document.getElementById("myChart")) {
    document.getElementById("myChart").remove()
  }
  const url = `${stats}?start_date=${start_date}&end_date=${end_date}`
  $.ajax({
    type: 'GET',
    url: url,
    dataType: 'json',
    success: function(data) {
      localStorage.removeItem('week');
      localStorage.removeItem('error')
      let canvas = document.createElement('canvas');
      canvas.id = 'myChart'
      container.appendChild(canvas);
      let ctx = document.getElementById('myChart').getContext('2d');
      let chart = new Chart(ctx, {
        type: 'line',
        data: {
          labels: Object.keys(data),
          datasets: [
            {
              label: 'Посещения',
              data: Object.values(data).map(function(d) {
                return d.visits;
              }),
              backgroundColor: 'rgba(255, 99, 132, 0.2)',
              borderColor: 'rgba(255, 99, 132, 1)',
              borderWidth: 3,
              yAxisID: 'y-count'
            },
            {
              label: 'Сумма платежей',
              data: Object.values(data).map(function(d) {
                return d.total_amount;
              }),
              backgroundColor: 'rgba(54, 162, 235, 0.2)',
              borderColor: 'rgba(54, 162, 235, 1)',
              borderWidth: 3,
              yAxisID: 'y-amount'
            },
            {
              label: 'Количество платежей',
              data: Object.values(data).map(function(d) {
                return d.total_count;
              }),
              backgroundColor: 'rgba(255, 206, 86, 0.2)',
              borderColor: 'rgba(255, 206, 86, 1)',
              borderWidth: 3,
              yAxisID: 'y-count'
            },
            {
              label: 'Пропуски',
              data: Object.values(data).map(function(d) {
                return d.missing_count;
              }),
              backgroundColor: 'rgba(75, 192, 192, 0.2)',
              borderColor: 'rgba(75, 192, 192, 1)',
              borderWidth: 3,
              yAxisID: 'y-count'
            },
            {
              label: 'Количество Заморозок',
              data: Object.values(data).map(function(d) {
                return d.total_lazy_day;
              }),
              backgroundColor: 'rgba(148,59,192,0.2)',
              borderColor: 'rgb(159, 75, 192)',
              borderWidth: 3,
              yAxisID: 'y-count'
            }
          ]
        },
        options: {
          scales: {
            'y-count': {
              type: 'linear',
              position: 'left',
              beginAtZero: true,
              stepSize: 1,
              grid: {
                lineWidth: 3
              },
              scaleLabel: {
                display: true,
                labelString: 'Посещения'
                },
            },
            'y-amount': {
              type: 'linear',
              position: 'right',
              beginAtZero: true,
              stepSize: 1,
              scaleLabel: {
                display: true,
                labelString: 'Сумма платежей'
              }
            },
          }
        }
      });
      localStorage.setItem('chartData', JSON.stringify(data));
      localStorage.setItem('chartOptions', JSON.stringify(chart.options));
      localStorage.setItem('chartType', 'line');
      localStorage.setItem('chartLabels', JSON.stringify(chart.data.labels));
      localStorage.setItem('chartDatasets', JSON.stringify(chart.data.datasets));
    },

    error: function(jqXHR, textStatus, errorThrown) {
      localStorage.removeItem('chartData');
      localStorage.removeItem('chartOptions');
      localStorage.removeItem('chartType');
      localStorage.removeItem('chartLabels');
      localStorage.removeItem('chartDatasets');
      if (document.getElementById("error")) {
        document.getElementById("error").remove()
      }
      let error = document.createElement('p');
      error.id = 'error'
      error.className = 'text-center text-danger m-3 p-3'
      if (errorThrown === 'Forbidden') {
        error.innerHTML = 'Войдите в систему!'
        localStorage.setItem('error', 'Войдите в систему!')
      } else if (errorThrown === 'Bad Request') {
         error.innerHTML = 'Вы ввели некорректные данные!'
        localStorage.setItem('error', 'Вы ввели некорректные данные!')
      }
      container.appendChild(error)
      console.log('Error:', textStatus, errorThrown);
    }
  });
}

  let storedData = localStorage.getItem('chartData');
  let storedOptions = localStorage.getItem('chartOptions');
  let storedType = localStorage.getItem('chartType');
  let storedLabels = localStorage.getItem('chartLabels');
  let storedDatasets = localStorage.getItem('chartDatasets');
  let week = localStorage.getItem('week');
  let error = localStorage.getItem('error');

  if (!error) {
    if (storedData && storedOptions && storedType && storedLabels && storedDatasets) {
      let data = JSON.parse(storedData);
      let options = JSON.parse(storedOptions);
      let type = storedType;
      let labels = JSON.parse(storedLabels);
      let datasets = JSON.parse(storedDatasets);

      let canvas = document.createElement('canvas');
      canvas.id = 'myChart'
      container.appendChild(canvas);
      let ctx = document.getElementById('myChart').getContext('2d');
      let chart = new Chart(ctx, {
        type: type,
        data: {
          labels: labels,
          datasets: datasets
        },
        options: options
      });
      if (week) {
        let paragraph = document.createElement('p');
        let text = document.createElement('i');
        paragraph.id = 'week'
        paragraph.className = 'text-center m-3 p-3'
        text.innerHTML = week
        paragraph.appendChild(text)
        container.appendChild(paragraph)
      }
    } else {
      let today = new Date();
      let weekAgo = new Date();
      weekAgo.setDate(today.getDate() - 7);
      let startDate = formatDate(weekAgo)
      let endDate = formatDate(today)
      loadChartData(startDate, endDate);
      let paragraph = document.createElement('p');
      let text = document.createElement('i');
      paragraph.id = 'week'
      paragraph.className = 'text-center m-3 p-3'
      text.innerHTML = 'Статистика предоставлена за последнюю неделю'
      paragraph.appendChild(text)
      container.appendChild(paragraph)
      localStorage.setItem('week', 'Статистика предоставлена за последнюю неделю');
    }
  } else {
      let paragraph = document.createElement('p');
      paragraph.id = 'error'
      paragraph.className = 'text-center text-danger m-3 p-3'
      paragraph.innerHTML = error
      container.appendChild(paragraph)
  }

  $('#statistics-form').submit(function(event) {
    event.preventDefault();
    if (document.getElementById('week')) {
      document.getElementById('week').remove()
    }
    if (document.getElementById('error')) {
      document.getElementById('error').remove()
    }
    let startDate = $('#start-date').val();
    let endDate = $('#end-date').val();
    localStorage.setItem('start-date', startDate);
    localStorage.setItem('end-date', endDate);
    loadChartData(startDate, endDate);
  })
});
