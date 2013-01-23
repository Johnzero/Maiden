var Groupie = {
connection: null,
room: null,
nickname: null
};
$(document).ready(function () {
$('#login_dialog').dialog({
autoOpen: true,
draggable: false,
modal: true,
title: 'Join a Room',
buttons: {
"Join": function () {
Groupie.room = $('#room').val();
Groupie.nickname = $('#nickname').val();
$(document).trigger('connect', {
jid: $('#jid').val(),
password: $('#password').val()
});
$('#password').val('');
$(this).dialog('close');
}
}
});});
$(document).bind('connect', function (ev, data) {
Groupie.connection = new Strophe.Connection('http://127.0.0.1:7070/http-bind/');
Groupie.connection.connect(
data.jid, data.password,
function (status) {
if (status === Strophe.Status.CONNECTED) {
$(document).trigger('connected');
} else if (status === Strophe.Status.DISCONNECTED) {
$(document).trigger('disconnected');
}
});
});
$(document).bind('connected', function () {
// nothing here yet
});
$(document).bind('disconnected', function () {
// nothing here yet
});