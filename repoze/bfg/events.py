import venusian

from zope.interface import implements

from repoze.bfg.interfaces import IAfterTraversal
from repoze.bfg.interfaces import INewRequest
from repoze.bfg.interfaces import INewResponse
from repoze.bfg.interfaces import IWSGIApplicationCreatedEvent

class subscriber(object):
    """ Decorator activated via a :term:`scan` which treats the
    function being decorated as an event subscriber for the set of
    interfaces passed as ``*ifaces`` to the decorator constructor.

    For example:

    .. code-block:: python
    
       from repoze.bfg.interfaces import INewRequest
       from repoze.bfg.events import subscriber

       @subscriber(INewRequest)
       def mysubscriber(event):
           event.request.foo = 1

    More than one event type can be passed as a construtor argument:
        
    .. code-block:: python
    
       from repoze.bfg.interfaces import INewRequest
       from repoze.bfg.events import subscriber

       @subscriber(INewRequest, INewResponse)
       def mysubscriber(event):
           print event

    When the ``subscriber`` decorator is used without passing an arguments,
    the function it decorates is called for every event sent:

    .. code-block:: python
    
       from repoze.bfg.interfaces import INewRequest
       from repoze.bfg.events import subscriber

       @subscriber()
       def mysubscriber(event):
           print event

    This method will have no effect until a :term:`scan` is performed
    against the package or module which contains it, ala:

    .. code-block:: python
    
       from repoze.bfg.configuration import Configurator
       config = Configurator()
       config.scan('somepackage_containing_subscribers')

    """
    venusian = venusian # for unit testing

    def __init__(self, *ifaces):
        self.ifaces = ifaces

    def register(self, scanner, name, wrapped):
        config = scanner.config
        config.add_subscriber(wrapped, self.ifaces)

    def __call__(self, wrapped):
        self.venusian.attach(wrapped, self.register, category='bfg')
        return wrapped

class NewRequest(object):
    """ An instance of this class is emitted as an :term:`event`
    whenever :mod:`repoze.bfg` begins to process a new request.  The
    instance has an attribute, ``request``, which is a :term:`request`
    object.  This class implements the
    :class:`repoze.bfg.interfaces.INewRequest` interface."""
    implements(INewRequest)
    def __init__(self, request):
        self.request = request

class NewResponse(object):
    """ An instance of this class is emitted as an :term:`event`
    whenever any :mod:`repoze.bfg` view returns a :term:`response`.
    The instance has an attribute, ``response``, which is the response
    object returned by the view.  This class implements the
    :class:`repoze.bfg.interfaces.INewResponse` interface.

    .. note::

       Postprocessing a response is usually better handled in a WSGI
       :term:`middleware` component than in subscriber code that is
       called by a :class:`repoze.bfg.interfaces.INewResponse` event.
       The :class:`repoze.bfg.interfaces.INewResponse` event exists
       almost purely for symmetry with the
       :class:`repoze.bfg.interfaces.INewRequest` event.
    """
    implements(INewResponse)
    def __init__(self, response):
        self.response = response

class AfterTraversal(object):
    implements(IAfterTraversal)
    """ An instance of this class is emitted as an :term:`event` after
    the :mod:`repoze.bfg` :term:`router` performs traversal but before
    any view code is executed.  The instance has an attribute,
    ``request``, which is the request object generated by
    :mod:`repoze.bfg`.  Notably, the request object will have an
    attribute named ``context``, which is the context that will be
    provided to the view which will eventually be called, as well as
    other attributes defined by the traverser.  This class implements
    the :class:`repoze.bfg.interfaces.IAfterTraversal` interface."""
    def __init__(self, request):
        self.request = request
    
class WSGIApplicationCreatedEvent(object):    
    """ An instance of this class is emitted as an :term:`event` when
    the :meth:`repoze.bfg.configuration.Configurator.make_wsgi_app` is
    called.  The instance has an attribute, ``app``, which is an
    instance of the :term:`router` that will handle WSGI requests.
    This class implements the
    :class:`repoze.bfg.interfaces.IWSGIApplicationCreatedEvent`
    interface."""
    implements(IWSGIApplicationCreatedEvent)
    def __init__(self, app):
        self.app = app
        self.object = app

