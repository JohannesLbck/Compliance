#!/usr/bin/ruby
require 'riddl/server'

class Test < Riddl::Implementation
  def response
    [
      Riddl::Parameter::Simple.new("id","Aeroflot"),
      Riddl::Parameter::Simple.new("costs","12.3"),
      Riddl::Parameter::Complex.new("something","application/json","[ { \"a\": 3} ]")
    ]
  end
end

Riddl::Server.new("test1.xml", :host =>"::", :port => 20033 ) do
  on resource do
    run Test if get
  end
end.loop!

