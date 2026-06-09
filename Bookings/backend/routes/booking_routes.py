from flask import jsonify, request
from database import get_connection
from utils.json_encoder import serialize_data
from services.notification_service import create_notification

def get_all_rooms():
    
    try:

        conn = get_connection()

        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM resources"
        )

        rooms = cursor.fetchall()

        cursor.close()

        conn.close()

        return jsonify(rooms)

    except Exception as e:

        return jsonify({
            "error": str(e)
        })



def get_all_booking_requests():
    
    try:

        conn = get_connection()

        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT *
            FROM booking_requests
            ORDER BY priority_score DESC
        """)

        requests = serialize_data(
            cursor.fetchall()
        )

        cursor.close()
        conn.close()

        return jsonify(requests)

    except Exception as e:

        return jsonify({
            "error": str(e)
        })
    
    

def get_room_by_id(room_id):

    try:

        conn = get_connection()

        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM resources WHERE resource_id = %s",
            (room_id,)
        )

        room = cursor.fetchone()
        if not room:
            cursor.close()
            conn.close()
            return jsonify({
                "error": "Room not found"
            }), 404

        cursor.close()
        conn.close()

        return jsonify(room)

    except Exception as e:

        return jsonify({
            "error": str(e)
        })
    


def submit_booking_request():
    
    try:

        data = request.get_json()

        conn = get_connection()

        cursor = conn.cursor()

        cursor.callproc(
            'submit_booking_request',
            [
                data['booking_id'],
                data['requester_id'],
                data['requester_type'],
                data['event_name'],
                data['purpose'],
                data['event_category'],
                data['participant_count'],
                data['request_reason'],
                data['resource_id'],
                data['booking_date'],
                data['start_time'],
                data['end_time']
            ]
        )

        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({
            "message": "Booking Request Submitted Successfully"
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        })
    

    

def get_booking_request_by_id(request_id):
    
    try:

        conn = get_connection()

        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT *
            FROM booking_requests
            WHERE request_id = %s
            """,
            (request_id,)
        )

        request_data = cursor.fetchone()
        if not request_data:
            cursor.close()
            conn.close()
            return jsonify({
                "error": "Booking request not found"
            }), 404

        request_data = serialize_data(request_data)

        cursor.close()
        conn.close()

        return jsonify(request_data)

    except Exception as e:

        return jsonify({
            "error": str(e)
        })
    


def get_alternative_room_v2(
    participant_count,
    booking_date,
    start_time,
    end_time
):

    try:

        conn = get_connection()

        cursor = conn.cursor(dictionary=True)

        cursor.callproc(
            'find_best_alternative_room_v2',
            [
                participant_count,
                booking_date,
                start_time,
                end_time
            ]
        )

        result = None

        for res in cursor.stored_results():

            result = res.fetchone()

        result = serialize_data(result)

        cursor.close()
        conn.close()

        return jsonify(result)

    except Exception as e:

        return jsonify({
            "error": str(e)
        })
    


def get_all_notifications():
    
    try:

        conn = get_connection()

        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT *
            FROM notifications
            ORDER BY notification_id DESC
        """)

        notifications = serialize_data(
            cursor.fetchall()
        )

        cursor.close()
        conn.close()

        return jsonify(notifications)

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500
    


def get_notification_by_id(notification_id):
    
    try:

        conn = get_connection()

        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT *
            FROM notifications
            WHERE notification_id = %s
            """,
            (notification_id,)
        )

        notification = cursor.fetchone()

        if not notification:

            cursor.close()
            conn.close()

            return jsonify({
                "error": "Notification not found"
            }), 404

        notification = serialize_data(
            notification
        )

        cursor.close()
        conn.close()

        return jsonify(notification)

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500
    


def get_negotiation_candidates():
    
    try:

        data = request.get_json()

        conn = get_connection()

        cursor = conn.cursor(dictionary=True)

        cursor.callproc(
            'find_negotiation_candidates_v2',
            [
                data['priority_score'],
                data['participant_count'],
                data['booking_date'],
                data['start_time'],
                data['end_time']
            ]
        )

        results = []

        for result in cursor.stored_results():

            results = result.fetchall()

        results = serialize_data(results)

        cursor.close()
        conn.close()

        return jsonify(results)

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500
    

