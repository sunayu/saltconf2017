#!/usr/bin/ruby

require 'sinatra'

set :bind, '0.0.0.0'

get '/:x' do |x|
  puts x

  start = Time.now

  f = x.to_i

  f.times do |i|
    f.times do |j|
      Math.sqrt(j) * i / 0.2
    end
  end

  elapsed = Time.now - start
  response['Access-Control-Allow-Origin'] = '*'
  puts "Elapsed: #{ elapsed }"
  elapsed.to_s
end
