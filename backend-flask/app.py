from flask import Flask
from flask import request
from flask_cors import CORS, cross_origin
import os

from services.home_activities import *
from services.notifications_activities import *
from services.user_activities import *
from services.create_activity import *
from services.create_reply import *
from services.search_activities import *
from services.message_groups import *
from services.messages import *
from services.create_message import *
from services.show_activity import *

# Honeycomb for observability """

from opentelemetry import trace
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.trace.export import ConsoleSpanExporter
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
#from opentelemetry.exporter.honeycomb import HoneycombSpanExporter
#from opentelemetry.ext.honeycomb import HoneycombSpanExporter

# X-RAY ---------
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.ext.flask.middleware import XRayMiddleware



# Instrument Honeycomb for the frontend-application to observe network latency between frontend and backend[HARD]_challenge
import libhoney
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# instrument: Set up the Honeycomb exporter:_homework challenge

honeycomb_key = os.environ.get("HONEYCOMB_API_KEY")
honeycomb_dataset = os.environ.get("HONEYCOMB_DATASET")
#exporter1 = HoneycombSpanExporter(
 #   service_name="test-service",
  #  writekey=honeycomb_key,
   # dataset=honeycomb_dataset,
#)


# Honeycomb
# Initialize tracing and an exporter that can send data to Honeycomb
provider = TracerProvider()
processor = BatchSpanProcessor(OTLPSpanExporter())
provider.add_span_processor(processor)

# X_RAY ---------
xray_url = os.getenv("AWS_XRAY_URL")
xray_recorder.configure(service='backend-flask', dynamic_naming=xray_url)


# Show log within the backend flask STDOUT honeycomb

simple_processor = SimpleSpanProcessor(ConsoleSpanExporter())
provider.add_span_processor(simple_processor)

#adding
#trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(exporter1))

trace.set_tracer_provider(provider)
tracer = trace.get_tracer(__name__)


#tracer = trace.get_tracer(__name__)

#with tracer.start_as_current_span('span_one'):
 #   with tracer.start_as_current_span('span_two'):
  #      with tracer.start_as_current_span('span_three'):
   #         print("Hello, from a child span")


app = Flask(__name__)
# X-RAY ------------
XRayMiddleware(app, xray_recorder)

# Honecomb instrument_homework challenge

@app.route('/')
def index():
    with tracer.start_as_current_span('frontend-request'):
        response = requests.get('https://4567-olaadesam-awsbootcampcr-81kgeozzzwr.ws-us92.gitpod.io:4567')

        #response = requests.get('http://backend-service')
    return response.text


#Honeycomb ... 
# Initialize automatic instrumentation with Flask

FlaskInstrumentor().instrument_app(app)
RequestsInstrumentor().instrument()

#challenge
#RequestsInstrumentor().instrument(tracer_provider=trace.get_tracer_provider())


#Challenge
#honeycomb_client = libhoney.Client(writekey=honeycomb_key, dataset=honeycomb_dataset)

def on_span_end(span):
    if span.name == 'frontend-request':
        latency_ms = span.end_time - span.start_time
        event = {
            'type': 'frontend-request',
            'duration_ms': latency_ms / 1000000,
        }
        honeycomb_client.send_now(event)

#trace.get_tracer_provider().add_span_processor(libhoney.SpanProcessor(on_span_end=on_span_end))



frontend = os.getenv('FRONTEND_URL')
backend = os.getenv('BACKEND_URL')
origins = [frontend, backend]
cors = CORS(
  app, 
  resources={r"/api/*": {"origins": origins}},
  expose_headers="location,link",
  allow_headers="content-type,if-modified-since",
  methods="OPTIONS,GET,HEAD,POST"
)

@app.route("/api/message_groups", methods=['GET'])
def data_message_groups():
  user_handle  = 'andrewbrown'
  model = MessageGroups.run(user_handle=user_handle)
  if model['errors'] is not None:
    return model['errors'], 422
  else:
    return model['data'], 200

@app.route("/api/messages/@<string:handle>", methods=['GET'])
def data_messages(handle):
  user_sender_handle = 'andrewbrown'
  user_receiver_handle = request.args.get('user_reciever_handle')

  model = Messages.run(user_sender_handle=user_sender_handle, user_receiver_handle=user_receiver_handle)
  if model['errors'] is not None:
    return model['errors'], 422
  else:
    return model['data'], 200
  return

@app.route("/api/messages", methods=['POST','OPTIONS'])
@cross_origin()
def data_create_message():
  user_sender_handle = 'andrewbrown'
  user_receiver_handle = request.json['user_receiver_handle']
  message = request.json['message']

  model = CreateMessage.run(message=message,user_sender_handle=user_sender_handle,user_receiver_handle=user_receiver_handle)
  if model['errors'] is not None:
    return model['errors'], 422
  else:
    return model['data'], 200
  return

@app.route("/api/activities/home", methods=['GET'])
def data_home():
  data = HomeActivities.run()
  return data, 200

@app.route("/api/activities/notifications", methods=['GET'])
def data_notifications():
  data = NotificationsActivities.run()
  return data, 200

@app.route("/api/activities/@<string:handle>", methods=['GET'])
def data_handle(handle):
  model = UserActivities.run(handle)
  if model['errors'] is not None:
    return model['errors'], 422
  else:
    return model['data'], 200

@app.route("/api/activities/search", methods=['GET'])
def data_search():
  term = request.args.get('term')
  model = SearchActivities.run(term)
  if model['errors'] is not None:
    return model['errors'], 422
  else:
    return model['data'], 200
  return

@app.route("/api/activities", methods=['POST','OPTIONS'])
@cross_origin()
def data_activities():
  user_handle  = 'andrewbrown'
  message = request.json['message']
  ttl = request.json['ttl']
  model = CreateActivity.run(message, user_handle, ttl)
  if model['errors'] is not None:
    return model['errors'], 422
  else:
    return model['data'], 200
  return

@app.route("/api/activities/<string:activity_uuid>", methods=['GET'])
def data_show_activity(activity_uuid):
  data = ShowActivity.run(activity_uuid=activity_uuid)
  return data, 200

@app.route("/api/activities/<string:activity_uuid>/reply", methods=['POST','OPTIONS'])
@cross_origin()
def data_activities_reply(activity_uuid):
  user_handle  = 'andrewbrown'
  message = request.json['message']
  model = CreateReply.run(message, user_handle, activity_uuid)
  if model['errors'] is not None:
    return model['errors'], 422
  else:
    return model['data'], 200
  return

if __name__ == "__main__":
  app.run(debug=True)