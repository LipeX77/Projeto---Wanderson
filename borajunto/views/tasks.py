from datetime import datetime, UTC
from flask import Blueprint, render_template, redirect, url_for, flash, abort, request
from flask_login import login_required, current_user
from borajunto.ext.db import db
from borajunto.models.trip import Trip
from borajunto.models.task import Task
from borajunto.forms.task import TaskForm, StatusForm
from borajunto.services.permissions import is_trip_member, can_manage_trip

bp_tasks = Blueprint("tasks", __name__, url_prefix="/trips/<int:trip_id>/tasks")

def load_trip_members_choices(trip):
    choices = [(0, "Sem responsável")]
    for member in trip.members:
        choices.append((member.user.id, member.user.name))
    return choices

@bp_tasks.route("/new", methods=["GET", "POST"])
@login_required
def create_task(trip_id):
    trip = db.get_or_404(Trip, trip_id)
    if not is_trip_member(trip_id, current_user.id):
        abort(403)
        
    form = TaskForm()
    form.assignee_id.choices = load_trip_members_choices(trip)
    
    if form.validate_on_submit():
        assignee = form.assignee_id.data if form.assignee_id.data > 0 else None
        
        task = Task(
            trip_id=trip.id,
            title=form.title.data,
            description=form.description.data,
            assignee_id=assignee,
            due_date=form.due_date.data,
            priority=form.priority.data,
            created_by_id=current_user.id,
            status="pending"
        )
        db.session.add(task)
        db.session.commit()
        
        flash("Tarefa criada com sucesso!", "success")
        return redirect(url_for("trips.detail_trip", trip_id=trip.id))
        
    return render_template("tasks/form.html", form=form, trip=trip, title="Nova Tarefa")

@bp_tasks.route("/<int:task_id>/edit", methods=["GET", "POST"])
@login_required
def edit_task(trip_id, task_id):
    task = db.get_or_404(Task, task_id)
    if task.trip_id != trip_id:
        abort(404)
        
    trip = db.get_or_404(Trip, trip_id)
    if not is_trip_member(trip_id, current_user.id):
        abort(403)
        
    form = TaskForm(obj=task)
    form.assignee_id.choices = load_trip_members_choices(trip)
    
    if form.validate_on_submit():
        task.title = form.title.data
        task.description = form.description.data
        task.assignee_id = form.assignee_id.data if form.assignee_id.data > 0 else None
        task.due_date = form.due_date.data
        task.priority = form.priority.data
        
        db.session.commit()
        flash("Tarefa atualizada com sucesso!", "success")
        return redirect(url_for("trips.detail_trip", trip_id=trip.id))
        
    if request.method == "GET":
        form.assignee_id.data = task.assignee_id if task.assignee_id else 0
        
    return render_template("tasks/form.html", form=form, trip=trip, title="Editar Tarefa", task=task)

@bp_tasks.route("/<int:task_id>/status", methods=["POST"])
@login_required
def update_task_status(trip_id, task_id):
    task = db.get_or_404(Task, task_id)
    if task.trip_id != trip_id:
        abort(404)
        
    if not is_trip_member(trip_id, current_user.id):
        abort(403)
        
    form = StatusForm()
    if form.validate_on_submit():
        new_status = form.status.data
        
        if new_status == "done" and task.status != "done":
            task.completed_at = datetime.now(UTC)
        elif new_status != "done" and task.status == "done":
            task.completed_at = None
            
        task.status = new_status
        db.session.commit()
        flash("Status atualizado com sucesso!", "success")
        
    return redirect(url_for("trips.detail_trip", trip_id=trip_id))

@bp_tasks.route("/<int:task_id>/delete", methods=["POST"])
@login_required
def delete_task(trip_id, task_id):
    task = db.get_or_404(Task, task_id)
    if task.trip_id != trip_id:
        abort(404)
        
    if not (can_manage_trip(trip_id, current_user.id) or task.created_by_id == current_user.id):
        abort(403)
        
    db.session.delete(task)
    db.session.commit()
    flash("Tarefa excluída com sucesso!", "success")
    return redirect(url_for("trips.detail_trip", trip_id=trip_id))

from borajunto.models.attachment import Attachment
from borajunto.forms.attachment import AttachmentForm
from borajunto.services.uploads import allowed_file, save_uploaded_file

@bp_tasks.route("/<int:task_id>/attachments/new", methods=["GET", "POST"])
@login_required
def upload_task_attachment(trip_id, task_id):
    trip = db.get_or_404(Trip, trip_id)
    task = db.get_or_404(Task, task_id)
    
    if task.trip_id != trip_id:
        abort(404)
        
    if not is_trip_member(trip_id, current_user.id):
        abort(403)
        
    form = AttachmentForm()
    
    if form.validate_on_submit():
        file = form.file.data
        if not allowed_file(file.filename):
            flash("Tipo de arquivo não permitido.", "danger")
            return render_template("tasks/upload.html", form=form, trip=trip, task=task)
            
        file_data = save_uploaded_file(file, subfolder="tasks")
        if file_data:
            attachment = Attachment(
                trip_id=trip.id,
                task_id=task.id,
                uploaded_by_id=current_user.id,
                original_name=file_data["original_name"],
                stored_name=file_data["stored_name"],
                storage_path=file_data["storage_path"],
                mime_type=file_data["mime_type"],
                file_size=file_data["file_size"],
                file_type="task_proof"
            )
            db.session.add(attachment)
            db.session.commit()
            flash("Comprovante enviado com sucesso!", "success")
            return redirect(url_for("trips.detail_trip", trip_id=trip.id))
            
    return render_template("tasks/upload.html", form=form, trip=trip, task=task)