'''def create_negotiation_case_route():
    
    try:

        data = request.get_json()

        conn = get_connection()

        cursor = conn.cursor()

        cursor.callproc(
            'create_negotiation_case',
            [
                data['booking_id'],
                data['request_id']
            ]
        )

        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({
            "message":
            "Negotiation Case Created Successfully"
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500
'''


def create_notification():
    
    try:

        data = request.get_json()

        conn = get_connection()
        cursor = conn.cursor()

        query = """
        INSERT INTO notifications(
            case_id,
            receiver_id,
            notification_type,
            message,
            receiver_role
        )
        VALUES(
            %s,%s,%s,%s,%s
        )
        """

        values = (
            data["case_id"],
            data["receiver_id"],
            "System",
            data["message"],
            data["receiver_role"]
        )

        cursor.execute(query, values)

        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({
            "message": "Notification Sent"
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        })


def get_all_negotiation_cases():
    
    try:

        conn = get_connection()

        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT *
            FROM negotiation_cases
            ORDER BY case_id DESC
        """)

        cases = serialize_data(
            cursor.fetchall()
        )

        cursor.close()
        conn.close()

        return jsonify(cases)

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500



def respond_to_negotiation_case():
    
    try:

        data = request.get_json()

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE negotiation_cases
            SET case_status = %s
            WHERE case_id = %s
            """,
            (
                data['response'],
                data['case_id']
            )
        )

        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({
            "message":
            "Negotiation response recorded"
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500
    



def process_negotiation_decision():
    
    try:

        data = request.get_json()

        case_id = data['case_id']
        if case_id <= 0:
            return jsonify({
                "error": "Invalid case_id"
            }), 400
        decision = data['decision']

        
        if decision not in [
            'Approved',
            'Rejected'
        ]:

            return jsonify({
                "error": "Invalid decision. Use Approved or Rejected."
            }), 400
        
        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT case_id
            FROM negotiation_cases
            WHERE case_id = %s
            """,
            (case_id,)
        )

        case_exists = cursor.fetchone()

        if not case_exists:

            cursor.close()
            conn.close()

            return jsonify({
                "error": "Negotiation case not found"
            }), 404
        
        cursor.execute(
            """
            SELECT request_id
            FROM negotiation_cases
            WHERE case_id = %s
            """,
            (case_id,)
        )

        request_id = cursor.fetchone()[0]

        if decision == "Approved":

            cursor.execute(
                """
                UPDATE negotiation_cases
                SET
                    case_status = 'Resolved',
                    final_decision = 'Approved'
                WHERE case_id = %s
                """,
                (case_id,)
            )

            cursor.execute(
                """
                UPDATE booking_requests
                SET
                    request_status = 'Approved',
                    negotiation_status = 'Accepted'
                WHERE request_id = %s
                """,
                (request_id,)
            )

        elif decision == "Rejected":
    
            cursor.execute(
                """
                SELECT booking_id
                FROM negotiation_cases
                WHERE case_id = %s
                """,
            (case_id,)
            )

            booking_id = cursor.fetchone()[0]

            cursor.execute(
                """
                INSERT INTO negotiation_history(

                    request_id,
                    booking_id,
                    response

                )

                VALUES(

                    %s,
                    %s,
                    'Rejected'

                )
                """,
                (
                    request_id,
                    booking_id
                )
            )

            cursor.execute(
                """
                UPDATE booking_requests
                SET
                    negotiation_status = 'Rejected',
                    negotiation_attempts =
                        negotiation_attempts + 1
                WHERE request_id = %s
                """,
                (request_id,)
            )
            next_candidate = find_next_candidate(
                request_id
            )

            if next_candidate is None:
    
                cursor.execute(
                    """
                    UPDATE negotiation_cases
                    SET escalation_stage = 2
                    WHERE case_id = %s
                    """,
                    (case_id,)
                )

                conn.commit()
                
                create_notification(
                    case_id,
                    'ADMIN001',
                    'System',
                    'Negotiation requires admin review'
                )

            else:

                print(
                    "Candidate Found:"
                )

                print(
                    next_candidate
                )
            cursor.execute(
                """
                UPDATE negotiation_cases
                SET
                    final_decision = 'Rejected'
                WHERE case_id = %s
                """,
                (case_id,)
            )

        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({
            "message":
            "Negotiation decision processed"
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500
    

def find_next_candidate(request_id):
    
    conn = get_connection()

    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT

            priority_score,
            participant_count,
            booking_date,
            start_time,
            end_time

        FROM booking_requests

        WHERE request_id = %s
        """,
        (request_id,)
    )

    request_data = cursor.fetchone()

    cursor.callproc(
        'find_next_negotiation_candidate_v1',
        [
            request_id,
            request_data['priority_score'],
            request_data['participant_count'],
            request_data['booking_date'],
            request_data['start_time'],
            request_data['end_time']
        ]
    )

    result = None

    for res in cursor.stored_results():

        result = res.fetchone()

    cursor.close()
    conn.close()

    return result



def process_admin_decision():
    
    try:

        data = request.get_json()

        case_id = data['case_id']

        if case_id <= 0:

            return jsonify({
                "error": "Invalid case_id"
            }), 400

        decision = data['decision']

        if decision not in [
            'Approved',
            'Rejected'
        ]:

            return jsonify({
                "error":
                "Invalid decision. Use Approved or Rejected."
            }), 400

        # ADD THE CASE EXISTS CHECK HERE

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT case_id
            FROM negotiation_cases
            WHERE case_id = %s
            """,
            (case_id,)
        )

        case_exists = cursor.fetchone()

        if not case_exists:

            cursor.close()
            conn.close()

            return jsonify({
                "error": "Negotiation case not found"
            }), 404

        cursor.execute(
            """
            SELECT request_id
            FROM negotiation_cases
            WHERE case_id = %s
            """,
            (case_id,)
        )

        request_id = cursor.fetchone()[0]

        if decision == "Approved":

            cursor.execute(
                """
                UPDATE negotiation_cases
                SET
                    case_status = 'Resolved',
                    final_decision = 'Approved'
                WHERE case_id = %s
                """,
                (case_id,)
            )

            cursor.execute(
                """
                UPDATE booking_requests
                SET
                    request_status = 'Approved',
                    negotiation_status = 'Accepted'
                WHERE request_id = %s
                """,
                (request_id,)
            )
        elif decision == "Rejected":
    
            cursor.execute(
                """
                UPDATE negotiation_cases
                SET
                    escalation_stage = 3
                WHERE case_id = %s
                """,
                (case_id,)
            )

            conn.commit()

            create_notification(
                case_id,
                'SUPERADMIN001',
                'System',
                'Admin rejected negotiation case'
            )

        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({
            "message": "Admin decision processed"
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500
    


def process_superadmin_decision():
    
    try:

        data = request.get_json()

        case_id = data['case_id']

        if case_id <= 0:

            return jsonify({
                "error": "Invalid case_id"
            }), 400

        decision = data['decision']

        if decision not in [
            'Approved',
            'Rejected'
        ]:

            return jsonify({
                "error":
                "Invalid decision. Use Approved or Rejected."
            }), 400

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT case_id
            FROM negotiation_cases
            WHERE case_id = %s
            """,
            (case_id,)
        )

        case_exists = cursor.fetchone()

        if not case_exists:

            cursor.close()
            conn.close()

            return jsonify({
                "error": "Negotiation case not found"
            }), 404

        cursor.execute(
            """
            SELECT request_id
            FROM negotiation_cases
            WHERE case_id = %s
            """,
            (case_id,)
        )

        request_id = cursor.fetchone()[0]

        if decision == "Approved":

            cursor.execute(
                """
                UPDATE negotiation_cases
                SET
                    case_status = 'Resolved',
                    final_decision = 'Approved'
                WHERE case_id = %s
                """,
                (case_id,)
            )

            cursor.execute(
                """
                UPDATE booking_requests
                SET
                    request_status = 'Approved',
                    negotiation_status = 'Accepted'
                WHERE request_id = %s
                """,
                (request_id,)
            )

        elif decision == "Rejected":
    
            cursor.execute(
                """
                UPDATE negotiation_cases
                SET
                    case_status = 'Resolved',
                    final_decision = 'Rejected'
                WHERE case_id = %s
                """,
                (case_id,)
            )

            cursor.execute(
                """
                UPDATE booking_requests
                SET
                    request_status = 'Rejected',
                    negotiation_status = 'Rejected'
                WHERE request_id = %s
                """,
                (request_id,)
            )

        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({
            "message":
            "Super Admin decision processed"
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500
    


def workflow_summary():
    
    try:

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM negotiation_cases
            WHERE case_status = 'Pending'
            """
        )
        pending_cases = cursor.fetchone()[0]

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM negotiation_cases
            WHERE case_status = 'Resolved'
            """
        )
        resolved_cases = cursor.fetchone()[0]

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM negotiation_cases
            WHERE final_decision = 'Approved'
            """
        )
        approved_cases = cursor.fetchone()[0]

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM negotiation_cases
            WHERE final_decision = 'Rejected'
            """
        )
        rejected_cases = cursor.fetchone()[0]

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM notifications
            """
        )
        notifications = cursor.fetchone()[0]

        cursor.close()
        conn.close()

        return jsonify({
            "pending_cases": pending_cases,
            "resolved_cases": resolved_cases,
            "approved_cases": approved_cases,
            "rejected_cases": rejected_cases,
            "notifications": notifications
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500
    



def get_case(case_id):

    try:

        conn = get_connection()

        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT *
            FROM negotiation_cases
            WHERE case_id = %s
            """,
            (case_id,)
        )

        case_data = cursor.fetchone()

        cursor.close()
        conn.close()

        if not case_data:

            return jsonify({
                "error": "Case not found"
            }), 404

        return jsonify(case_data)

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500
    

