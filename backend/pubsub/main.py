import webapp2
import json
import logging
import urllib
import base64
import pytz
import datetime
from models.models import *

from google.cloud import bigquery

import asu_constants


class ASUTestHandler(webapp2.RequestHandler):
    def get(self):
        self.response.headers.add_header("Access-Control-Allow-Origin", "*")
        self.response.write("TEST")


class ReceiveMessage(webapp2.RequestHandler):
    """A handler for push subscription endpoint.."""

    def post(self):
        if asu_constants.SUBSCRIPTION_UNIQUE_TOKEN != self.request.get('token'):
            self.response.status = 404
            return

        try:
            message = json.loads(urllib.unquote(self.request.body).rstrip('='))
            logging.info("MESSAGE")
            logging.info(message)
            controller_id = message['message']['attributes']['deviceId']
            message_body = base64.b64decode(str(message['message']['data']))
            logging.info("MESSAGE BODY")
            logging.info(message_body)
            data = json.loads(message_body)
            logging.info("DATA")
            logging.info(data)

            datetime_r = pytz.timezone('America/Phoenix').localize(
                datetime.datetime.strptime(data['timestamp'].strip(), "%Y-%m-%dT%H:%M:%S.%f"))
            nonaware_datetime_r = datetime_r.replace(tzinfo=None) - datetime_r.utcoffset()

            location = data['location']
            ph = data['ph']
            temperature = data['temperature']
            ec = data['ec']

        except:
            self.response.status = 200
            logging.info("ERROR")
            self.response.write('ERROR')

        r = Data.create_and_store(
            timestamp=nonaware_datetime_r,
            controller_id=controller_id,
            location=location,
            temperature=temperature,
            ec=ec,
            ph=ph
        )
        if r == True:
            self.response.status = 200
            logging.info('SUCCESS')
        else:
            self.response.status = 200
            logging.info('FAILURE')


class MyEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.datetime):
            return o.strftime("%y-%m-%d (%H:%M:00.000)MST")
        return json.JSONEncoder.default(self, o)


class GetData(webapp2.RequestHandler):
    def get(self):
        controller_id = str(self.request.get('controller_id'))
        data = Data.query().filter(Data.controller_id == controller_id).order(-Data.timestamp).fetch(limit=12)
        dict_data = []
        for t in data:
            datetime_r = pytz.timezone('America/Phoenix').localize(t.timestamp)
            nonaware_datetime_r = datetime_r.replace(tzinfo=None) + datetime_r.utcoffset()
            dict_data.append(
                {'timestamp': nonaware_datetime_r, 'controller_id': t.controller_id, 'ec': t.ec, 'ph': t.ph,
                 'temperature': t.temperature, 'location': t.location})
        json_data = json.dumps(dict_data, cls=MyEncoder)
        self.response.headers.add_header("Access-Control-Allow-Origin", "*")
        self.response.headers['Content-Type'] = 'application/json; charset=utf-8'
        self.response.out.write(json_data)


class MyEncoder1(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.date):
            return o.strftime("%y-%m-%d %H:%M:%S UTC")
        return json.JSONEncoder.default(self, o)


class GetDataHourly(webapp2.RequestHandler):
    def get(self):
        controller_id = str(self.request.get('controller_id'))
        from requests_toolbelt.adapters import appengine
        appengine.monkeypatch()
        client = bigquery.Client()
        query_job = client.query(asu_constants.QUERY_HOURLY.format(controller_id))
        results = query_job.result()
        rows = list(results)
        dict_data = []
        for i in range(len(rows)):
            dict_data.append({'controller_id': rows[i][0], 'hour_number': rows[i][1], 'Average_temp': rows[i][2],
                              'Average_ph': rows[i][3], 'Average_ec': rows[i][4]})
        json_data = json.dumps(dict_data, cls=MyEncoder1)
        self.response.headers.add_header("Access-Control-Allow-Origin", "*")
        self.response.headers['Content-Type'] = 'application/json; charset=utf-8'
        self.response.out.write(json_data)


