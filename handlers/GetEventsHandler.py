import tornado.web
import tornado
import time

class GetEventsHandler(tornado.web.RequestHandler):

    schedule_time = 0.2
    current_handle = None

    @tornado.web.asynchronous
    def get(self, last_event_id):
        self.last_event_id = last_event_id
        self.schedule_execution(self.schedule_time, self.loop)

    def schedule_execution(self, schedule_time, callback):
        self.handle = tornado.ioloop.IOLoop.instance().add_timeout(time.time() + schedule_time, callback)

    def loop(self):
        tornado.ioloop.IOLoop.instance().remove_timeout(self.handle)

        self.write('test' + self.last_event_id)

        self.finish()
#        session = self._get_session()
#
#        if session:
#            message = session.queue_next()
#
#            if message:
#                self.finish_with_message(message)
#            else:
#                if time.time() - self.start_time < self.timeout:
#                    self.schedule_execution(self.time_schedule, self.loop)
#                else:
#                    status = Status()
#                    status.message = 'Timeout'
#
#                    self.finish_with_message(status)

