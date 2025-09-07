import os
import subprocess
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, send_from_directory
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = os.urandom(24)

UPLOAD_FOLDER = '/srv/backups/timemachine'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ADMIN_USER = 'admin'
ADMIN_PASS = 'password'

@app.route('/')
def index():
    if 'logged_in' in session:
        return render_template('index.html')
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == ADMIN_USER and request.form['password'] == ADMIN_PASS:
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            return 'Invalid credentials'
    return render_template('login.html')

@app.route('/users_data')
def users_data():
    if not 'logged_in' in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    users = []
    try:
        output = subprocess.check_output(['getent', 'passwd'], universal_newlines=True)
        for line in output.splitlines():
            parts = line.split(':')
            if int(parts[2]) >= 1000 and int(parts[2]) < 60000:
                users.append(parts[0])
    except subprocess.CalledProcessError as e:
        return jsonify({'error': f'Failed to list users: {e.stderr}'}), 500

    return jsonify(users)

@app.route('/files_data')
def files_data():
    if not 'logged_in' in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    file_list = []
    try:
        output = subprocess.check_output(['sudo', 'ls', '-la', app.config['UPLOAD_FOLDER']], universal_newlines=True)
        lines = output.splitlines()
        for line in lines[1:]:
            parts = line.split()
            if len(parts) >= 9:
                file_list.append({
                    'name': parts[8],
                    'size': parts[4],
                    'owner': parts[2]
                })
    except subprocess.CalledProcessError as e:
        return jsonify({'error': f'Failed to list files: {e.stderr}'}), 500

    return jsonify(file_list)

@app.route('/create_user', methods=['POST'])
def create_user():
    if not 'logged_in' in session:
        return jsonify({'error': 'Unauthorized'}), 401
    username = request.json.get('username')
    password = request.json.get('password')

    try:
        cmd_useradd = ['sudo', 'useradd', '-m', username]
        subprocess.run(cmd_useradd, check=True, capture_output=True, text=True)
        
        cmd_smbpasswd = ['sudo', 'smbpasswd', '-a', username]
        p = subprocess.Popen(cmd_smbpasswd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = p.communicate(input=f'{password}\n{password}\n')
        if p.returncode != 0:
            raise subprocess.CalledProcessError(p.returncode, cmd_smbpasswd, output=stdout, stderr=stderr)

        return jsonify({'message': f'User {username} created successfully!'}), 200
    except subprocess.CalledProcessError as e:
        return jsonify({'error': f'Failed to create user. Error: {e.stderr}'}), 500
        
@app.route('/delete_user', methods=['POST'])
def delete_user():
    if not 'logged_in' in session:
        return jsonify({'error': 'Unauthorized'}), 401
    username = request.json.get('username')

    if username in ['root', 'user', 'tm_backup', 'admin']:
        return jsonify({'error': 'Cannot delete critical system or admin users.'}), 400

    try:
        cmd = ['sudo', 'deluser', '--remove-home', username]
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        return jsonify({'message': f'User {username} deleted successfully!'}), 200
    except subprocess.CalledProcessError as e:
        return jsonify({'error': f'Failed to delete user: {e.stderr}'}), 500

@app.route('/upload', methods=['POST'])
def upload_file():
    if not 'logged_in' in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected for uploading'}), 400
        
    try:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return jsonify({'message': f'File {filename} uploaded successfully!'}), 200
    except Exception as e:
        return jsonify({'error': f'Failed to upload file: {str(e)}'}), 500

@app.route('/download/<filename>')
def download_file(filename):
    if not 'logged_in' in session:
        return jsonify({'error': 'Unauthorized'}), 401
    try:
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)
    except Exception as e:
        return jsonify({'error': f'Failed to download file: {str(e)}'}), 500

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
