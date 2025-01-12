from app import redis

class Poll:
    @staticmethod
    def create(question, options):
        poll_id = redis.incr('poll_id')
        poll_data = {
            'question': question,
            'options': options,
            'votes': [0] * len(options)
        }
        redis.hmset(f'poll:{poll_id}', poll_data)
        redis.hset('polls', poll_id, question)
        return poll_id

    @staticmethod
    def get(poll_id):
        poll_data = redis.hgetall(f'poll:{poll_id}')
        if poll_data:
            poll_data['options'] = eval(poll_data['options'])
            poll_data['votes'] = eval(poll_data['votes'])
        return poll_data

    @staticmethod
    def vote(poll_id, option_index):
        poll_data = Poll.get(poll_id)
        if poll_data:
            poll_data['votes'][option_index] += 1
            redis.hset(f'poll:{poll_id}', 'votes', poll_data['votes'])

    @staticmethod
    def all():
        polls = redis.hgetall('polls')
        return polls

    @staticmethod
    def delete(poll_id):
        redis.delete(f'poll:{poll_id}')
        redis.hdel('polls', poll_id)