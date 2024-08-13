from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import StudentInfo, User, AnnouncementTeacher, AnnouncementAdmin, Schedule, Level, Enrol, Section, Subject
from . import db

views = Blueprint('views', __name__)

@views.route('/student-dashboard', methods=['GET', 'POST'])
@login_required
def student_dashboard():
   student_info = StudentInfo.query.filter_by(user_id=current_user.id).first()
   announcements = AnnouncementTeacher.query.all()
   announcements1 = AnnouncementAdmin.query.all()
   levels = Level.query.all()
   schedules = Schedule.query.all()
   subjects_dict = {subject.id: subject.name for subject in Subject.query.all()}
   subjects = []


   if request.method == 'POST':
       level_id = request.form.get('level')
       schedule_id = request.form.get('schedule')
       action = request.form.get('action')
       section_id = request.form.get('section_id')


       if level_id and schedule_id:
           subjects = Section.query.filter_by(level_id=level_id, schedule_id=schedule_id).all()


       if action == 'reserve' and section_id:
           existing_enrollment = Enrol.query.filter_by(user_id=current_user.id, section_id=section_id).first()
           if not existing_enrollment:
               new_enrollment = Enrol(user_id=current_user.id, section_id=section_id)
               db.session.add(new_enrollment)
               db.session.commit()
               flash('Successfully reserved the subject!', 'success')


       if action == 'unreserve' and section_id:
           existing_enrollment = Enrol.query.filter_by(user_id=current_user.id, section_id=section_id).first()
           if existing_enrollment:
               db.session.delete(existing_enrollment)
               db.session.commit()
               flash('Successfully unreserved the subject!', 'info')


   reserved_subjects = Section.query.join(Enrol).filter(Enrol.user_id == current_user.id).all()


   return render_template('student_dashboard.html', 
                          student=student_info,
                          student_id=current_user.id,  
                          announcements=announcements, 
                          announcements1=announcements1, 
                          levels=levels, 
                          schedules=schedules, 
                          subjects=subjects,  
                          subjects_dict=subjects_dict,
                          reserved_subjects=reserved_subjects, 
                          title='Student Dashboard')


@views.route('/teacher-dashboard', methods=['GET', 'POST'])
@login_required
def teacher_dashboard():
   announcements = AnnouncementTeacher.query.all()
   curriculums = Section.query.all()


   if request.method == 'POST':
       title = request.form.get('title')
       description = request.form.get('description')


       if title and description:
           new_announcement = AnnouncementTeacher(title=title, description=description, created_by=current_user.id)
           db.session.add(new_announcement)
           db.session.commit()
           flash('Announcement added successfully!', category='success')


       elif 'announcement_id' in request.form:
           announcement_id = request.form.get('announcement_id')
           announcement = AnnouncementTeacher.query.get(announcement_id)


           if announcement:
               if AnnouncementTeacher.created_by == current_user.id:
                   db.session.delete(announcement)
                   db.session.commit()
                   flash('Announcement deleted successfully!', category='success')
               else:
                   flash('Announcement not found!', category='error') # Admin Announce could be seen


   return render_template('teacher_dashboard.html', user=current_user, announcements=announcements, curriculums=curriculums, title='Teacher Dashboard')




