from flask import Flask,request 
from routes.booking_routes import (
    get_all_rooms,
    get_room_by_id,
    submit_booking_request,
    get_all_booking_requests,
    get_booking_request_by_id,
    get_alternative_room_v2,
    get_all_notifications,
    get_notification_by_id,
    get_alternative_room_v2,
    get_negotiation_candidates,
    #create_negotiation_case_route,
    get_all_negotiation_cases,
    respond_to_negotiation_case,
    process_negotiation_decision,
    process_admin_decision,
    process_superadmin_decision,
    workflow_summary,
    get_notifications,
    get_available_slots,
    check_custom_availability,
    create_booking
)
from flask_cors import CORS

app = Flask(__name__)

CORS(
    app,
    
)

@app.route('/')
def home():
    return "Room Booking Backend Running Successfully"


@app.route('/rooms')
def rooms():
    return get_all_rooms()



@app.route('/rooms/<int:room_id>')
def room_details(room_id):
    return get_room_by_id(room_id)


@app.route('/booking-request', methods=['POST'])
def booking_request():
    return submit_booking_request()


@app.route('/booking-requests')
def booking_requests():
    return get_all_booking_requests()



@app.route('/booking-requests/<int:request_id>')
def booking_request_details(request_id):
    return get_booking_request_by_id(request_id)



@app.route(
    '/alternative-room',
    methods=['POST']
)
def alternative_room():

    data = request.get_json()

    return get_alternative_room_v2(
        data['participant_count'],
        data['booking_date'],
        data['start_time'],
        data['end_time']
    )


@app.route('/notifications')
def notifications():
    return get_all_notifications()


@app.route('/notifications/<int:notification_id>')
def notification_details(
    notification_id
):

    return get_notification_by_id(
        notification_id
    )


@app.route(
    '/negotiation-candidates',
    methods=['POST']
)
def negotiation_candidates():
    return get_negotiation_candidates()


'''@app.route(
    '/create-negotiation-case',
    methods=['POST']
)
def create_negotiation_case():
    return create_negotiation_case_route()
'''

@app.route('/negotiation-cases')
def negotiation_cases():
    return get_all_negotiation_cases()



@app.route(
    '/negotiation-response',
    methods=['POST']
)
def negotiation_response():
    return respond_to_negotiation_case()


@app.route(
    '/process-negotiation-decision',
    methods=['POST']
)
def process_decision():
    return process_negotiation_decision()


app.add_url_rule(
    '/process-admin-decision',
    view_func=process_admin_decision,
    methods=['POST']
)


app.add_url_rule(
    '/process-superadmin-decision',
    view_func=process_superadmin_decision,
    methods=['POST']
)

app.add_url_rule(
    '/workflow-summary',
    view_func=workflow_summary,
    methods=['GET']
)

app.add_url_rule(
    '/notifications',
    view_func=get_notifications,
    methods=['GET']
)



@app.route(
    '/available-slots/<int:room_id>/<booking_date>'
)
def available_slots(
    room_id,
    booking_date
):

    return get_available_slots(
        room_id,
        booking_date
    )


@app.route(
    '/check-availability',
    methods=['POST']
)
def check_availability():

    data = request.get_json()

    return check_custom_availability(
        data['room_id'],
        data['booking_date'],
        data['start_time'],
        data['end_time']
    )


@app.route(
    '/book-room',
    methods=['POST']
)
def book_room():
    return create_booking()


if __name__ == '__main__':
    app.run(debug=True)




