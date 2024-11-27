#!/usr/bin/ruby
require 'sinatra'
require 'json'
require 'time'


set :port, 9322

def parse_time(input)
  if input.match?(/^\d+$/) # Check if input is a number (Unix timestamp)
    Time.at(input.to_i)
  else
    Time.parse(input)
  end
end

# accepts timestamp, waits until the timestamp to sync up 
post '/wait_until' do
  content_type :json

  # Parse the request body for the timestamp
  request_payload = JSON.parse(request.body.read)
  timestamp = request_payload['timestamp']

  # Convert the timestamp to a Time object
  begin
    target_time = Time.parse_time(timestamp)
  rescue ArgumentError
    halt 400, { error: 'Invalid timestamp format' }.to_json
  end

  # Calculate the delay in seconds
  delay = target_time - Time.now

  # If the target time is in the past, return immediately
  if delay <= 0
    { waited: False }.to_json
  else
    # Wait until the specified time
    sleep(delay)

    # Return a response
    { waited: True }.to_json
  end
end

