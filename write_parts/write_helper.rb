require 'fileutils'
require 'shellwords'

module WriteHelper
  def generate
    make
  ensure
    @_file.close if @_file
    @_file = nil
  end

  # DSL
  def file(filepath)
    @_file.close if @_file
    @_file = write_helper_open(filepath)
  end
  
  def out(*args)
    if @_file.nil?
      raise "file not open."
    end
    @_file.puts(*args)
  end
  
  ['title', 'section', 'subsection', 'echo'].each {|m|
    module_eval "def #{m}(message); @_write_helper_handlers[:#{m}].call(message) end"
  }

  module ClassMethods
    def generate(context)
      self.new(context).generate
    end
  end
  def self.included(base)
    base.extend(ClassMethods)
  end
  
  def write_helper_setup
    write_helper_mode(:shell)
  end
  
  def write_helper_mode(mode)
    @_write_helper_handlers =
      case mode
      when :shell
        {
          :open       => method(:write_helper_sh_open),
          :title      => method(:write_helper_sh_title),
          :section    => method(:write_helper_sh_section),
          :subsection => method(:write_helper_sh_subsection),
          :echo       => method(:write_helper_sh_echo),
        }
      else
        raise "undefined helper mode: #{mode}"
      end
  end

  def write_helper_extend_instance_variable(hash)
    hash.map {|key, value|
      instance_variable_set("@#{key}", value)
    }
  end

  def write_helper_open(filepath, &block);
    FileUtils.mkdir_p(File.dirname(filepath))
    @_write_helper_handlers[:open].call(filepath, &block)
  end
  
  def write_helper_sh_open(filepath, &block)
    if block
      File.open(filepath, 'w') {|f|
        @_file = f
        out "#!/bin/bash\n"
        yield(f)
      }
      @_file = nil
    else
      return File.open(filepath, 'w')
    end
  end
  
  def write_helper_sh_title(message)
    border = sprintf('#' * (message.length + 10))
    out 'echo ' + Shellwords.escape(border)
    out 'echo ' + Shellwords.escape("#### #{message} ####")
    out 'echo ' + Shellwords.escape(border)
  end
  
  def write_helper_sh_section(message)
    border = '#*' + ('*' * message.size) + ('*' * 10)
    out 'echo ' + Shellwords.escape(border)
    out 'echo ' + Shellwords.escape("# #{message}")
    out 'echo ' + Shellwords.escape(border)
  end

  def write_helper_sh_subsection(message)
    border = '#-' + ('-' * message.size) + ('-' * 5)
    out 'echo ' + Shellwords.escape(border)
    out 'echo ' + Shellwords.escape("# #{message}")
    out 'echo ' + Shellwords.escape(border)
  end

  def write_helper_sh_echo(message)
    out 'echo ' + Shellwords.escape(message)
  end
end
