from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
import json

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Required for session management

slots = {
    "Day 1": [True] * 10,
    "Day 2": [True] * 10,
    "Day 3": [True] * 10,
    "Day 4": [True] * 10,
    "Day 5": [True] * 10,
    "Day 6": [True] * 10,
}

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        roll = request.form.get('roll')
        id = request.form.get('id')
        with open("data.json","r") as f:
             data = json.load(f)
        if roll in data and data[roll][0] == id:
            session['user'] = roll
            flash('Login successful!', 'success')
            return redirect(url_for('booking_page'))
        else:
            flash('Invalid credentials. Please try again.', 'danger')

    return render_template('login.html')

@app.route('/booking_page')
def booking_page():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('page.html', slots=slots)

@app.route('/book', methods=['POST'])
def book():
    if 'user' not in session:
        return jsonify({"status": "failure", "message": "You need to log in first."})

    user = session['user']
    data = request.get_json()
    day = data.get('day')
    slot = data.get('slot')

    # Check if the user has already booked a slot
    if 'booked_slot' in session:
        booked_slot = session['booked_slot']
        return jsonify({"status": "failure", "message": f"You have already booked Slot {booked_slot}."})

    # Proceed with booking if the slot is available
    if slots[day][slot]:
        slots[day][slot] = False
        session['booked_slot'] = f"{day} Slot {slot + 1}"
        return jsonify({"status": "success", "message": f"Slot {slot + 1} on {day} booked successfully."})
    else:
        return jsonify({"status": "failure", "message": "Slot already booked."})

@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('booked_slot', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, port=5555)
