from flask import Blueprint, render_template, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from borajunto.ext.db import db
from borajunto.models.trip import Trip
from borajunto.models.member import TripMember
from borajunto.models.invite import TripInvite
from borajunto.forms.trip import TripForm
from borajunto.services.permissions import is_trip_member, can_manage_trip
from borajunto.services.invites import create_trip_invite, get_valid_invite_by_token

bp_trips = Blueprint("trips", __name__, url_prefix="/trips")

@bp_trips.route("/")
@login_required
def list_trips():
    memberships = TripMember.query.filter_by(user_id=current_user.id).all()
    trips = [m.trip for m in memberships]
    return render_template("trips/list.html", trips=trips)

@bp_trips.route("/new", methods=["GET", "POST"])
@login_required
def create_trip():
    form = TripForm()
    if form.validate_on_submit():
        trip = Trip(
            title=form.title.data,
            destination=form.destination.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            description=form.description.data,
            owner_id=current_user.id
        )
        db.session.add(trip)
        db.session.flush() # para obter trip.id

        member = TripMember(
            trip_id=trip.id,
            user_id=current_user.id,
            role="owner"
        )
        db.session.add(member)
        db.session.commit()
        
        flash("Viagem criada com sucesso!", "success")
        return redirect(url_for("trips.detail_trip", trip_id=trip.id))
        
    return render_template("trips/form.html", form=form)

@bp_trips.route("/<int:trip_id>")
@login_required
def detail_trip(trip_id):
    trip = db.get_or_404(Trip, trip_id)
    
    if not is_trip_member(trip_id, current_user.id):
        abort(403)
        
    can_manage = can_manage_trip(trip_id, current_user.id)
    
    from borajunto.models.task import Task
    from borajunto.forms.task import StatusForm
    from borajunto.models.photo import Photo
    
    pending_tasks = Task.query.filter_by(trip_id=trip_id, status="pending").order_by(Task.created_at.desc()).all()
    doing_tasks = Task.query.filter_by(trip_id=trip_id, status="doing").order_by(Task.created_at.desc()).all()
    done_tasks = Task.query.filter_by(trip_id=trip_id, status="done").order_by(Task.completed_at.desc()).all()
    status_form = StatusForm()
    
    latest_photos = Photo.query.filter_by(trip_id=trip_id).order_by(
        db.desc(Photo.taken_at), db.desc(Photo.created_at)
    ).limit(4).all()
        
    return render_template("trips/detail.html", trip=trip, can_manage=can_manage, 
                           pending_tasks=pending_tasks, doing_tasks=doing_tasks, 
                           done_tasks=done_tasks, status_form=status_form,
                           latest_photos=latest_photos)

@bp_trips.route("/<int:trip_id>/invite")
@login_required
def invite_trip(trip_id):
    trip = db.get_or_404(Trip, trip_id)
    
    if not can_manage_trip(trip_id, current_user.id):
        abort(403)
        
    invites = TripInvite.query.filter_by(trip_id=trip_id, is_active=True).all()
    return render_template("trips/invite.html", trip=trip, invites=invites)

@bp_trips.route("/<int:trip_id>/invite/generate", methods=["POST"])
@login_required
def generate_invite(trip_id):
    trip = db.get_or_404(Trip, trip_id)
    
    if not can_manage_trip(trip_id, current_user.id):
        abort(403)
        
    create_trip_invite(trip, current_user)
    flash("Convite gerado com sucesso!", "success")
    return redirect(url_for("trips.invite_trip", trip_id=trip.id))

@bp_trips.route("/join/<token>")
@login_required
def join_trip(token):
    invite = get_valid_invite_by_token(token)
    if not invite:
        flash("Convite inválido ou expirado.", "danger")
        return redirect(url_for("trips.list_trips"))
        
    if is_trip_member(invite.trip_id, current_user.id):
        flash("Você já é membro desta viagem.", "info")
        return redirect(url_for("trips.detail_trip", trip_id=invite.trip_id))
        
    member = TripMember(
        trip_id=invite.trip_id,
        user_id=current_user.id,
        role="member"
    )
    invite.uses += 1
    
    db.session.add(member)
    db.session.commit()
    
    flash("Você entrou na viagem com sucesso!", "success")
    return redirect(url_for("trips.detail_trip", trip_id=invite.trip_id))
