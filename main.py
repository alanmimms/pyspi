import localconfig
import network
import utime
import esp32


config = esp32.NVS('config')

try:
        essidBA = bytearray(64, 'utf-8')
        len = config.get_blob('essid', essidBA)
        essid = essidBA[0:len].decode()
except:
        while True:
                print('Missing "essid". You must define esp32.NVS("config") blobs for "essid" and "password"')


try:
        passBA = bytearray(64, 'utf-8')
        len = config.get_blob('password', passBA)
        password = passBA[0:len].decode()
except:
        while True:
                print('Missing "password". You must define esp32.NVS("config") blobs for "essid" and "password"')


nic = network.WLAN(network.STA_IF)
nic.active(True)

utime.sleep(1)
nic.connect(essid, password)

while not nic.isconnected():
        print('Trying to connect.')
        print('  Status=', nic.status())
        print('  ifconfig=', nic.ifconfig())
        utime.sleep(1)

print('Connected. ifconfig=', nic.ifconfig())


from microWebSrv import MicroWebSrv

# ----------------------------------------------------------------------------

@MicroWebSrv.route('/test')
def _httpHandlerTestGet(httpClient, httpResponse) :
	content = """\
	<!DOCTYPE html>
	<html lang=en>
        <head>
        	<meta charset="UTF-8" />
            <title>TEST GET</title>
        </head>
        <body>
            <h1>TEST GET</h1>
            Client IP address = %s
            <br />
			<form action="/test" method="post" accept-charset="ISO-8859-1">
				First name: <input type="text" name="firstname"><br />
				Last name: <input type="text" name="lastname"><br />
				<input type="submit" value="Submit">
			</form>
        </body>
    </html>
	""" % httpClient.GetIPAddr()
	httpResponse.WriteResponseOk( headers		 = None,
								  contentType	 = "text/html",
								  contentCharset = "UTF-8",
								  content 		 = content )


@MicroWebSrv.route('/test', 'POST')
def _httpHandlerTestPost(httpClient, httpResponse) :
	formData  = httpClient.ReadRequestPostedFormData()
	firstname = formData["firstname"]
	lastname  = formData["lastname"]
	content   = """\
	<!DOCTYPE html>
	<html lang=en>
		<head>
			<meta charset="UTF-8" />
            <title>TEST POST</title>
        </head>
        <body>
            <h1>TEST POST</h1>
            Firstname = %s<br />
            Lastname = %s<br />
        </body>
    </html>
	""" % ( MicroWebSrv.HTMLEscape(firstname),
		    MicroWebSrv.HTMLEscape(lastname) )
	httpResponse.WriteResponseOk( headers		 = None,
								  contentType	 = "text/html",
								  contentCharset = "UTF-8",
								  content 		 = content )


@MicroWebSrv.route('/edit/<index>')             # <IP>/edit/123           ->   args['index']=123
@MicroWebSrv.route('/edit/<index>/abc/<foo>')   # <IP>/edit/123/abc/bar   ->   args['index']=123  args['foo']='bar'
@MicroWebSrv.route('/edit')                     # <IP>/edit               ->   args={}
def _httpHandlerEditWithArgs(httpClient, httpResponse, args={}) :
	content = """\
	<!DOCTYPE html>
	<html lang=en>
        <head>
        	<meta charset="UTF-8" />
            <title>TEST EDIT</title>
        </head>
        <body>
	"""
	content += "<h1>EDIT item with {} variable arguments</h1>"\
		.format(len(args))
	
	if 'index' in args :
		content += "<p>index = {}</p>".format(args['index'])
	
	if 'foo' in args :
		content += "<p>foo = {}</p>".format(args['foo'])
	
	content += """
        </body>
    </html>
	"""
	httpResponse.WriteResponseOk( headers		 = None,
								  contentType	 = "text/html",
								  contentCharset = "UTF-8",
								  content 		 = content )

# ----------------------------------------------------------------------------

def _acceptWebSocketCallback(webSocket, httpClient) :
	print("WS ACCEPT")
	webSocket.RecvTextCallback   = _recvTextCallback
	webSocket.RecvBinaryCallback = _recvBinaryCallback
	webSocket.ClosedCallback 	 = _closedCallback

def _recvTextCallback(webSocket, msg) :
	print("WS RECV TEXT : %s" % msg)
	webSocket.SendText("Reply for %s" % msg)

def _recvBinaryCallback(webSocket, data) :
	print("WS RECV DATA : %s" % data)

def _closedCallback(webSocket) :
	print("WS CLOSED")

# ----------------------------------------------------------------------------

#routeHandlers = [
#	( "/test",	"GET",	_httpHandlerTestGet ),
#	( "/test",	"POST",	_httpHandlerTestPost )
#]

srv = MicroWebSrv(webPath='www/')
srv.MaxWebSocketRecvLen     = 256
srv.WebSocketThreaded		= False
srv.AcceptWebSocketCallback = _acceptWebSocketCallback
srv.Start()

# ----------------------------------------------------------------------------
