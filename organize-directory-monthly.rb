#! /usr/bin/env ruby
# coding: utf-8
#
# フォルダ内のファイルを月単位のフォルダに整理する。
#
# [BEFORE]
#   log/
#     `- teraterm/
#          +- HOST_A_20191105_160850.log
#          +- HOST_B_20191105_170202.log
#          `- HOST_A_20191205_093456.log
#
# [AFTER]
#   log/
#     `- teraterm/
#          +- 201911/
#          |    +- HOST_A_20191105_160850.log
#          |    `- HOST_B_20191105_170202.log
#          `- 201912/
#               `- HOST_A_20191205_093456.log
#

require 'fileutils'

def find_files(dirname, glob_pattern)
  Dir.chdir(dirname)
  return Dir.glob(glob_pattern).select {|e| File.file?(e) }.map {|e| File.expand_path(e) }
end

def move_logfiles(logfiles)
  logfiles.each {|logfile|
    dirname = File.dirname(logfile)
    filename = File.basename(logfile)
    date = logfile.slice(/.*?((?:19|20)\d\d[01]\d)\d\d.*/, 1)
    
    if date.nil?
      puts "skip #{logfile}"
      next
    end

    dstdir = File.join(dirname, date)
    FileUtils.mkdir_p(dstdir)

    dstpath = File.join(dstdir, filename)
    if not File.exist?(dstpath)
      FileUtils.move(logfile, dstpath)
      puts "move #{logfile}"
    else
      puts "skip #{logfile} (exists)"
    end
  }
end

def main
  if ARGV.size != 2
    usage = <<-STR
      error: invalid arguments.

      USAGE:
        organize-directory-monthly.rb directory glob_pattern"
       
      EXAMPLE:
        organize-directory-monthly.rb teraterm '*.log'
    STR
    
    STDERR.puts usage.gsub(/^ {6}/, '')
    exit 1
  end
  
  dirname = ARGV.shift
  glob_pattern = ARGV.shift
  
  logfiles = find_files(dirname, glob_pattern)
  move_logfiles(logfiles)
end

main
