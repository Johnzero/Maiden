
WebRtcJingle = function() 
{
	if (!window.webkitRTCPeerConnection) 
	{
		var msg = "webkitRTCPeerConnection not supported by this browser";			
		alert(msg);
		throw Error(msg);

	}

	this.remoteOffer = null;
	this.localStream = null;
	this.callback = null;
	this.pc = null;
	this.sid = null;	
	this.farParty = null;
	this.interval = null;
	this.inviter = false;
	this.peerConfig = null;
	this.jid = null;
	
}

WebRtcJingle.prototype.startApp =  function(callback, peerConfig)
{
	//console.log("startApp");

	this.callback = callback;
	this.peerConfig = peerConfig;	
	this.getUserMedia();
}


WebRtcJingle.prototype.stopApp = function ()
{
	//console.log("stopApp");
	
	this.jingleTerminate();

	if (this.pc != null) this.pc.close();
	this.pc = null;
		
}

WebRtcJingle.prototype.getUserMedia  = function()
{
	//console.log("getUserMedia");

	navigator.webkitGetUserMedia({audio:true, video:true}, this.onUserMediaSuccess.bind(this), this.onUserMediaError.bind(this));
}

WebRtcJingle.prototype.onUserMediaSuccess = function(stream)
{
	var url = webkitURL.createObjectURL(stream);
	//console.log("onUserMediaSuccess " + url);
	this.localStream = stream;
	
	if (this.callback != null)
	{
		this.callback.startLocalMedia(url);
	}
}

WebRtcJingle.prototype.onUserMediaError = function (error)
{
	//console.log("onUserMediaError " + error.code);
}


WebRtcJingle.prototype.onMessage = function(packet)
{
	console.log("webrtc - onMessage");
	console.log(packet);

	var elem = this.textToXML(packet);

	if (elem.nodeName == "iq")
	{
		if (elem.getAttribute("type") == "result")
		{
			var channels = elem.getElementsByTagName("channel");
			
			if (channels.length > 0)
			{
				var relayHost = channels[0].getAttribute("host");
				var relayLocalPort = channels[0].getAttribute("localport");
				var relayRemotePort = channels[0].getAttribute("remoteport");
				
				console.log("add JingleNodes candidate: " + relayHost + " " + relayLocalPort + " " + relayRemotePort); 

				this.sendTransportInfo("0", "a=candidate:3707591233 1 udp 2113937151 " + relayHost + " " + relayRemotePort + " typ host generation 0");				
				
				var candidate = new RTCIceCandidate({sdpMLineIndex: "0", candidate: "a=candidate:3707591233 1 udp 2113937151 " + relayHost + " " + relayLocalPort + " typ host generation 0"});				
				this.pc.addIceCandidate(candidate);				
			}
		
		} else if (elem.getAttribute("type") != "error") {
		
			var jingle = elem.firstChild;
			this.sid = jingle.getAttribute("sid");

			if (jingle.nodeName == "jingle" && jingle.getAttribute("action") != "session-terminate")
			{	
				if (this.pc == null)
				{
					this.createPeerConnection();
				}

				if (jingle.getAttribute("action") == "transport-info")	
				{
					if (jingle.getElementsByTagName("candidate").length > 0)
					{
						var candidate = jingle.getElementsByTagName("candidate")[0];
						var ice = {sdpMLineIndex: candidate.getAttribute("label"), candidate: candidate.getAttribute("candidate")};				
						this.pc.addIceCandidate(new RTCIceCandidate(ice));
					}

				} else {

					if (jingle.getElementsByTagName("webrtc").length > 0)
					{
						var sdp = jingle.getElementsByTagName("webrtc")[0].firstChild.data;

						if (jingle.getAttribute("action") == "session-initiate")
						{
							this.inviter= false;			
							this.remoteOffer = new RTCSessionDescription({type: "offer", sdp : sdp});

							if (this.callback != null)
							{
								this.callback.incomingCall(elem.getAttribute("from"));
							}				

						} else {

							this.inviter= true;
							this.pc.setRemoteDescription(new RTCSessionDescription({type: "answer", sdp : sdp}));
							
							this.addJingleNodesCandidates();
						}
					}
				}

			} else {

				this.doCallClose();
			}
		}
	}
	
}

WebRtcJingle.prototype.acceptCall = function(farParty)
{
	//console.log("acceptCall");

	this.farParty = farParty;
	this.pc.setRemoteDescription(this.remoteOffer);	
}

WebRtcJingle.prototype.onConnectionClose = function()
{
	//console.log("webrtc - onConnectionClose");

	this.doCallClose();	
}
	

WebRtcJingle.prototype.jingleInitiate = function(farParty)
{
	//console.log("jingleInitiate " + farParty);

	this.farParty = farParty;
	this.inviter = true;	
	this.sid = "webrtc-initiate-" + Math.random().toString(36).substr(2,9);
	
	this.createPeerConnection();
	
	if (this.pc != null)
	{
		var webrtc = this;
		
		this.pc.createOffer( function(desc) 
		{
			webrtc.pc.setLocalDescription(desc);
			webrtc.sendJingleIQ(desc.sdp); 				

		}, null, {has_audio: true, has_video: true});		
	}
}

WebRtcJingle.prototype.jingleTerminate = function ()
{
	//console.log("jingleTerminate");

	this.sendJingleTerminateIQ()
	this.doCallClose();
}

