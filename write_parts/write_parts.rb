require 'shellwords'

module WriteHelper
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
end

class FileBase
  include WriteHelper
  
  def initialize(context)
    @context = context
    @filepath = nil

    post_initialize
  end

  def generate
    if @context[:io]
      @file = @context[:io]
      make
    else
      File.open(@filepath, 'w') {|f|
        @file = f
        make
      }
    end
  end

  def self.generate(context)
    self.new(context).generate
  end
end

class FileA < FileBase
  def post_initialize
    @filepath = 'A.txt'
  end

  def make()
    sh_title 'sample'
    sh_section 'test'
    sh_subsection 'test'
  end
end

FileA.generate({:a => 123})


class MultiFileBase
  include WriteHelper
  
  def initialize(context)
    @context = context
    post_initialize
  end

  def post_initialize
  end
  
  def make_file(filepath)
    File.open(filepath, 'w') {|f|
      @file = f
      yield
    }
  end
  
  def generate
    make
  end

  def self.generate(context)
    self.new(context).generate
  end
end

class FileBC < MultiFileBase
  def make
    make_file('B.txt') { sampleB }
    make_file('C.txt') { sampleC }
  end

  def sampleB
    out 'sampleB'
  end
  
  def sampleC
    out 'sampleC'
  end
end

FileBC.generate({:b => 321})
