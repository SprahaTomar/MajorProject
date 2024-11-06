from flask import flash, render_template, redirect, url_for, request, jsonify
from app import app, db, login_manager, csrf
from flask_login import current_user, login_required, login_user, logout_user
from app.forms import RegistrationForm, LoginForm, ProjectForm
from app.models import Users, Projects, Investment
from flask_wtf.csrf import generate_csrf
from flask import send_from_directory
#from app.data_loader import load_data
from flask import current_app
from flask import send_from_directory, after_this_request

#import app.charting_algorithm as charting_algorithm

@app.route('/')
def index():
    return render_template('main.html')

def get_project_id_for_user(username):
    # Query the Users table to get the user
    user = Users.query.filter_by(username=username).first()

    if user:
        # Query the Projects table to get the project ID associated with the user
        user_project = Projects.query.filter_by(user_id=user.id).first()
        if user_project:
            return user_project.id
    return None

# Flask backend

@app.route('/register', methods=['GET', 'POST'])
def register():
    register_form = RegistrationForm()
    login_form = LoginForm()
    user_type = request.args.get('user_type')
    print(user_type)
    print("1")
    if register_form.validate_on_submit():
        user_type = request.form.get('user_type')
        print(user_type)
        print("2")
        user = Users(username=register_form.username.data, email=register_form.email.data, user_type=user_type)
        user.set_password(register_form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', register_form=register_form, login_form=login_form, user_type=user_type)


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

# Logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('index'))

@app.route('/admin')
def admin():
    register_form = RegistrationForm()
    login_form = LoginForm()
    project_form = ProjectForm()
    username = request.args.get('username')
    user = Users.query.filter_by(username=username).first()
    if user is None:
        print('User not found')
        return redirect(url_for('index'))
    return render_template('admin.html', title='Admin', user=user,register_form=register_form, login_form=login_form, project_form=project_form)


@app.route('/investor')
def investor():
    # Add your logic for the investor route here
    print("in the investor route")
    register_form = RegistrationForm()
    login_form = LoginForm()
    username = request.args.get('username')
    print("in the route below")
    if username:
        user = Users.query.filter_by(username=username).first()
        print("in the if statement")
        if user:
            print("in the if - if statement")
            return render_template('investor.html', title='Investor', user=user, register_form=register_form, login_form=login_form)
    print('User not found')
    return redirect(url_for('index'))

@app.route('/create_project', methods=['GET', 'POST'])
@login_required
def create_project():
  print("1")
  print(current_user)
  
  project_form = ProjectForm()
  if project_form.validate_on_submit():
    print("in the if statement")
    project = Projects(project_name=project_form.project_name.data,
                        description=project_form.description.data,
                        investment_goal=project_form.investment_goal.data,
                        location=project_form.location.data,
                        user_id=current_user.id)
    try:
      db.session.add(project)
      db.session.commit()
      flash('Your project has been created!', 'success')
      print("Project saved successfully")
      return redirect(url_for('index'))
    except Exception as e:  # Catch any database commit errors
      print(f"Error saving project: {e}")
      flash('Failed to create project. Please try again.', 'danger')
      return render_template('admin.html', title='Create Project', project_form=project_form)
  print("Form validation failed:", project_form.errors)
  return render_template('admin.html', title='Create Project', project_form=project_form)


@app.route('/login', methods=['GET', 'POST'])
#@csrf.exempt
def login():
    register_form = RegistrationForm()
    login_form = LoginForm()
    if request.method == 'POST':
        # Extract username and password from form data (assuming form submission)
        username = request.form.get('login_username')
        password = request.form.get('login_password')

        print(f"Username entered: {username}")  # Check username value
        print(f"Password entered: {password}")

        # Check if username and password are provided
        if not (username and password):
            print("1")
            return jsonify({'error': 'Missing required fields'}), 400

        # Query the database to find the user
        print("2")
        user = Users.query.filter_by(username=username).first()
        print(user)
        print("User retrieved from database:", user)

        # If user not found or password is incorrect, return error
        if user is None or not user.check_password(password):
            print("Password validation result:", user.check_password(password))
            return jsonify({'error': 'Invalid username or password'}), 401
        print(user)
        # If credentials are correct, login user and return success message
        login_user(user)
        print("the user type is: " + user.user_type)
        project_id = get_project_id_for_user(username)  # Implement this function to get the project ID for the user
        #project_details = get_project_details(project_id)
        redirect_url = '/admin' if user.user_type == 'farmer' else '/investor'
        return jsonify({'success': True, 'redirect_url': redirect_url, 'username': username, 'project_id': project_id}), 200
    
    # Handle potential GET requests here (optional, e.g., redirect to login form)
    csrf_token= generate_csrf()
    print('CSRF Token:', csrf_token)
    return render_template('register.html',title='login',login_form=login_form,register_form=register_form, csrf_token=csrf_token)  # Adjust template name if needed


@app.route('/user_projects/<username>')
@login_required
def user_projects(username):
    user = Users.query.filter_by(username=username).first()
    if user is None:
        return jsonify({'error': 'User not found'}), 404

    # Fetch projects associated with the user
    user_projects = Projects.query.filter_by(user_id=user.id).all()

    # Process project data into a format suitable for JSON response
    projects_data = []
    for project in user_projects:
        print("if the new route is working")
        projects_data.append({
            'project_name': project.project_name,
            'description': project.description,
            'investment_goal': project.investment_goal,
            'location': project.location
            # Add more fields if needed
        })

    return jsonify(projects_data)

@app.route('/project_details/<project_id>')
@login_required
def project_details(project_id):
    project = Projects.query.get(project_id)
    if project is None:
        return jsonify({'error': 'Project not found'}), 404

    # Fetch current investment and ROI for the project
    current_investment = project.current_investment
    roi = project.ROI  # Assuming ROI is a field in the Projects model
    print("if the second new route is working")
    # Process project details into a format suitable for JSON response
    project_details = {
        'project_name': project.project_name,
        'description': project.description,
        'investment_goal': project.investment_goal,
        'location': project.location,
        'current_investment': current_investment,
        'roi': roi
        # Add more fields if needed
    }

    return jsonify(project_details)


