require 'jimson'
require 'json'
require 'work_queue'

client = Jimson::Client.new('http://127.0.0.1:8080')
wq = WorkQueue.new 5, nil
results = Array.new

Dir.glob "./var/log/secure*" do |file|
    wq.enqueue_b do
        content = File.read file
        results << client.parse_log(content)
    end
end
wq.join

aggregate = Hash.new
results.each do |result|
    result.each do |key, value|
        if aggregate.include? key
            aggregate[key] += value
        else
            aggregate[key] = value
        end
    end
end

puts aggregate
