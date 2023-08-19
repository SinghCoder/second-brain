from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/slack/events', methods=['POST'])
def slack_events():
    data = request.json
    
    # Check if the request contains a challenge field
    if 'challenge' in data:
        return jsonify({"challenge": data['challenge']})

    event_type = data['event']['type']
    # Print only the message events:
    if event_type == 'message':
        # Format: User <user_id> sent message: <msg>
        print(f"User {data['event']['user']} sent message: {data['event']['text']}")

    # Respond to Slack to acknowledge receipt
    return jsonify({"message": "Event received"})

@app.route('/telegram', methods=['POST'])
def telegram_events():
    data = request.json
    print(data)
    return jsonify({"message": "Event received"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
