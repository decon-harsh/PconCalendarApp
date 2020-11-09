$(function() {
    $('input[name="daterange"]').daterangepicker({
      timePicker: true,
      autoUpdateInput: true,
      locale: {
        format: 'DD/M/Y H:mm',
        cancelLabel: 'Clear'
      }
    });
  });