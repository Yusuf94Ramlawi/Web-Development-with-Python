from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def dashboard():
    return render_template('index.html')

@app.route('/equipment')
def equipment():
    return render_template('equipment/list.html')

@app.route('/equipment/add', methods=['GET', 'POST'])
def add_equipment():
    if request.method == 'POST':
        return redirect(url_for('equipment'))
    return render_template('equipment/form.html')

@app.route('/equipment/edit/<int:id>', methods=['GET', 'POST'])
def edit_equipment(id):
    if request.method == 'POST':
        return redirect(url_for('equipment'))
    return render_template('equipment/form.html', id=id)

@app.route('/equipment/delete/<int:id>', methods=['POST'])
def delete_equipment(id):
    return redirect(url_for('equipment'))

@app.route('/equipment/<int:id>')
def view_equipment(id):
    return render_template('equipment/detail.html', id=id)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)