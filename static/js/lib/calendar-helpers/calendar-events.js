// sample calendar events data

'use strict'

var curYear = moment().format('YYYY');
var curMonth = moment().format('MM');




// Competitions Events Source
var competitionEvents = {
  backgroundColor: '#fcbfdc',
  borderColor: '#f10075',
  events: [
    {
      id: '10',
      start: curYear+'-'+curMonth+'-04',
      end: curYear+'-'+curMonth+'-06',
      title: 'Feast Day',
      description: 'Hey this is Feast Day!'
    },
    {
      id: '11',
      start: curYear+'-'+curMonth+'-26',
      end: curYear+'-'+curMonth+'-27',
      title: 'Memorial Day',
      description: 'Hey this is Memorial Day!'
    },
    {
      id: '12',
      start: curYear+'-'+curMonth+'-28',
      end: curYear+'-'+curMonth+'-29',
      title: 'Veteran\'s Day'
    }
  ]
};


// Regular Events Source
var regularEvents = {
  backgroundColor: '#dedafe',
  borderColor: '#5b47fb',
  events: [
    {
      id: '14',
      start: curYear+'-'+curMonth+'-03',
      end: curYear+'-'+curMonth+'-05',
      title: 'UI/UX Meetup Conference',
      description: 'Hey this is an important event'
    },
    {
      id: '15',
      start: curYear+'-'+curMonth+'-18',
      end: curYear+'-'+curMonth+'-20',
      title: 'Angular Conference Meetup',
      description: 'Hey this is an important event'
    }
  ]
};

