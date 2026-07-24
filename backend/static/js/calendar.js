
document.addEventListener('DOMContentLoaded', function() {

  const calendarEl = document.getElementById('calendar');
  const eventsUrl = calendarEl.dataset.eventsUrl;

  const calendar = new FullCalendar.Calendar(calendarEl, {
    initialView: 'dayGridMonth',
    height: 600,   // controlled height (clean UI)
    events: eventsUrl
  });

  calendar.render();

});
