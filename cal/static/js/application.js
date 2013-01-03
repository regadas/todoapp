(function() {

  $(document).ready(function() {
    var calendar, remote_data, todo_edit_form, todo_form;
    moment.defaultFormat = 'YYYY-MM-DDTHH:mm:ss';
    calendar = $('#calendar');
    todo_form = $('#todo-form');
    todo_edit_form = $('#todo-edit-form');
    $('#todo-add-start').datetimepicker({
      'dateFormat': 'yy-mm-dd',
      'timeFormat': 'hh:mm:ss'
    });
    $('#todo-add-end').datetimepicker({
      'dateFormat': 'yy-mm-dd',
      'timeFormat': 'hh:mm:ss'
    });
    $('#todo-edit-start').datetimepicker({
      'dateFormat': 'yy-mm-dd',
      'timeFormat': 'hh:mm:ss'
    });
    $('#todo-edit-end').datetimepicker({
      'dateFormat': 'yy-mm-dd',
      'timeFormat': 'hh:mm:ss'
    });
    remote_data = function() {
      var fragment, url;
      url = document.URL;
      fragment = url.split('public');
      if (fragment.length === 2) {
        return {
          'calendar': fragment[1].replace(/\/|#/g, '')
        };
      } else {
        return {};
      }
    };
    calendar.fullCalendar({
      eventSources: [
        {
          url: '/todos',
          type: 'GET',
          data: remote_data(),
          error: function() {
            return alert('there was an error while fetching events!');
          },
          color: 'yellow',
          textColor: 'black'
        }
      ],
      header: {
        left: 'prev,next today',
        center: 'title',
        right: 'month,agendaWeek,agendaDay'
      },
      allDayDefault: false,
      editable: false,
      droppable: false,
      eventClick: function(event, jsEvent, view) {
        var copy, original;
        original = $(this).data('eventObject');
        copy = $.extend({}, original);
        copy.id = event.id;
        copy.start = event.start;
        copy.end = event.end;
        copy.allDay = event.allDay;
        $("#todo-edit-title").val(event.title);
        $("#todo-edit-start").val(moment(event.start).format('YYYY-MM-DD HH:mm:ss'));
        $("#todo-edit-end").val(moment(event.end).format('YYYY-MM-DD HH:mm:ss'));
        todo_edit_form.data('eventObject', copy);
        return todo_edit_form.modal('toggle');
      },
      dayClick: function(date, allDay, jsEvent, view) {
        var copy, original;
        original = $(this).data('eventObject');
        copy = $.extend({}, original);
        copy.start = date;
        copy.allDay = false;
        todo_form.data('eventObject', copy);
        $("#todo-add-start").val(moment(copy.start).format('YYYY-MM-DD HH:mm:ss'));
        return todo_form.modal('toggle');
      }
    });
    $('#todo-add').on('click', function() {
      var data, event, title;
      event = todo_form.data('eventObject');
      event.color = 'red';
      title = $("#todo-title").val();
      event.title = title;
      event.start = moment($("#todo-add-start").val(), 'YYYY-MM-DD HH:mm:ss').toDate();
      event.end = moment($("#todo-add-end").val(), 'YYYY-MM-DD HH:mm:ss').toDate();
      data = remote_data();
      data.start = moment(event.start).format();
      data.end = moment(event.end).format();
      data.title = event.title;
      return $.post("/todos/create", JSON.stringify(data), function(data) {
        event.id = data.id;
        calendar.fullCalendar('renderEvent', event, true);
        return todo_form.modal('toggle');
      });
    });
    $('#todo-edit').on('click', function() {
      var data, event;
      event = todo_edit_form.data('eventObject');
      event.title = $("#todo-edit-title").val();
      event.start = moment($("#todo-edit-start").val(), 'YYYY-MM-DD HH:mm:ss').toDate();
      event.end = moment($("#todo-edit-end").val(), 'YYYY-MM-DD HH:mm:ss').toDate();
      calendar.fullCalendar('removeEvents', [event.id]);
      calendar.fullCalendar('renderEvent', event, true);
      data = remote_data();
      data.id = event.id;
      data.start = moment(event.start).format();
      data.end = moment(event.end).format();
      data.title = event.title;
      return $.post("/todos/edit/", JSON.stringify(data), function(data) {
        return todo_edit_form.modal('toggle');
      });
    });
    $('#todo-delete').on('click', function() {
      var data, event;
      event = todo_edit_form.data('eventObject');
      calendar.fullCalendar('removeEvents', [event.id]);
      data = remote_data();
      data.id = event.id;
      console.log(data);
      return $.post("/todos/delete", JSON.stringify(data), function(data) {
        return todo_edit_form.modal('toggle');
      });
    });
    $('#share').on('click', function() {
      var href;
      href = $(this).attr('href');
      $.ajax({
        type: 'POST',
        url: href,
        success: function() {
          $('#unshare').show();
          return $('#share-calendar').modal('toggle');
        }
      });
      return false;
    });
    return $('#unshare').on('click', function() {
      var href, that;
      that = $(this);
      href = that.attr('href');
      $.ajax({
        type: 'POST',
        url: href,
        success: function() {
          return that.hide();
        }
      });
      return false;
    });
  });

}).call(this);
