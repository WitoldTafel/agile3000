from flask import Flask, render_template, redirect, request, session
import csv
app = Flask(__name__)

@app.route('/')
def route_index():
    return render_template('index.html', stories = list_of_dic_from_file() )

@app.route('/story')
def story_add():
    return render_template('story.html')

@app.route('/story', methods=['POST'])
def route_save():
    session['story'] = request.form
    write_form_to_file()
    return redirect('/')

@app.route('/story/<story_id>')
def story_edit(story_id):
    dict = list_of_dic_from_file()[int(story_id)-1]
    return render_template('story.html',dict=dict)


@app.route('/story/<story_id>', methods=['POST'])
def save_edit(story_id):
    session['story'] = request.form
    replace_row_in_file(int(story_id))
    return redirect('/')
    


def write_form_to_file():
    with open('data.csv', 'a') as f: 
        w = csv.DictWriter(f, sorted(session['story'].keys()))
        w.writerow(session['story'])

def replace_row_in_file(row_number):
    list_dict = list_of_dic_from_file()
    list_dict[row_number-1] = session['story']
    with open('data.csv', 'w') as f: 
        w = csv.DictWriter(f, sorted(session['story'].keys()))
        w.writerows(list_dict)


def list_of_dic_from_file():
        with open("data.csv", 'r') as f:
            reader = csv.DictReader(f,sorted(session['story'].keys()))
            dics = [ d for d in reader ]
            
        return dics





if __name__ == "__main__":
  app.secret_key = 'wiciumistrz' 
  app.run(
      debug=True,  # Allow verbose error reports
      port=5000  # Set custom port
  )