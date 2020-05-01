require 'fileutils'
require 'shellwords'

module WriteParts
  module WriteHelper
    def helper_setup
      helper_mode(:shell)
    end
    
    def helper_mode(mode)
      @helper_mode = mode
      @helper_handlers =
        case mode
        when :shell
          {
            :open       => method(:sh_open),
            :title      => method(:sh_title),
            :section    => method(:sh_section),
            :subsection => method(:sh_subsection),
          }
        else
          raise "undefined helper mode: #{mode}"
        end
    end

    def instance_variable_set_from_hash(hash)
      hash.map {|key, value|
        instance_variable_set("@#{key}", value)
      }
    end

    def open(filepath, &block);
      FileUtils.mkdir_p(File.dirname(filepath))
      @helper_handlers[:open].call(filepath, &block)
    end
    def title(message); @helper_handlers[:title].call(message) end
    def section(message); @helper_handlers[:section].call(message) end
    def subsection(message); @helper_handlers[:subsection].call(message) end
    
    def sh_open(filepath)
      File.open(filepath, 'w') {|f|
        @file = f
        out "#!/bin/bash\n"
        yield(f)
      }
      @file = nil
    end
    
    def sh_title(message)
      border = sprintf('#*%s*#', '*' * (message.length + 10))
      out border.center(80)
      out message.center(80)
      out border.center(80)
    end
    
    def sh_section(message)
      border = '#*' + ('*' * message.size) + ('*' * 10)
      out "echo #{border}"
      out "echo # #{Shellwords.escape(message)}"
      out "echo #{border}"
    end

    def sh_subsection(message)
      border = '#-' + ('-' * message.size) + ('-' * 5)
      out "echo #{border}"
      out "echo # #{Shellwords.escape(message)}"
      out "echo #{border}"
    end

    def out(*args)
      @file.puts(*args)
    end

    
    module ClassMethods
      def build(map)
        self.new(map).__build
      end
    end
  end

  class SingleFileBase
    include WriteHelper
    
    def initialize(context)
      @context = context
      @filepath = nil
      helper_setup

      post_initialize
    end

    def generate
      if @context[:io]
        @file = @context[:io]
        make
      else
        open(@filepath) {|f|
          @file = f
          make
        }
      end
    end

    def self.generate(context)
      self.new(context).generate
    end
  end

  class MultiFileBase
    include WriteHelper
    
    def initialize(context)
      @context = context
      helper_setup
      post_initialize
    end

    def post_initialize
    end
    
    def make_file(filepath)
      open(filepath) {|f|
        yield(f)
      }
    end
    
    def generate
      make
    end

    def self.generate(context)
      self.new(context).generate
    end
  end
end
