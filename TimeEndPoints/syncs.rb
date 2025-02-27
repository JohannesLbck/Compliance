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
  timestamp = params["timestamp"]
  # Convert the timestamp to a Time object
  begin
    target_time = parse_time(timestamp)
  rescue ArgumentError
    halt 400, { error: 'Invalid timestamp format' }.to_json
  end
  # Calculate the delay in seconds
  delay = target_time - Time.now

  # If the target time is in the past, return immediately
  if delay <= 0
    { waited: false }.to_json
  else
    # Wait until the specified time
    sleep(delay)

    # Return a response
    { waited: true }.to_json
  end
end

get '/return_time' do
  content_type :json
  time = Time.now.to_i
  { Time: time}.to_json
end

post '/due_date' do
  content_type :json

  timestamp = params["timestamp"]
  diff = timestamp - Time.now
  if diff < 0
    { result: True}.to_json
  else
    { result: False}.to_json
  end
end