class GetDataDaily(webapp2.RequestHandler):
    def get(self):
        controller_id = str(self.request.get('controller_id'))
        from requests_toolbelt.adapters import appengine
        appengine.monkeypatch()
        client = bigquery.Client()
        query_job = client.query(asu_constants.QUERY_WEEKLY.format(controller_id))
        results = query_job.result()
        rows = list(results)
        dict_data = []
        for i in range(len(rows)):
            dict_data.append({'controller_id': rows[i][0], 'hour_number': rows[i][1], 'Average_temp': rows[i][2],
                              'Average_ph': rows[i][3], 'Average_ec': rows[i][4]})
        json_data = json.dumps(dict_data, cls=MyEncoder1)
        self.response.headers.add_header("Access-Control-Allow-Origin", "*")
        self.response.headers['Content-Type'] = 'application/json; charset=utf-8'
        self.response.out.write(json_data)


class GetDataWeekly(webapp2.RequestHandler):
    def get(self):
        controller_id = str(self.request.get('controller_id'))
        from requests_toolbelt.adapters import appengine
        appengine.monkeypatch()
        client = bigquery.Client()
        query_job = client.query(asu_constants.QUERY_EIGHT_WEEKLY.format(controller_id))
        results = query_job.result()
        rows = list(results)
        dict_data = []
        for i in range(len(rows)):
            dict_data.append({'controller_id': rows[i][0], 'hour_number': rows[i][1], 'Average_ph': rows[i][2],
                              'Average_ec': rows[i][3], 'Average_temp': rows[i][4]})
        json_data = json.dumps(dict_data, cls=MyEncoder1)
        self.response.headers.add_header("Access-Control-Allow-Origin", "*")
        self.response.headers['Content-Type'] = 'application/json; charset=utf-8'
        self.response.out.write(json_data)


class SendDataBigQuery(webapp2.RequestHandler):
    def post(self):
        if asu_constants.SUBSCRIPTION_UNIQUE_TOKEN != self.request.get('token'):
            self.response.status = 404
            return
        try:
            message = json.loads(urllib.unquote(self.request.body).rstrip('='))
            logging.info("MESSAGE")
            logging.info(message)
            controller_id = message['message']['attributes']['deviceId']
            message_body = base64.b64decode(str(message['message']['data']))
            logging.info("MESSAGE BODY")
            logging.info(message_body)
            data = json.loads(message_body)
            logging.info("DATA")
            logging.info(data)
            datetime_r = pytz.timezone('America/Phoenix').localize(
                datetime.datetime.strptime(data['timestamp'].strip(), "%Y-%m-%dT%H:%M:%S.%f"))
            nonaware_datetime_r = datetime_r.replace(tzinfo=None) - datetime_r.utcoffset()

            location = data['location']
            ph = data['ph']
            temperature = data['temperature']
            ec = data['ec']
            rows_to_insert = [(nonaware_datetime_r, controller_id, location, ph, ec, temperature)]
        except:
            self.response.status = 200
            logging.info("ERROR")
            self.response.write('ERROR')

        from requests_toolbelt.adapters import appengine
        appengine.monkeypatch()

        client = bigquery.Client()
        dummy = client.get_table(asu_constants.TABLE_NAME)
        client.insert_rows(asu_constants.TABLE_NAME, rows_to_insert, selected_fields=dummy.schema)
        self.response.status = 200
        logging.info('SUCCESS')


class TimestampQueryAvg(webapp2.RequestHandler):
    def get(self):
        from requests_toolbelt.adapters import appengine
        appengine.monkeypatch()
        controller = str(self.request.get('controller_id'))
        t1 = str(self.request.get('t1'))
        t2 = str(self.request.get('t2'))
        # controller = 'controller1'
        #t1 = '2019-04-29T18:00:04.291333'
        #t2 = '2019-04-30T18:00:04.291333'
        client = bigquery.Client()
        query_job = client.query(
            asu_constants.QUERY_AVG.format(controller, t1, t2, controller, t1, t2, controller, t1, t2))
        results = query_job.result()
        rows = list(results)
        dict_data = []
        for i in range(len(rows)):
            dict_data.append({'Column': rows[i][0], 'value': rows[i][1]})
        json_data = json.dumps(dict_data)
        self.response.headers.add_header("Access-Control-Allow-Origin", "*")
        self.response.headers['Content-Type'] = 'application/json; charset=utf-8'
        self.response.out.write(json_data)


