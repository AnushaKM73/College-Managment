from database import get_connection
#from services.notification_service import create_notification

def create_notification(
    case_id,
    receiver_id,
    notification_type,
    message
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO notifications(

            case_id,
            receiver_id,
            notification_type,
            message

        )

        VALUES(

            %s,
            %s,
            %s,
            %s

        )
        """,
        (
            case_id,
            receiver_id,
            notification_type,
            message
        )
    )

    conn.commit()

    cursor.close()
    conn.close()





def create_negotiation_case_and_notify(
    booking_id,
    request_id
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.callproc(
        'create_negotiation_case',
        [
            booking_id,
            request_id
        ]
    )

    conn.commit()

    cursor.execute(
        """
        SELECT
            requester_id
        FROM bookings
        WHERE booking_id = %s
        """,
        (booking_id,)
    )

    owner = cursor.fetchone()

    cursor.execute(
        """
        SELECT
            MAX(case_id)
        FROM negotiation_cases
        """
    )

    case_id = cursor.fetchone()[0]

    create_notification(
        case_id,
        owner[0],
        'System',
        'Higher priority request requires negotiation'
    )

    cursor.close()
    conn.close()