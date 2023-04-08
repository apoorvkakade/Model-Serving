# add our app to the system path
import sys
sys.path.insert(0, "/var/www/html/disml-project")
# import the application and away we go...
from web_server import app as application
