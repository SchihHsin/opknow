-- Layout filter for the Word manuscript build (build_manuscript_docx.py).
--
-- Two jobs, both of which have to happen inside pandoc rather than in the
-- markdown, so manuscript-en-v0.2.md stays the single editable source:
--
--  1. Table column widths. Pandoc lays every pipe table out with equal
--     columns; these are the canonical widths already used by the ACM/LaTeX
--     build in submission/acm-figures.lua, never invented per format.
--  2. Figure sizing and rasterisation. Word cannot embed the SVG artwork
--     pandoc is handed, so every figure is re-pointed at the PNG rendered by
--     the same build script and pinned to the text width.

-- Widths mirror submission/acm-figures.lua so the LaTeX, HTML and Word
-- versions of the paper break their tables the same way.
local WIDTHS = {
  id_three        = { 0.07, 0.27, 0.66 },
  indicator_three = { 0.54, 0.23, 0.23 },
  plain_three     = { 0.25, 0.31, 0.44 },
  four            = { 0.40, 0.12, 0.24, 0.24 },
  five            = { 0.40, 0.10, 0.16, 0.16, 0.18 },
}

-- A4 with 22 mm margins leaves 166 mm of text; 160 mm keeps the artwork clear
-- of the table borders Word draws for figures.
local FIGURE_WIDTH = "6.3in"

local function set_widths(tbl, widths)
  if #tbl.colspecs ~= #widths then return tbl end
  for i = 1, #widths do
    tbl.colspecs[i] = { tbl.colspecs[i][1], widths[i] }
  end
  return tbl
end

function Table(tbl)
  local header = pandoc.utils.stringify(tbl.head)
  local n = #tbl.colspecs
  if n == 3 then
    if header:match("^ID") then return set_widths(tbl, WIDTHS.id_three) end
    if header:match("^Indicator") then return set_widths(tbl, WIDTHS.indicator_three) end
    return set_widths(tbl, WIDTHS.plain_three)
  elseif n == 4 then
    return set_widths(tbl, WIDTHS.four)
  elseif n == 5 then
    return set_widths(tbl, WIDTHS.five)
  end
  return tbl
end

local function shape(image)
  image.attributes.description = nil
  image.attributes.width = FIGURE_WIDTH
  image.src = image.src:gsub("%.svg$", ".png")
  return image
end

function Figure(figure)
  figure.attributes.description = nil
  return figure:walk({ Image = shape })
end

function Image(image)
  return shape(image)
end
