from App import app
import recorder as rec


# This function sets up the database first time it is run
rec.pre_record()

# The following three lines limit output to errors
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

if __name__ == '__main__':  
    app.run_server(
        # host = '192.168.20.3',
        # port=8080,
        debug=False)
       