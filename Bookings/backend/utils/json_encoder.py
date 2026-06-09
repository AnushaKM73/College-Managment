import datetime


def serialize_data(data):

    if isinstance(data, list):

        return [
            serialize_data(item)
            for item in data
        ]

    elif isinstance(data, dict):

        return {
            key: serialize_data(value)
            for key, value in data.items()
        }

    elif isinstance(
        data,
        (
            datetime.date,
            datetime.datetime,
            datetime.time,
            datetime.timedelta
        )
    ):

        return str(data)

    else:

        return data