class MyEncoder2(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.date):
            return o.strftime("%y-%m-%dT%H:%M:%S.%f")
        return json.JSONEncoder.default(self, o)


class TimestampQueryMax(webapp2.RequestHandler):
    def get(self):
        from requests_toolbelt.adapters import appengine
        appengine.monkeypatch()
        controller = str(self.request.get('controller_id'))
        t1 = str(self.request.get('t1'))
        t2 = str(self.request.get('t2'))
        #controller = 'controller1'
        #t1 = '2019-04-29T18:00:04.291333'
        #t2 = '2019-04-30T18:00:04.291333'
        client = bigquery.Client()
        query_job = client.query(
            asu_constants.QUERY_MAX.format(controller, t1, t2, controller, controller, t1, t2, controller, controller,
                                           t1, t2, controller))
        results = query_job.result()
        rows = list(results)
        dict_data = []
        for i in range(len(rows)):
            dict_data.append({'Column': rows[i][0], 'DATE': rows[i][1], 'value': rows[i][2]})
        json_data = json.dumps(dict_data, cls=MyEncoder2)
        self.response.headers.add_header("Access-Control-Allow-Origin", "*")
        self.response.headers['Content-Type'] = 'application/json; charset=utf-8'
        self.response.out.write(json_data)


class TimestampQueryMin(webapp2.RequestHandler):
    def get(self):
        from requests_toolbelt.adapters import appengine
        appengine.monkeypatch()
        controller = str(self.request.get('controller_id'))
        t1 = str(self.request.get('t1'))
        t2 = str(self.request.get('t2'))
        #controller = 'controller1'
        #t1 = '2019-04-29T18:00:04.291333'
        #t2 = '2019-04-30T18:00:04.291333'
        client = bigquery.Client()
        query_job = client.query(
            asu_constants.QUERY_MIN.format(controller, t1, t2, controller, controller, t1, t2, controller, controller,
                                           t1, t2, controller))
        results = query_job.result()
        rows = list(results)
        dict_data = []
        for i in range(len(rows)):
            dict_data.append({'Column': rows[i][0], 'DATE': rows[i][1], 'value': rows[i][2]})
        json_data = json.dumps(dict_data, cls=MyEncoder2)
        self.response.headers.add_header("Access-Control-Allow-Origin", "*")
        self.response.headers['Content-Type'] = 'application/json; charset=utf-8'
        self.response.out.write(json_data)


class TimestampQuery(webapp2.RequestHandler):
    def get(self):
        from requests_toolbelt.adapters import appengine
        appengine.monkeypatch()
        controller = str(self.request.get('controller_id'))
        t1 = str(self.request.get('t1'))
        t2 = str(self.request.get('t2'))
        client = bigquery.Client()
        query_job = client.query(
            asu_constants.QUERY.format(controller, t1, t2))
        results = query_job.result()
        rows = list(results)
        dict_data = []
        for i in range(len(rows)):
            dict_data.append({'timestamp': rows[i][0], 'controller_id': rows[i][1], 'ph': rows[i][2], 'ec': rows[i][3], 'temperature': rows[i][4]})
        json_data = json.dumps(dict_data, cls=MyEncoder2)
        self.response.headers.add_header("Access-Control-Allow-Origin", "*")
        self.response.headers['Content-Type'] = 'application/json; charset=utf-8'
        self.response.out.write(json_data)



app = webapp2.WSGIApplication(
    [
        ('/pubsub/test', ASUTestHandler),
        ('/pubsub/receive_message', ReceiveMessage),
        ('/pubsub/data_to_bq', SendDataBigQuery),
        ('/pubsub/data', GetData),
        ('/pubsub/hourly', GetDataHourly),
        ('/pubsub/daily', GetDataDaily),
        ('/pubsub/weekly', GetDataWeekly),
        ('/pubsub/timestamp_avg', TimestampQueryAvg),
        ('/pubsub/timestamp_max', TimestampQueryMax),
        ('/pubsub/timestamp_min', TimestampQueryMin),
        ('/pubsub/timestamp', TimestampQuery),
    ], debug=True)
