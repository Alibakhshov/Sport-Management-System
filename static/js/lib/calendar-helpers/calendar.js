
'use strict'

new PerfectScrollbar('#calSidebar', {
  suppressScrollX: true
});

$('#datepicker1').datepicker({
  showOtherMonths: true,
  selectOtherMonths: true
});

var calendarEl = document.getElementById('calendar');
var calendar = new FullCalendar.Calendar(calendarEl, {
  initialView: 'dayGridMonth',
  headerToolbar: {
    left: 'custom1 prev,next today',
    center: 'title',
    right: 'dayGridMonth,timeGridWeek,timeGridDay'
  },
  eventSources: [calendarEvents, birthdayEvents, holidayEvents, discoveredEvents, meetupEvents, otherEvents],
  selectable: true,
  select: function(info) {
    var startDate = moment(info.start).format('LL');
    $('#startDate').val(startDate);

    var endDate = moment(info.startStr).add(1, 'days');
    $('#endDate').val(endDate.format('LL'));

    $('#modalCreateEvent').modal('show');
  },
  eventClick: function(info) {
    console.log(info.event.start);

    // Set title
    $('#modalLabelEventView').text(info.event.title);

    $('#modalEventView').modal('show');
  },
  customButtons: {
    custom1: {
      icon: 'chevron-left',
      click: function() {
        $('.main-calendar').toggleClass('show');
      }
    }
  }
});

calendar.render();

$('#btnCreateEvent').on('click', function(e){
  e.preventDefault();

  var startDate = moment().format('LL');
  $('#startDate').val(startDate);

  var endDate = moment().add(1, 'days');
  $('#endDate').val(endDate.format('LL'));

  $('#modalCreateEvent').modal('show');
});
