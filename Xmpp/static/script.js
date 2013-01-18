var conn = new Strophe.Connection("http://bosh.metajack.im:5280/xmpp-httpbind");
function my_callback(status) {
if (status === Strophe.Status.CONNECTED) {
conn.disconnect();
}
}
//conn.connect("zero1233276@jabber.org", "zero1233276", my_callback);				  

var Hello = {
    
    
connection: null,
start_time: null,



log: function (msg) {
$('#log').append('<p>' + msg + '</p>');
},


handle_pong: function (iq) {
var elapsed = (new Date()).getTime() - Hello.start_time;
Hello.log("Received pong from server in " + elapsed + "ms");
Hello.connection.disconnect();
return false;
},


send_ping: function (to) {
var ping = $iq({
to: to,
type: 'get',
id: 'ping1'}).c('ping', {xmlns: 'urn:xmpp:ping'});


Hello.log("Sending ping to " + to + ".");
Hello.start_time = (new Date()).getTime();
Hello.connection.send(ping);}

            };

$(document).ready(function () {
$('#login_dialog').dialog({
autoOpen: true,
draggable: false,
modal: true,
title: 'Connect to XMPP',
buttons: {
"Connect": function () {
$(document).trigger('connect', {
jid: $('#jid').val(),
password: $('#password').val()
});
$('#password').val('');
$(this).dialog('close');
}
}
});
});


$(document).bind('connect', function (ev, data) {
var conn = new Strophe.Connection(
'http://bosh.metajack.im:5280/xmpp-httpbind');
conn.connect(data.jid, data.password, function (status) {
if (status === Strophe.Status.CONNECTED) {
$(document).trigger('connected');
} else if (status === Strophe.Status.DISCONNECTED) {
$(document).trigger('disconnected');
}
});
Hello.connection = conn;

});



$(document).bind('connected', function () {
Hello.log("Connection established.");
Hello.connection.addHandler(Hello.handle_pong, null, "iq", null, "ping1");
var domain = Strophe.getDomainFromJid(Hello.connection.jid);
Hello.send_ping(domain);
});



$(document).bind('disconnected', function () {
Hello.log("Connection terminated.");
Hello.connection = null;
});







