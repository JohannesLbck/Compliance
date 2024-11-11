#!/usr/bin/ruby
require 'sinatra'
require 'json'

post '/' do
  pp JSON::parse(params['notification'])
  nil
end
