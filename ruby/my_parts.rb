
class String
  def color(fg_color, bg_color = nil, attr = nil)
    attr_val = ({ :bold  => 1, :underline => 4,
                  :blink => 5, :reverse   => 7 }[attr] || 0)
    colors = {
      :black  => 0, :red  => 1, :green   => 2,
      :yellow => 3, :blue => 4, :magenta => 5,
      :cyan   => 6, :white => 7
    }
    background = nil
    background = ";4#{(colors[bg_color]||0)}" if bg_color
    foreground = "3#{(colors[fg_color]||0)}"

    return "\e[#{attr_val};#{foreground}#{background}m#{self}\e[m"
  end
end

class Array
  def continuous_numbers?
    f = self.first

    self.each {|n|
      return false if !n.is_a?(Number)
      return false if n != f

      f = f + 1
    }
    return true
  end
end

class Integer
  def to_s_excel
    value = self
    raise ArgumentError.new('must positive') if value < 0

    mapping = %w{a b c d e f g h i j k l m n o p q r s t u v w x y z}
    parts = []
    while value >= 0
      parts << mapping[value % 26]
      value = (value / 26) - 1
    end
    return parts.reverse.join.upcase
  end
end

class String
  def to_i_excel
    mapping = %w{a b c d e f g h i j k l m n o p q r s t u v w x y z}
    result = 0
    self.each_char {|char|
      pos = mapping.index(char.downcase)
      raise ArgumentError('Invalid Excel row format') if pos.nil?
      result = (result * mapping.size) + pos + 1
    }
    return result - 1
  end
end