@views.route('/admin-dashboard', methods=['GET', 'POST'])
@login_required
def admin_dashboard():
    sections = Section.query.all()
    student_info = StudentInfo.query.filter_by(user_id=current_user.id).first()
    announcements = AnnouncementTeacher.query.all()
    announcements_admin = AnnouncementAdmin.query.all()
    levels = Level.query.all()
    schedules = Schedule.query.all()
    subjects = Subject.query.all()
    enrollments = Enrol.query.all()
    users = User.query.all()

    student_counts = []

    # Categorize users by role
    students = [user for user in users if user.role == 'student']
    teachers = [user for user in users if user.role == 'teacher']
    admins = [user for user in users if user.role == 'admin']

    if request.method == 'POST':
        if 'email' in request.form:
            # Handle student info form submission (unchanged)
            email = request.form.get('email')
            last_name = request.form.get('last_name')
            middle_name = request.form.get('middle_name')
            first_name = request.form.get('first_name')
            suffix = request.form.get('suffix')
            date_of_birth = request.form.get('date_of_birth')
            gender = request.form.get('gender')
            nationality = request.form.get('nationality')
            address = request.form.get('address')
            parent_guardian_name = request.form.get('parent_guardian_name')
            relationship_to_student = request.form.get('relationship_to_student')
            contact_number = request.form.get('contact_number')
            email_gp = request.form.get('email_gp')
            emergency_contact_name = request.form.get('emergency_contact_name')
            emergency_relationship = request.form.get('emergency_relationship')
            emergency_contact_number = request.form.get('emergency_contact_number')

            user = User.query.filter_by(email=email).first()
            if user:
                student_info = StudentInfo.query.filter_by(email=email).first()
                if student_info:
                    student_info.last_name = last_name
                    student_info.middle_name = middle_name
                    student_info.first_name = first_name
                    student_info.suffix = suffix
                    student_info.date_of_birth = date_of_birth
                    student_info.gender = gender
                    student_info.nationality = nationality
                    student_info.address = address
                    student_info.parent_guardian_name = parent_guardian_name
                    student_info.relationship_to_student = relationship_to_student
                    student_info.contact_number = contact_number
                    student_info.emergency_contact_name = emergency_contact_name
                    student_info.emergency_relationship = emergency_relationship
                    student_info.email_gp = email_gp
                    student_info.emergency_contact_number = emergency_contact_number
                else:
                    student_info = StudentInfo(
                        email=email,
                        last_name=last_name,
                        middle_name=middle_name,
                        first_name=first_name,
                        suffix=suffix,
                        date_of_birth=date_of_birth,
                        gender=gender,
                        nationality=nationality,
                        address=address,
                        parent_guardian_name=parent_guardian_name,
                        relationship_to_student=relationship_to_student,
                        contact_number=contact_number,
                        email_gp=email_gp,
                        emergency_contact_name=emergency_contact_name,
                        emergency_relationship=emergency_relationship,
                        emergency_contact_number=emergency_contact_number,
                        user_id=user.id
                    )
                    db.session.add(student_info)
                    db.session.commit()
                flash('Student information has been saved successfully!', category='success')
            else:
                flash('No user found with this email address.', category='error')
            return redirect(url_for('views.admin_dashboard'))  # Redirect after successful addition


        elif 'title' in request.form:
            # Handling announcements
            title = request.form.get('title')
            description = request.form.get('description')
            if title and description:
                new_announcement = AnnouncementAdmin(title=title, description=description, created_by=current_user.id)
                db.session.add(new_announcement)
                db.session.commit()
                flash('Announcement added successfully!', category='success')
            return redirect(url_for('views.admin_dashboard'))  # Redirect after successful addition
            

        elif 'edit_section_id' in request.form:
            section_id = request.form.get('edit_section_id')
            new_level_id = request.form.get('edit_level_id')
            new_schedule_id = request.form.get('edit_schedule_id')
            new_subject_id = request.form.get('edit_subject_id')
            new_time_from = request.form.get('edit_time_from')
            new_time_to = request.form.get('edit_time_to')
            new_instructor = request.form.get('edit_instructor')

            section = Section.query.get(section_id)

            if section:
                section.level_id = new_level_id or section.level_id
                section.schedule_id = new_schedule_id or section.schedule_id
                section.subject_id = new_subject_id or section.subject_id
                section.time_from = new_time_from or section.time_from
                section.time_to = new_time_to or section.time_to
                section.instructor = new_instructor or section.instructor
                db.session.commit()
                flash('Section updated successfully!', category='success')
            else:
                flash('Section not found!', category='error')

            return redirect(url_for('views.admin_dashboard'))

        elif 'announcement_id' in request.form:
            # Deleting announcements
            announcement_id = request.form.get('announcement_id')
            if announcement_id:
                announcement = AnnouncementAdmin.query.get(announcement_id)
                if announcement:
                    db.session.delete(announcement)
                    db.session.commit()
                    flash('Announcement deleted successfully!', category='success')
                else:
                    flash('Announcement not found!', category='error')
            return redirect(url_for('views.admin_dashboard'))  # Redirect after successful addition

        elif 'announcement_id1' in request.form:
            announcement_id1 = request.form.get('announcement_id1')
            if announcement_id1:
                announcement1 = AnnouncementTeacher.query.get(announcement_id1)
                if announcement1:
                    db.session.delete(announcement1)
                    db.session.commit()
                    flash('Announcement deleted successfully!', category='success')
                else:
                    flash('Announcement not found!', category='error')
            return redirect(url_for('views.admin_dashboard'))  # Redirect after successful addition

        elif 'level_name' in request.form:
            # Adding new level, schedule, and subject
            level_name = request.form.get('level_name')
            if level_name:
                existing_level = Level.query.filter_by(name=level_name).first()
                if existing_level:
                    flash('Level with this name already exists!', category='error')
                else:
                    new_level = Level(name=level_name)
                    db.session.add(new_level)
                    db.session.commit()
                    flash('Level added successfully!', category='success')
            return redirect(url_for('views.admin_dashboard'))  # Redirect after successful addition

        elif 'schedule_name' in request.form:
            schedule_name = request.form.get('schedule_name')
            if schedule_name:
                existing_schedule = Schedule.query.filter_by(name=schedule_name).first()
                if existing_schedule:
                    flash('Schedule with this name already exists!', category='error')
                else:
                    new_schedule = Schedule(name=schedule_name)
                    db.session.add(new_schedule)
                    db.session.commit()
                    flash('Schedule added successfully!', category='success')
            return redirect(url_for('views.admin_dashboard'))  # Redirect after successful addition

        elif 'subject_name' in request.form:
            subject_name = request.form.get('subject_name')
            if subject_name:
                existing_subject = Subject.query.filter_by(name=subject_name).first()
                if existing_subject:
                    flash('Subject with this name already exists!', category='error')
                else:
                    new_subject = Subject(name=subject_name)
                    db.session.add(new_subject)
                    db.session.commit()
                    flash('Subject added successfully!', category='success')
            return redirect(url_for('views.admin_dashboard'))  # Redirect after successful addition

        elif 'edit_level_id' in request.form:
            # Editing level, schedule, and subject
            edit_level_id = request.form.get('edit_level_id')
            new_level_name = request.form.get('edit_level_name')
            if edit_level_id and new_level_name:
                level = Level.query.get(edit_level_id)
                if level:
                    level.name = new_level_name
                    db.session.commit()
                    flash('Level updated successfully!', category='success')
                else:
                    flash('Level not found!', category='error')

        elif 'edit_schedule_id' in request.form:
            edit_schedule_id = request.form.get('edit_schedule_id')
            new_schedule_name = request.form.get('edit_schedule_name')
            if edit_schedule_id and new_schedule_name:
                schedule = Schedule.query.get(edit_schedule_id)
                if schedule:
                    schedule.name = new_schedule_name
                    db.session.commit()
                    flash('Schedule updated successfully!', category='success')
                else:
                    flash('Schedule not found!', category='error')

        elif 'edit_subject_id' in request.form:
            edit_subject_id = request.form.get('edit_subject_id')
            new_subject_name = request.form.get('edit_subject_name')
            if edit_subject_id and new_subject_name:
                subject = Subject.query.get(edit_subject_id)
                if subject:
                    subject.name = new_subject_name
                    db.session.commit()
                    flash('Subject updated successfully!', category='success')
                else:
                    flash('Subject not found!', category='error')
            return redirect(url_for('views.admin_dashboard'))  # Redirect after successful addition

        elif 'delete_level_id' in request.form:
            # Deleting level, schedule, and subject
            delete_level_id = request.form.get('delete_level_id')
            if delete_level_id:
                level = Level.query.get(delete_level_id)
                if level:
                    db.session.delete(level)
                    db.session.commit()
                    flash('Level deleted successfully!', category='success')
                else:
                    flash('Level not found!', category='error')
            return redirect(url_for('views.admin_dashboard'))  # Redirect after successful addition

        elif 'delete_schedule_id' in request.form:
            delete_schedule_id = request.form.get('delete_schedule_id')
            if delete_schedule_id:
                schedule = Schedule.query.get(delete_schedule_id)
                if schedule:
                    db.session.delete(schedule)
                    db.session.commit()
                    flash('Schedule deleted successfully!', category='success')
                else:
                    flash('Schedule not found!', category='error')
            return redirect(url_for('views.admin_dashboard'))  # Redirect after successful addition

        elif 'delete_subject_id' in request.form:
            delete_subject_id = request.form.get('delete_subject_id')
            if delete_subject_id:
                subject = Subject.query.get(delete_subject_id)
                if subject:
                    db.session.delete(subject)
                    db.session.commit()
                    flash('Subject deleted successfully!', category='success')
                else:
                    flash('Subject not found!', category='error')
            return redirect(url_for('views.admin_dashboard'))  # Redirect after successful addition

        elif 'level_id' in request.form and 'schedule_id' in request.form:
            # Add, edit, and delete sections
            level_id = request.form.get('level_id', type=int)
            schedule_id = request.form.get('schedule_id', type=int)
            subject_id = request.form.get('subject_id', type=int)
            time_from = request.form.get('time_from')
            time_to = request.form.get('time_to')
            instructor = request.form.get('instructor')

            if level_id and schedule_id and subject_id:
                new_section = Section(
                    level_id=level_id,
                    schedule_id=schedule_id,
                    subject_id=subject_id,
                    time_from=time_from,
                    time_to=time_to,
                    instructor=instructor
                )
                db.session.add(new_section)
                db.session.commit()
                flash('Section added successfully!', category='success')
            return redirect(url_for('views.admin_dashboard'))  # Redirect after successful addition

        elif 'edit_section_id' in request.form:
            edit_section_id = request.form.get('edit_section_id')
            new_level_id = request.form.get('edit_level_id')
            new_schedule_id = request.form.get('edit_schedule_id')
            new_subject_id = request.form.get('edit_subject_id')
            new_time_from = request.form.get('edit_time_from')
            new_time_to = request.form.get('edit_time_to')
            new_instructor = request.form.get('edit_instructor')

            if edit_section_id:
                section = Section.query.get(edit_section_id)
                if section:
                    if new_level_id:
                        section.level_id = new_level_id
                    if new_schedule_id:
                        section.schedule_id = new_schedule_id
                    if new_subject_id:
                        section.subject_id = new_subject_id
                    if new_time_from:
                        section.time_from = new_time_from
                    if new_time_to:
                        section.time_to = new_time_to
                    if new_instructor:
                        section.instructor = new_instructor

                    db.session.commit()
                    flash('Section updated successfully!', category='success')
                else:
                    flash('Section not found!', category='error')
            return redirect(url_for('views.admin_dashboard'))  # Redirect after successful update

        elif 'delete_section_id' in request.form:
            delete_section_id = request.form.get('delete_section_id')
            if delete_section_id:
                section = Section.query.get(delete_section_id)
                if section:
                    db.session.delete(section)
                    db.session.commit()
                    flash('Section deleted successfully!', category='success')
                else:
                    flash('Section not found!', category='error')
            return redirect(url_for('views.admin_dashboard'))  # Redirect after successful addition

        elif 'delete_enrollment' in request.form:
           user_id = request.form.get('user_id')
           enrollments = Enrol.query.filter_by(user_id=user_id).all()
           if enrollments:
               for enrollment in enrollments:
                   db.session.delete(enrollment)
               db.session.commit()
               flash('Enrollments deleted successfully!', 'success')
           else:
               flash('No enrollments found for this user.', 'error')
           return redirect(url_for('views.admin_dashboard'))
        
        elif 'enrollment_id' in request.form:
                # Enrollment status update
                enrollment_id = request.form.get('enrollment_id')
                new_status = request.form.get('status')
                if enrollment_id:
                    enrollment = Enrol.query.get(enrollment_id)
                    if enrollment:
                        enrollment.status = new_status
                        db.session.commit()
                        flash('Enrollment status updated successfully!', category='success')
                    else:
                        flash('Enrollment not found!', category='error')
                return redirect(url_for('views.admin_dashboard'))  # Redirect after successful addition

        elif 'level' in request.form and 'schedule' in request.form:
                selected_level = request.form.get('level')
                selected_schedule = request.form.get('schedule')
                if selected_level and selected_schedule:
                    sections = Section.query.filter_by(level_id=selected_level, schedule_id=selected_schedule).all()
                    count = 0
                    enrolled_students = []

                    for section in sections:
                        enrollments_in_section = Enrol.query.filter_by(section_id=section.id).all()
                        count += len(enrollments_in_section)
                        for enrol in enrollments_in_section:
                            student = StudentInfo.query.filter_by(user_id=enrol.user_id).first()
                            if student:
                                enrolled_students.append(student)
                    student_counts.append((selected_level, selected_schedule, count, enrolled_students))

    return render_template(
       "admin_dashboard.html",
       users=users,
       student_info=student_info,
       announcements=announcements,
       announcements_admin=announcements_admin,
       levels=levels,
       schedules=schedules,
       subjects=subjects,
       sections=sections,
       students=students,
       teachers=teachers,
       admins=admins,
       enrollments=enrollments,
       student_counts = student_counts,
       user = current_user
   )
    

            


@views.route('/', methods=['GET', 'POST'])
@login_required
def index():


   if current_user.is_authenticated:
       # Redirect authenticated users to their respective dashboards
       if current_user.role == 'admin':
           return redirect(url_for('views.admin_dashboard'))
       elif current_user.role == 'teacher':
           return redirect(url_for('views.teacher_dashboard'))
       elif current_user.role == 'student':
           return redirect(url_for('views.student_dashboard'))
   # Render a base page or login page for unauthenticated users
   return render_template('base.html')