from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Database connection helper
def get_db_connection():
    conn = sqlite3.connect('voting_system.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        voter_id = request.form['voter_id']
        
        conn = get_db_connection()
        voter = conn.execute('SELECT * FROM voters WHERE voter_id = ?', (voter_id,)).fetchone()
        conn.close()
        
        if voter is None:
            flash('Invalid Voter ID!', 'error')
            return redirect(url_for('login'))
        
        if voter['has_voted']:
            flash('You have already voted!', 'error')
            return redirect(url_for('login'))
        
        session['voter_id'] = voter_id
        session['logged_in'] = True
        return redirect(url_for('vote'))
    
    return render_template('login.html')

@app.route('/vote', methods=['GET', 'POST'])
def vote():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    
    if request.method == 'POST':
        candidate_id = request.form['candidate_id']
        
        # Update candidate votes
        conn.execute('UPDATE candidates SET votes = votes + 1 WHERE id = ?', (candidate_id,))
        
        # Mark voter as voted
        conn.execute('UPDATE voters SET has_voted = TRUE WHERE voter_id = ?', (session['voter_id'],))
        
        conn.commit()
        conn.close()
        
        session.pop('voter_id', None)
        session.pop('logged_in', None)
        
        flash('Thank you for voting!', 'success')
        return redirect(url_for('results'))
    
    candidates = conn.execute('SELECT * FROM candidates').fetchall()
    conn.close()
    
    return render_template('vote.html', candidates=candidates)

@app.route('/results')
def results():
    conn = get_db_connection()
    candidates = conn.execute('SELECT * FROM candidates ORDER BY votes DESC').fetchall()
    total_votes = conn.execute('SELECT SUM(votes) as total FROM candidates').fetchone()['total']
    conn.close()
    
    return render_template('results.html', candidates=candidates, total_votes=total_votes)

@app.route('/logout')
def logout():
    session.pop('voter_id', None)
    session.pop('logged_in', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Initialize database if it doesn't exist
    if not os.path.exists('voting_system.db'):
        from init_db import init_database
        init_database()
    
    app.run(debug=True)