WebRtcJingle.prototype.doCallClose = function ()
{
	if (this.pc != null) this.pc.close();
	this.pc = null;

	if (this.callback != null)
	{
		this.callback.terminatedCall();
	}	
}
	

WebRtcJingle.prototype.createPeerConnection = function()
{
	//console.log("createPeerConnection");

	this.pc = new window.webkitRTCPeerConnection(this.peerConfig);

	this.pc.onicecandidate = this.onIceCandidate.bind(this);		
	this.pc.onstatechange = this.onStateChanged.bind(this);
	this.pc.onopen = this.onSessionOpened.bind(this);
	this.pc.onaddstream = this.onRemoteStreamAdded.bind(this);
	this.pc.onremovestream = this.onRemoteStreamRemoved.bind(this);
	
	this.pc.addStream(this.localStream);

}

WebRtcJingle.prototype.onIceCandidate = function (event)
{
	//console.log("onIceCandidate");
	
	if (event.candidate && this.callback != null)
	{		
		this.sendTransportInfo(event.candidate.sdpMLineIndex, event.candidate.candidate);
	}	
		
}


WebRtcJingle.prototype.sendTransportInfo = function (sdpMLineIndex, candidate)
{
	//console.log("sendTransportInfo");
	
	var id = "webrtc-jingle-" + Math.random().toString(36).substr(2,9);

	var jingleIq = "<iq type='set' to='" + this.farParty + "' id='" + id + "'>";
	jingleIq = jingleIq + "<jingle xmlns='urn:xmpp:jingle:1' action='transport-info' initiator='" + this.jid + "' sid='" + this.sid + "'>";		      			      
	jingleIq = jingleIq + "<transport xmlns='http://phono.com/webrtc/transport'><candidate label='" + sdpMLineIndex + "' candidate='" + candidate + "' /></transport></jingle></iq>";      

	this.callback.sendPacket(jingleIq);	

}

WebRtcJingle.prototype.onSessionOpened = function (event)
{
	//console.log("onSessionOpened");
	//console.log(event);
}

WebRtcJingle.prototype.onRemoteStreamAdded = function (event)
{
	var url = webkitURL.createObjectURL(event.stream);
	//console.log("onRemoteStreamAdded " + url);
	//console.log(event);
	
	if (this.inviter == false)
	{
	    var webrtc = this;	
	    
	    this.pc.createAnswer( function (desc)
	    {
		webrtc.pc.setLocalDescription(desc);			
		webrtc.sendJingleIQ(desc.sdp); 	
		
	    }, null, {has_audio: true, has_video: true});			
	}
	
	if (this.callback != null)
	{
		this.callback.startRemoteMedia(url, this.farParty);
	}		
}

WebRtcJingle.prototype.onRemoteStreamRemoved = function (event)
{
	var url = webkitURL.createObjectURL(event.stream);
	//console.log("onRemoteStreamRemoved " + url);
	//console.log(event);
}

WebRtcJingle.prototype.onStateChanged = function (event)
{
	//console.log("onStateChanged");
	//console.log(event);
}



WebRtcJingle.prototype.sendJingleTerminateIQ = function()
{
	if (this.callback != null)
	{
		var id = "webrtc-jingle-" + Math.random().toString(36).substr(2,9);
			
		var jIQ = "<iq type='set' to='" + this.farParty + "' id='" + id + "'>";
		jIQ = jIQ + "<jingle xmlns='urn:xmpp:jingle:1' action='session-terminate' initiator='" + this.jid + "' sid='" + this.sid + "'>";
		jIQ = jIQ + "<reason><success/></reason></jingle></iq>"

		this.callback.sendPacket(jIQ);
	}
}


WebRtcJingle.prototype.sendJingleIQ = function(sdp)
{
	if (this.callback == null)
	{
		return;
	}

	//console.log("sendJingleIQ");
	//console.log(sdp);

	var action = this.inviter? "session-initiate" : "session-accept";
	var iq = "";
	var id = "webrtc-jingle-" + Math.random().toString(36).substr(2,9);
		
	iq += "<iq type='set' to='" +  this.farParty + "' id='" + id + "'>";
	iq += "<jingle xmlns='urn:xmpp:jingle:1' action='" + action + "' initiator='" + this.jid + "' sid='" + this.sid + "'>";
	iq += "<webrtc xmlns='http://webrtc.org'>" + sdp + "</webrtc>";
	iq += "</jingle></iq>";	

	this.callback.sendPacket(iq);
}


WebRtcJingle.prototype.textToXML = function (text)
{
	var doc = null;

	if (window['DOMParser']) {
	    var parser = new DOMParser();
	    doc = parser.parseFromString(text, 'text/xml');

	} else if (window['ActiveXObject']) {
	    var doc = new ActiveXObject("MSXML2.DOMDocument");
	    doc.async = false;
	    doc.loadXML(text);

	} else {
	    throw Error('No DOMParser object found.');
	}

	return doc.firstChild;
}

WebRtcJingle.prototype.addJingleNodesCandidates = function() 
{
	console.log("addJingleNodesCandidates");
	
	var iq = "";
	var id = "jingle-nodes-" + Math.random().toString(36).substr(2,9);
		
	iq += "<iq type='get' to='" +  "relay." + window.location.hostname + "' id='" + id + "'>";
	iq += "<channel xmlns='http://jabber.org/protocol/jinglenodes#channel' protocol='udp' />";
	iq += "</iq>";	

	this.callback.sendPacket(iq);	
}
