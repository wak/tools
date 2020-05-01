#! /usr/bin/env ruby

require './write_parts'

class SingleSample < WriteParts::SingleFileBase
  def post_initialize
    @filepath = 'out/single/A.txt'
    instance_variable_set_from_hash(@context)
  end

  def make
    title 'sample'
    section 'test'
    subsection 'test'

    out @text
  end
end

SingleSample.generate({:text => 'hello'})
