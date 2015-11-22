var guws = '/config/wifi/sta/ssid';
var guwp = '/config/wifi/sta/password';

var guah = '/config/api/hostname';
var guap = '/config/api/port';

var gus = '/action/save';

var gur = '/action/register';

var guiw = '/info/wifi/sta';
var guir = '/info/register';

var gmt = t('<li class="#{this.c}">#{this.v}</li>');

/**
 * Get WiFi Status
 */
function gws()
{
    var r;
    r = new j();
    r.open('GET', guiw, false);
    r.onreadystatechange = function () {
        var status = JSON.parse(r.responseText);
        var message_element = $('#msw');
        message_element.innerHTML = '';
        if(status['connected'] == true) {
            message_element.className = "msg success";
            message_element.innerHTML += gmt({'c':'', 'v': 'Connected'});
            message_element.innerHTML += gmt({'c':'', 'v': 'IP: ' + status['ip']});
            message_element.innerHTML += gmt({'c':'', 'v': 'Netmask: ' + status['netmask']});
        } else {
            message_element.className = "msg error";
            message_element.innterHTML = gmt({'c':'', 'v': 'Not connected'});
        }
    };
    r.send();
}

/**
 * Get Register Status
 */
function grs()
{
    var r;
    r = new j();
    r.open('GET', guir, false);
    r.onreadystatechange = function () {
        var status = JSON.parse(r.responseText);
        var message_element = $('#msr');
        message_element.innerHTML = '';
        if(status['registered'] == true) {
            message_element.className = "msg success";
            message_element.innerHTML += gmt({'c':'', 'v': 'Registered'});
        } else {
            message_element.className = "msg error";
            message_element.innterHTML = gmt({'c':'', 'v': 'Not Registered'});
        }
    };
    r.send();
}

function load()
{
    var r;
    r = new j();
    r.open('GET', guws, false);
    r.onreadystatechange = function () {
        if(r.status == 200) {
            $('#s').value = r.responseText;
        }
    };
    r.send();

    r = new j();
    r.open('GET', guah, false);
    r.onreadystatechange = function () {
        if(r.status == 200) {
            $('#h').value = r.responseText;
        }
    };
    r.send();

    r = new j();
    r.open('GET', guap, false);
    r.onreadystatechange = function () {
        if(r.status == 200) {
            $('#po').value = r.responseText;
        }
    };
    r.send();
}

/**
 * Save API config
 */
function sa()
{
    var message_element = $('#ma');
    message_element.innerHTML = '';
    sa_h(message_element);
}

/**
 * Save API Hostname
 */
function sa_h(message_element)
{
    var hostname = $('#h').value;
    var r = new j();
    r.open('POST', guah, false);
    r.onreadystatechange = function () {
        var class = 'msg success';
        if(r.status != 200) {
            class = "msg error";
        }
        message_element.innerHTML += gmt({'c': class, 'v': r.responseText});
        sa_p(message_element);
    };

    r.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
    r.send("hostname=" + encodeURIComponent(hostname));
}

/**
 * Save API Port
 */
function sa_p(message_element)
{
    var port = $('#po').value;
    var r = new j();
    r.open('POST', guap, false);
    r.onreadystatechange = function () {
        var class = 'msg success';
        if(r.status != 200) {
            class = "msg error";
        }
        message_element.innerHTML += gmt({'c': class, 'v': r.responseText});
        save(message_element);
    };

    r.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
    r.send("port=" + encodeURIComponent(port));
}

/**
 * Save WiFi
 */
function sw()
{
    var message_element = $('#mw');
    message_element.innerHTML = '';
    sw_ssid(message_element);
}

/**
 * Save WiFi Password
 */
function sw_pw(message_element)
{
    var password = $('#p').value;

    r = new j();
    r.open('POST', guwp, false);
    r.onreadystatechange = function () {
        var class = 'msg error';
        if(r.status != 200) {
            class = "msg error";
        }
        message_element.innerHTML += gmt({'c': class, 'v': r.responseText});
        save(message_element);
    };

    r.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
    r.send("password=" + encodeURIComponent(password));
}

/**
 * Save WiFi SSID
 */
function sw_ssid(message_element)
{
    var ssid = $('#s').value;

    var r = new j();
    r.open('POST', guws, false);
    r.onreadystatechange = function () {
        var class = 'msg error';
        if(r.status != 200) {
            class = "msg error";
        }
        message_element.innerHTML += gmt({'c': class, 'v': r.responseText});
        sw_pw(message_element);
    };

    r.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
    r.send("ssid=" + encodeURIComponent(ssid));
}

/**
 * Save to flash
 */
function save(message_element)
{
    r = new j();
    r.open('GET', gus, false);
    r.onreadystatechange = function () {
        var class = "msg success";
        if(r.status != 200) {
            class = "msg error";
        }
        message_element.innerHTML += gmt({'c': class, 'v': r.responseText});
    };

    r.send();
}

function register(f)
{
    var message_element = $('#mr');

    var email = $('#e').value;
    var name = $('#n').value;

    var r = new j();
    r.open('POST', gur, false);
    r.onreadystatechange = function () {
        var class = 'msg success';
        if(r.status != 200) {
            class = "msg error";
        }
        message_element.innerHTML += gmt({'c': class, 'v': r.responseText});
    };

    r.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
    r.send("email=" + encodeURIComponent(email) + "&name=" + encodeURIComponent(name));
}