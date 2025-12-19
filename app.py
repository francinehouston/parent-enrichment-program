from flask import Flask, render_template, request, redirect, url_for, flash, session
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'

# Sample data structure - in a real app, this would be a database
programs = []
participants = []

# Admin credentials - In production, store these securely in environment variables or database
# Default: username='admin', password='admin123' (CHANGE THIS!)
ADMIN_CREDENTIALS = {
    'username': 'admin',
    'password_hash': generate_password_hash('admin123')  # Change this password!
}

# Content storage - In production, use a database
documents = []
courses = []
quizzes = []
videos = []
tests = []
certifications = []

# Authentication decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_logged_in' not in session or not session['admin_logged_in']:
            flash('Please log in to access the admin area.', 'error')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html', programs=programs, participant_count=len(participants))

@app.route('/programs')
def list_programs():
    """List all programs"""
    return render_template('programs.html', programs=programs)

@app.route('/programs/new', methods=['GET', 'POST'])
def new_program():
    """Create a new program"""
    if request.method == 'POST':
        program = {
            'id': len(programs) + 1,
            'title': request.form['title'],
            'description': request.form['description'],
            'date': request.form['date'],
            'time': request.form['time'],
            'location': request.form['location'],
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        programs.append(program)
        flash('Program created successfully!', 'success')
        return redirect(url_for('list_programs'))
    return render_template('new_program.html')

@app.route('/participants')
def list_participants():
    """List all participants"""
    return render_template('participants.html', participants=participants)

@app.route('/participants/new', methods=['GET', 'POST'])
def new_participant():
    """Register a new participant"""
    if request.method == 'POST':
        participant = {
            'id': len(participants) + 1,
            'name': request.form['name'],
            'email': request.form['email'],
            'phone': request.form['phone'],
            'children_ages': request.form['children_ages'],
            'registered_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        participants.append(participant)
        flash('Participant registered successfully!', 'success')
        return redirect(url_for('list_participants'))
    return render_template('new_participant.html')

@app.route('/about')
def about():
    """About page"""
    return render_template('about.html')

@app.route('/membership')
def membership():
    """Membership page"""
    return render_template('membership.html')

@app.route('/donate', methods=['GET', 'POST'])
def donate():
    """Donate page"""
    # Handle PayPal return URLs
    if request.args.get('success') == '1':
        flash('Thank you for your donation! Your support makes a difference. You should receive a confirmation email from PayPal shortly.', 'success')
    elif request.args.get('cancel') == '1':
        flash('Your donation was cancelled. If you experienced any issues, please try again or contact us for assistance.', 'error')
    
    if request.method == 'POST':
        # This handles any form submissions (though PayPal forms post to PayPal directly)
        flash('Thank you for your donation! Your support makes a difference.', 'success')
        return redirect(url_for('donate'))
    return render_template('donate.html')

# ==================== ADMIN AUTHENTICATION ====================

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Admin login page"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == ADMIN_CREDENTIALS['username'] and check_password_hash(ADMIN_CREDENTIALS['password_hash'], password):
            session['admin_logged_in'] = True
            session['admin_username'] = username
            flash('Successfully logged in!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid username or password.', 'error')
    
    return render_template('admin/login.html')

@app.route('/admin/logout')
def admin_logout():
    """Admin logout"""
    session.pop('admin_logged_in', None)
    session.pop('admin_username', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('admin_login'))

@app.route('/admin')
@login_required
def admin_dashboard():
    """Admin dashboard"""
    stats = {
        'documents': len(documents),
        'courses': len(courses),
        'quizzes': len(quizzes),
        'videos': len(videos),
        'tests': len(tests),
        'certifications': len(certifications)
    }
    return render_template('admin/dashboard.html', stats=stats)

# ==================== DOCUMENTS ====================

@app.route('/admin/documents')
@login_required
def list_documents():
    """List all documents"""
    return render_template('admin/documents/list.html', documents=documents)

@app.route('/admin/documents/new', methods=['GET', 'POST'])
@login_required
def new_document():
    """Create a new document"""
    if request.method == 'POST':
        document = {
            'id': len(documents) + 1,
            'title': request.form['title'],
            'content': request.form['content'],
            'category': request.form.get('category', 'General'),
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'created_by': session.get('admin_username', 'Admin')
        }
        documents.append(document)
        flash('Document created successfully!', 'success')
        return redirect(url_for('list_documents'))
    return render_template('admin/documents/new.html')

@app.route('/admin/documents/<int:doc_id>')
@login_required
def view_document(doc_id):
    """View a document"""
    document = next((d for d in documents if d['id'] == doc_id), None)
    if not document:
        flash('Document not found.', 'error')
        return redirect(url_for('list_documents'))
    return render_template('admin/documents/view.html', document=document)

# ==================== COURSES ====================

@app.route('/admin/courses')
@login_required
def list_courses():
    """List all courses"""
    return render_template('admin/courses/list.html', courses=courses)

@app.route('/admin/courses/new', methods=['GET', 'POST'])
@login_required
def new_course():
    """Create a new course"""
    if request.method == 'POST':
        course = {
            'id': len(courses) + 1,
            'title': request.form['title'],
            'description': request.form['description'],
            'content': request.form['content'],
            'duration': request.form.get('duration', ''),
            'level': request.form.get('level', 'Beginner'),
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'created_by': session.get('admin_username', 'Admin')
        }
        courses.append(course)
        flash('Course created successfully!', 'success')
        return redirect(url_for('list_courses'))
    return render_template('admin/courses/new.html')

@app.route('/admin/courses/<int:course_id>')
@login_required
def view_course(course_id):
    """View a course"""
    course = next((c for c in courses if c['id'] == course_id), None)
    if not course:
        flash('Course not found.', 'error')
        return redirect(url_for('list_courses'))
    return render_template('admin/courses/view.html', course=course)

# ==================== QUIZZES ====================

@app.route('/admin/quizzes')
@login_required
def list_quizzes():
    """List all quizzes"""
    return render_template('admin/quizzes/list.html', quizzes=quizzes)

@app.route('/admin/quizzes/new', methods=['GET', 'POST'])
@login_required
def new_quiz():
    """Create a new quiz"""
    if request.method == 'POST':
        # Parse questions from form
        questions = []
        question_count = int(request.form.get('question_count', 0))
        for i in range(1, question_count + 1):
            if request.form.get(f'question_{i}'):
                questions.append({
                    'question': request.form.get(f'question_{i}'),
                    'options': [
                        request.form.get(f'option_{i}_1', ''),
                        request.form.get(f'option_{i}_2', ''),
                        request.form.get(f'option_{i}_3', ''),
                        request.form.get(f'option_{i}_4', '')
                    ],
                    'correct_answer': int(request.form.get(f'correct_{i}', 1))
                })
        
        quiz = {
            'id': len(quizzes) + 1,
            'title': request.form['title'],
            'description': request.form['description'],
            'questions': questions,
            'time_limit': request.form.get('time_limit', ''),
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'created_by': session.get('admin_username', 'Admin')
        }
        quizzes.append(quiz)
        flash('Quiz created successfully!', 'success')
        return redirect(url_for('list_quizzes'))
    return render_template('admin/quizzes/new.html')

@app.route('/admin/quizzes/<int:quiz_id>')
@login_required
def view_quiz(quiz_id):
    """View a quiz"""
    quiz = next((q for q in quizzes if q['id'] == quiz_id), None)
    if not quiz:
        flash('Quiz not found.', 'error')
        return redirect(url_for('list_quizzes'))
    return render_template('admin/quizzes/view.html', quiz=quiz)

# ==================== VIDEOS ====================

@app.route('/admin/videos')
@login_required
def list_videos():
    """List all videos"""
    return render_template('admin/videos/list.html', videos=videos)

@app.route('/admin/videos/new', methods=['GET', 'POST'])
@login_required
def new_video():
    """Create a new video"""
    if request.method == 'POST':
        video = {
            'id': len(videos) + 1,
            'title': request.form['title'],
            'description': request.form['description'],
            'video_url': request.form['video_url'],
            'thumbnail_url': request.form.get('thumbnail_url', ''),
            'duration': request.form.get('duration', ''),
            'category': request.form.get('category', 'General'),
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'created_by': session.get('admin_username', 'Admin')
        }
        videos.append(video)
        flash('Video added successfully!', 'success')
        return redirect(url_for('list_videos'))
    return render_template('admin/videos/new.html')

@app.route('/admin/videos/<int:video_id>')
@login_required
def view_video(video_id):
    """View a video"""
    video = next((v for v in videos if v['id'] == video_id), None)
    if not video:
        flash('Video not found.', 'error')
        return redirect(url_for('list_videos'))
    return render_template('admin/videos/view.html', video=video)

# ==================== TESTS ====================

@app.route('/admin/tests')
@login_required
def list_tests():
    """List all tests"""
    return render_template('admin/tests/list.html', tests=tests)

@app.route('/admin/tests/new', methods=['GET', 'POST'])
@login_required
def new_test():
    """Create a new test"""
    if request.method == 'POST':
        # Parse questions from form
        questions = []
        question_count = int(request.form.get('question_count', 0))
        for i in range(1, question_count + 1):
            if request.form.get(f'question_{i}'):
                questions.append({
                    'question': request.form.get(f'question_{i}'),
                    'options': [
                        request.form.get(f'option_{i}_1', ''),
                        request.form.get(f'option_{i}_2', ''),
                        request.form.get(f'option_{i}_3', ''),
                        request.form.get(f'option_{i}_4', '')
                    ],
                    'correct_answer': int(request.form.get(f'correct_{i}', 1)),
                    'points': int(request.form.get(f'points_{i}', 1))
                })
        
        test = {
            'id': len(tests) + 1,
            'title': request.form['title'],
            'description': request.form['description'],
            'questions': questions,
            'time_limit': request.form.get('time_limit', ''),
            'passing_score': int(request.form.get('passing_score', 70)),
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'created_by': session.get('admin_username', 'Admin')
        }
        tests.append(test)
        flash('Test created successfully!', 'success')
        return redirect(url_for('list_tests'))
    return render_template('admin/tests/new.html')

@app.route('/admin/tests/<int:test_id>')
@login_required
def view_test(test_id):
    """View a test"""
    test = next((t for t in tests if t['id'] == test_id), None)
    if not test:
        flash('Test not found.', 'error')
        return redirect(url_for('list_tests'))
    # Calculate total points
    total_points = sum(q.get('points', 1) for q in test.get('questions', []))
    return render_template('admin/tests/view.html', test=test, total_points=total_points)

# ==================== CERTIFICATIONS ====================

@app.route('/admin/certifications')
@login_required
def list_certifications():
    """List all certifications"""
    return render_template('admin/certifications/list.html', certifications=certifications)

@app.route('/admin/certifications/new', methods=['GET', 'POST'])
@login_required
def new_certification():
    """Create a new certification"""
    if request.method == 'POST':
        certification = {
            'id': len(certifications) + 1,
            'title': request.form['title'],
            'description': request.form['description'],
            'requirements': request.form['requirements'],
            'validity_period': request.form.get('validity_period', ''),
            'associated_course': request.form.get('associated_course', ''),
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'created_by': session.get('admin_username', 'Admin')
        }
        certifications.append(certification)
        flash('Certification created successfully!', 'success')
        return redirect(url_for('list_certifications'))
    return render_template('admin/certifications/new.html', courses=courses)

@app.route('/admin/certifications/<int:cert_id>')
@login_required
def view_certification(cert_id):
    """View a certification"""
    certification = next((c for c in certifications if c['id'] == cert_id), None)
    if not certification:
        flash('Certification not found.', 'error')
        return redirect(url_for('list_certifications'))
    return render_template('admin/certifications/view.html', certification=certification)

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8000)

