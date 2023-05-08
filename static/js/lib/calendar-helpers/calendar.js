
'use strict'

const urlsContainer = document.getElementById('url-container');
const eventsUrl = urlsContainer.dataset.eventsApi;
const competitionsUrl = urlsContainer.dataset.competitionsApi;


new PerfectScrollbar('#calSidebar', {
  suppressScrollX: true
});

$('#datepicker1').datepicker({
  showOtherMonths: true,
  selectOtherMonths: true
});


async function fetchCompetitionEvents() {
  const response = await fetch(competitionsUrl);
  const data = await response.json();
  return data.map(event => ({
    id: event.id,
    title: event.name,
    start: event.start_date_time,
    end: event.end_date_time,
    sport: event.sport,
    description: event.description,
    location: event.location,
    event_type: event.event_type,
    status: event.status,
    extendedProps: {
      side_a: event.side_a,
      side_b: event.side_b,
      side_a_score: event.side_a_score,
      side_b_score: event.side_b_score,
    },

  }));
}


async function fetchRegularEvents() {
  const response = await fetch(eventsUrl);
  const data = await response.json();
  return data.map(event => ({
    id: event.id,
    start: event.start_date_time,
    end: event.end_date_time,
    title: event.name,
    sport: event.sport,
    description: event.description,
    location: event.location,
    event_type: event.event_type,
    
    creator: event.creator.name,
    participants: event.participants_count,
    declined_participants: event.declined_participants_count,
    
  }));
}


async function fetchParticipant(id, sportType) {
  try {
    const parsedId = parseInt(id, 10); // Parse the ID as an integer
    let response, data;

    if (sportType === 'Single-Player') {
      response = await fetch(`/api/user/${parsedId}/`);
      data = await response.json();
    } else if (sportType === 'Team-Player') {
      response = await fetch(`/api/team/${parsedId}/`);
      data = await response.json();
    }

    return {
      name: data.name,
      avatar_url: data.avatar, // Replace 'avatar' with the actual property name in the API response, if different
    };
  } catch (error) {
    console.error(`Error fetching participant: ${error}`);
  }
}



var calendarEl = document.getElementById('calendar');
var calendar = new FullCalendar.Calendar(calendarEl, {
  eventTimeFormat: {
    hour: '2-digit',
    minute: '2-digit',
    hour12: true,
    meridiem: 'short'
  },
  firstDay: 1,

  initialView: 'dayGridMonth',
  headerToolbar: {
    left: 'custom1 prev,next today',
    center: 'title',
    right: 'dayGridMonth,timeGridWeek,timeGridDay'
  },
  eventSources: [
    {
      backgroundColor: '#fcbfdc',
      borderColor: '#f10075',
      display: 'block',
      events: function(fetchInfo, successCallback, failureCallback) {
        fetchCompetitionEvents()
          .then(events => successCallback(events))
          .catch(err => failureCallback(err));
      },

    },

    {
      backgroundColor: '#dedafe',
      borderColor: '#5b47fb',
      display: 'block',
      events: function(fetchInfo, successCallback, failureCallback) {
        fetchRegularEvents()
          .then(events => successCallback(events))
          .catch(err => failureCallback(err));
      },
    },
  ],
  
  selectable: true,

  select: function(info) {
    var startDate = moment(info.start);
    var endDate = moment(info.start).add(1, 'hours'); // Adjust the duration as needed
  
    // Set the start and end date-time values in the form
    document.getElementById('startDate').value = startDate.format('YYYY-MM-DDTHH:mm');
    document.getElementById('endDate').value = endDate.format('YYYY-MM-DDTHH:mm');
  
    $('#modalCreateEvent').modal('show');
  },

  eventClick: async function(info) {
    // Set title
    $('#modalLabelEventView').text(info.event.title);
  
    $('#eventStart').text(moment(info.event.start).format('MMMM D, YYYY hh:mmA'));
    $('#eventEnd').text(moment(info.event.end).format('MMMM D, YYYY hh:mmA'));
  
    $('#eventLocation').text(info.event.extendedProps.location);
    $('#eventSport').text(info.event.extendedProps.sport.name);
    $('#eventDescription').text(info.event.extendedProps.description);

    $('#status').text(info.event.extendedProps.status);

    $('#eventCreator').text(info.event.extendedProps.creator);
    $('#usersInterested').text(info.event.extendedProps.participants);
    console.log(info.event.extendedProps.participants);

    $('#AScore').text(info.event.extendedProps.side_a_score);
    $('#BScore').text(info.event.extendedProps.side_b_score);
  
    const eventType = info.event.extendedProps.event_type;
  
    if (eventType === 'Competition') {
      const sideA = info.event.extendedProps.side_a;
      const sideB = info.event.extendedProps.side_b;
      const sportType = info.event.extendedProps.sport.sport_type;
  
      const participantA = await fetchParticipant(sideA, sportType);
      const participantB = await fetchParticipant(sideB, sportType);

      
      // Update UI with the participant's information
      if (participantA) {
        $('#participantAName').text(participantA.name);
        $('#participantAImg').attr('src', participantA.avatar_url);
      }
  
      if (participantB) {
        $('#participantBName').text(participantB.name);
        $('#participantBImg').attr('src', participantB.avatar_url);
      }
      
      $('#beasts').show();
      $('#competition_score').show();
      $('#competition_status').show();
      $('#spc_bar').show();
      $('#creatorofevent').hide();
      $('#interestedusers').hide();
    } else {
      // Hide the participants section in the UI
      $('#beasts').hide();
      $('#competition_score').hide();
      $('#competition_status').hide();
      $('#spc_bar').hide();
      $('#creatorofevent').show();
      $('#interestedusers').show();
    }
  
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
