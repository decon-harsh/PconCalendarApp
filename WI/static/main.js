document.addEventListener('DOMContentLoaded', function () {
    var calendarEl = document.getElementById('calendar');
    var today = new Date();
    var dd = String(today.getDate()).padStart(2, '0');
    var mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
    var yyyy = today.getFullYear();

    today = yyyy + '-' + mm + '-' + dd;
    var calendar = new FullCalendar.Calendar(calendarEl, {

        initialView: 'dayGridMonth',
        initialDate: today,
        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,timeGridWeek,timeGridDay'
        },
        events: window.value,

        eventClick: function (info) {
            var groupmembers=[];
            var i;
            for(i=0;i<Object.keys(info.event.extendedProps).length;i++)
            {
                groupmembers.push((info.event.extendedProps[i.toString()]).toString());
            }
            if (groupmembers.length>0){
                alert("-> Title of this event is : " + info.event.title +"\n-> StartDate : " + info.event.start + "\n-> EndDate : " + info.event.end + "\n-> Group members are: \n"+ groupmembers.join("\n"));
            }
            else{
                alert("No group members");
            }


            // console.log(Object.keys(info.event.extendedProps).length);
        }

    });
    calendar.render();
});




