from App import app
import recorder as rec
import webbrowser
from threading import Timer



# This function sets up the database first time it is run
rec.pre_record()

# The following three lines limit output to errors
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


port = 5000 # or simply open on the default `8050` port

def open_browser():
    webbrowser.open_new("http://localhost:{}".format(port))

if __name__ == '__main__':
    Timer(1, open_browser).start();
    app.run_server(debug=False, port=port)
            

       