from borajunto.models.member import TripMember

def get_membership(trip_id, user_id):
    return TripMember.query.filter_by(trip_id=trip_id, user_id=user_id).first()

def is_trip_member(trip_id, user_id):
    return get_membership(trip_id, user_id) is not None

def can_manage_trip(trip_id, user_id):
    membership = get_membership(trip_id, user_id)
    if membership and membership.role in ["owner", "admin"]:
        return True
    return False