def get_notifications():
    
    try:

        conn = get_connection()

        cursor = conn.cursor(
            dictionary=True
        )

        cursor.execute(
            """
            SELECT *
            FROM notifications
            ORDER BY notification_id DESC
            """
        )

        notifications = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify(
            notifications
        )

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500
    


def get_available_slots(room_id, booking_date):
    
    print("ROOM ID =", room_id)
    print("BOOKING DATE =", booking_date)

    try:

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        all_slots = [
            "09:00-10:00",
            "11:00-12:00",
            "14:00-16:00"
        ]

        cursor.execute(
            """
            SELECT start_time, end_time
            FROM bookings
            WHERE resource_id = %s
            AND booking_date = %s
            AND booking_status != 'Cancelled'
            """,
            (room_id, booking_date)
        )

        booked = cursor.fetchall()

        print("BOOKED =", booked)   # <-- ADD HERE

        booked_slots = []

        for row in booked:
    
            start_seconds = row['start_time'].seconds
            end_seconds = row['end_time'].seconds

            start_hour = start_seconds // 3600
            start_min = (start_seconds % 3600) // 60

            end_hour = end_seconds // 3600
            end_min = (end_seconds % 3600) // 60

            slot = (
                f"{start_hour:02d}:{start_min:02d}-"
                f"{end_hour:02d}:{end_min:02d}"
            )

            booked_slots.append(slot)

            print("BOOKED SLOTS =", booked_slots)   # <-- ADD HERE

        available = []

        for slot in all_slots:

            if slot not in booked_slots:
                available.append(slot)

        print("AVAILABLE =", available)   # <-- ADD HERE

        cursor.close()
        conn.close()

        return jsonify(available)

    except Exception as e:

        print("ERROR =", e)

        return jsonify({
            "error": str(e)
        })


