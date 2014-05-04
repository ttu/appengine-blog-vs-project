Install:

Python 2.7
Google AppEngine SDK
jinja2
Requests-OAuthlib
???

Debugging:

You will get a ZipImportError exception.
This exception can be ignored and this is how you do that:
Open Debug->Exceptions... 
click the Add button.
Set type to "Python Exceptions" and in the name field write this:
google.appengine.dist.py_zipimport.ZipImportError 
click the OK button and uncheck the User-unhandled checkbox
click OK and continue execution.