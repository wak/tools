#! /usr/bin/env ruby

require './write_helper'

class SampleFile
  include WriteHelper

  def initialize(context)
    write_helper_setup
    write_helper_extend_instance_variable(context)
  end

  def make
    make_file_a
    make_file_b
  end

  def make_file_a
    file 'out/A.txt'
    title 'sample'
    section 'test'
    subsection 'test'

    echo @text
  end

  def make_file_b
    file 'out/B.txt'
    echo 'test B'
  end
end

SampleFile.generate({:text => 'hello'})