def check_custom_availability(
    room_id,
    booking_date,
    start_time,
    end_time
):

    try:

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT COUNT(*)

            FROM booking_requests

            WHERE resource_id = %s
            AND booking_date = %s

            AND (
                start_time < %s
                AND end_time > %s
            )
            """,
            (
                room_id,
                booking_date,
                end_time,
                start_time
            )
        )

        count = cursor.fetchone()[0]

        cursor.close()
        conn.close()

        if count == 0:

            return jsonify({
                "available": True,
                "message": "Room Available"
            })

        return jsonify({
            "available": False,
            "message": "Room Not Available"
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        })
    

def create_booking():
    
    try:

        data = request.get_json()

        conn = get_connection()
        cursor = conn.cursor()

        query = """
        INSERT INTO bookings(
            resource_id,
            requester_id,
            requester_type,
            event_name,
            purpose,
            participant_count,
            booking_date,
            start_time,
            end_time,
            booking_status,
            event_category
        )
        VALUES(
            %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s
        )
        """

        values = (
            data["resource_id"],
            data["requester_id"],
            data["requester_type"],
            data["event_name"],
            data["purpose"],
            data["participant_count"],
            data["booking_date"],
            data["start_time"],
            data["end_time"],
            "Confirmed",
            data["event_category"]
        )

        cursor.execute(query, values)

        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({
            "message": "Room Booked Successfully"
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        })
    

