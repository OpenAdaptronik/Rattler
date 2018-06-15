var color = ['#005C47','#FF6600' , '#006E94' , '#FDC300', '#B28700' , '#FF3400']
var dateFormat = $("#dateFormat").val();
$('.datepicker').pickadate({
    monthsFull: [ 'Januar', 'Februar', 'März', 'April', 'Mai', 'Juni', 'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember' ],
    monthsShort: [ 'Jan', 'Feb', 'Mär', 'Apr', 'Mai', 'Jun', 'Jul', 'Aug', 'Sep', 'Okt', 'Nov', 'Dez' ],
    weekdaysFull: [ 'Sonntag', 'Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag' ],
    weekdaysShort: [ 'So', 'Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa' ],
    today: 'Heute',
    clear: 'Löschen',
    close: 'Schließen',
    firstDay: 1,
    format: 'dddd, dd. mmmm yyyy',
    formatSubmit: dateFormat
});
