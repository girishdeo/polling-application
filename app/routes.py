from flask import render_template, request, redirect, url_for
from app import app, redis

@app.route('/')
def index():
    polls = redis.hgetall('polls')
    return render_template('index.html', polls=polls)

@app.route('/poll/<poll_id>')
def poll(poll_id):
    poll = redis.hgetall(f'poll:{poll_id}')
    return render_template('poll.html', poll=poll)

@app.route('/create_poll', methods=['POST'])
def create_poll():
    poll_id = redis.incr('poll_id')
    question = request.form['question']
    options = request.form.getlist('options')
    redis.hmset(f'poll:{poll_id}', {'question': question, 'options': options, 'votes': [0] * len(options)})
    redis.hset('polls', poll_id, question)
    return redirect(url_for('index'))

@app.route('/vote/<poll_id>', methods=['POST'])
def vote(poll_id):
    option_index = int(request.form['option'])
    poll = redis.hgetall(f'poll:{poll_id}')
    votes = list(map(int, poll['votes']))
    votes[option_index] += 1
    redis.hset(f'poll:{poll_id}', 'votes', votes)
    return redirect(url_for('poll', poll_id=poll_id))