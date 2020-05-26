# coding: utf-8

require 'erb'

module ERBHelper
  def self.included(base)
    base.extend(ClassMethods)
  end

  def initialize(map)
    @external_encoding = Encoding::UTF_8
    @internal_encoding = Encoding::UTF_8

    if map.is_a?(Hash)
      map.each {|key, value| instance_variable_set("@#{key}", value) }
    end

    post_initialize(map)
  end

  def post_initialize(map)
  end

  def __build
    # 昔のRubyなら、(text, nil, '-')
    erb = ERB.new(__read, trim_mode: '-')
    erb.result(binding)
  end

  def __make_file(outfile)
    File.open(outfile, 'w',
              :internal_encoding => @internal_encoding,
              :external_encoding => @external_encoding) {|f|
      f.write(__build)
    }
  end

  def __read
    File.open(@template,
              :internal_encoding => @internal_encoding,
              :external_encoding => @external_encoding) {|f|
      return f.read
    }
  end

  module ClassMethods
    def build(map)
      self.new(map).__build
    end

    def make_file(outfile, map)
      self.new(map).__make_file(outfile)
    end
  end
end
