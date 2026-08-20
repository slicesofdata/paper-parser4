def split_frontmatter_and_intro(blocks):
    """
    Splits leading blocks into: title, authors, abstract, keywords, introduction.
    Returns dict of section_name -> list of blocks.
    Consumes blocks until the first text_level >= 2 heading is found.
    """
    sections = {"title": [], "authors": [], "abstract": [], 
                "keywords": [], "introduction": []}
    
    stage = "title"  # state machine: title → authors → abstract → keywords → intro
    
    for block in blocks:
        if block.get("type") != "text":
            # figures/tables/equations get attached to current stage
            sections[stage if stage != "title" else "introduction"].append(block)
            continue
        
        text = block.get("text", "").strip()
        level = block.get("text_level")
        
        # Hit a real section heading - stop consuming
        if level and level >= 2:
            return sections, block  # return remaining-start marker
        
        # Title
        if stage == "title" and level == 1:
            sections["title"].append(block)
            stage = "authors"
            continue
        
        # Keywords line
        if text.lower().startswith(("keywords:", "key words:", "keyword:")):
            sections["keywords"].append(block)
            stage = "introduction"
            continue
        
        # Author blocks (short, institution-like)
        if stage == "authors":
            if len(text) < 300 and _looks_like_author_block(text):
                sections["authors"].append(block)
                continue
            else:
                # first long block after authors = abstract
                stage = "abstract"
        
        if stage == "abstract":
            sections["abstract"].append(block)
            stage = "post_abstract"  # next non-keyword block goes to intro
            continue
        
        if stage == "post_abstract":
            # if it's not keywords (handled above), it's introduction
            stage = "introduction"
        
        sections["introduction"].append(block)
    
    return sections, None


def _looks_like_author_block(text: str) -> bool:
    institution_keywords = ["university", "college", "institute", "department", 
                            "school", "laboratory", "hospital", "center", "centre"]
    lower = text.lower()
    return any(kw in lower for kw in institution_keywords) or len(text) < 100