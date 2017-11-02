#!/usr/bin/ruby

require 'faraday'
require 'slop'
require 'whenever'


# Main execution point
if __FILE__ == $0
  # Parse command line arguments
  opts = Slop.parse do |o|
    o.banner = 'Usage: evil_whale.rb [options] ...'
    o.separator ''

    o.separator 'Options:'
    o.float     '-p', '--ping', 'ping interval in seconds (default: 0, i.e. no repeat)', default: 0
    o.int       '-l', '--load', 'load factor; cpu ~ 2^(2 * l) (default: 10)', default: 10
    o.string    '-a', '--addr', 'target address'
    o.on        '-h', '--help', 'print this help' do
        puts o
        exit
    end
  end


  threads = []
  i = 0
  loop do
    # Send request with given load factor
    threads << Thread.new {
      j = i
      i += 1
      response = Faraday.get "#{ opts[:addr] }/#{ opts[:load] }"
      puts "Ping #{ j } time: #{ response.body }"
    }

    # Continue if ping interval is set
    break unless opts[:ping] > 0
    sleep( opts[:ping] )
  end

  # Wait on threads for completion
  threads.each( &:join )
end
