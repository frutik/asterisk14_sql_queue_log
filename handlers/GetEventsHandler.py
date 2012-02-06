import tornado.web
import tornado
import time
import simplejson as json

from sqlobject import *

class QueueLog(SQLObject):
    time = StringCol()

    callid = StringCol()
    queuename = StringCol()
    agent = StringCol()
    event = StringCol()
    data = StringCol()

class GetEventsHandler(tornado.web.RequestHandler):

    schedule_time = 0.2
    current_handle = None

    @tornado.web.asynchronous
    def get(self, last_event_id):
        self.last_event_id = int(last_event_id)
        self.schedule_execution(self.schedule_time, self.loop)

    def schedule_execution(self, schedule_time, callback):
        self.handle = tornado.ioloop.IOLoop.instance().add_timeout(time.time() + schedule_time, callback)

    def loop(self):
        tornado.ioloop.IOLoop.instance().remove_timeout(self.handle)
	
	try:                                                                                                                                                                                   
	    events = QueueLog.select(QueueLog.q.id > self.last_event_id).orderBy('id').limit(1)
	
	except:                                                                                                                                                                 
	    self.schedule_execution(self.schedule_time, self.loop)
	    return 
	
	event = events[0]

	print event
	    
    self.write(json.dumps({
        'id': event.id,
        'callid': event.callid,
        'queuename': event.queuename,
        'agent': event.agent,
        'event': event.event,
        'data': event.data
    }))

    self.finish()

