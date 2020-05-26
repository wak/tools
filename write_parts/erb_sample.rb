#! /usr/bin/env ruby

require './erb_helper'

class MyTemplate
  include ERBHelper

  def post_initialize(map)
    @template = 'in/template.erb'
    @internal_encoding = Encoding::UTF_8
    @external_encoding = Encoding::SJIS
  end

  def greeting(who)
    "Hello, #{who}."
  end

  def test?
    true
  end
end

puts MyTemplate.build({:subject => 'Template test', :greeting => 'hello'})
MyTemplate.make_file('out/erb_sample.txt', {:subject => 'Template test', :greeting => 'hello'})
