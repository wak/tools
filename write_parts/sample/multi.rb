#! /usr/bin/env ruby

require './write_parts'

class MultiSample < WriteParts::MultiFileBase
  def post_initialize
    instance_variable_set_from_hash(@context)
  end
  
  def make
    make_file('out/multi/A.txt') { sampleA }
    make_file('out/multi/B.txt') { sampleB }
  end

  def sampleA
    out "multi: #{@var1}"
  end
  
  def sampleB
    out "multi: #{@var2}"
  end
end

MultiSample.generate({:var1 => 'var1', :var2 => 'var2'})
