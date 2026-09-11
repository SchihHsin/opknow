-- Keep Pandoc figure numbering/captions while adding ACM accessibility text.
-- Every Markdown figure must carry description="..." on its image or figure.
function Table(tbl)
  if #tbl.colspecs == 3 then
    local header = pandoc.utils.stringify(tbl.head)
    local widths = header:match("^ID") and {0.07, 0.27, 0.66} or {0.25, 0.31, 0.44}
    if header:match("^Indicator") then widths = {0.54, 0.23, 0.23} end
    for i=1,3 do tbl.colspecs[i][2] = widths[i] end
    if header:match("^Indicator") then
      return {pandoc.RawBlock("latex", "\\ifdefined\\Needspace\\Needspace{14\\baselineskip}\\fi"), tbl}
    end
  elseif #tbl.colspecs == 5 then
    local widths = {0.40, 0.10, 0.16, 0.16, 0.18}
    for i=1,5 do tbl.colspecs[i][2] = widths[i] end
  end
  return tbl
end

function Figure(figure)
  local description = figure.attributes.description
  local function inspect(image)
    description = description or image.attributes.description
    image.attributes.description = nil
    -- The full caption already belongs to Figure.caption. ACM uses Description
    -- for accessibility; suppress Pandoc's newer graphicx alt= option so the
    -- generated source also compiles with established TeX distributions.
    image.caption = {}
    -- Constrain both dimensions while preserving the original aspect ratio.
    if not image.attributes.width then image.attributes.width = "100%" end
    return image
  end
  figure = figure:walk({Image = inspect})
  if not description or description == "" then
    error("Figure " .. figure.identifier .. " needs a description attribute for ACM accessibility.")
  end
  local escaped = pandoc.write(pandoc.Pandoc({pandoc.Plain({pandoc.Str(description)})}), "latex")
  escaped = escaped:gsub("%s+$", "")
  -- A second block in Figure.content becomes a side-by-side minipage in
  -- Pandoc 3.11. Add the command to the existing image paragraph instead.
  local inserted = false
  for _, block in ipairs(figure.content) do
    if block.t == "Plain" or block.t == "Para" then
      block.content:insert(pandoc.RawInline("latex", "\\Description{" .. escaped .. "}"))
      inserted = true
      break
    end
  end
  if not inserted then error("Figure requires an image paragraph.") end
  figure.attributes.description = nil
  -- Keep the short rubric illustrations next to their explanatory paragraphs.
  if figure.identifier:match("^fig:scoring%-") then
    local rendered = pandoc.write(pandoc.Pandoc({figure}), "latex")
    rendered = rendered:gsub("\\begin{figure}", "\\begin{figure}[H]", 1)
    return pandoc.RawBlock("latex", rendered)
  end
  return figure
end
