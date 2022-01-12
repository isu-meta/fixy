from lxml import etree

NS = {
    "cdm": "http://www.oclc.org/contentdm",
    "mods": "http://www.loc.gov/mods/v3"
}


# Attributes

def add_update_attribute_roleTerm_type_text(mods):
    global NS
    xpath = "//mods:name/mods:role/mods:roleTerm"
    roleTerms = mods.xpath(xpath, namespaces=NS)

    for r in roleTerms:
        r.attrib["type"] = "text"
    
    return mods


def update_attribute_curator_authority_to_naf(mods):
    global NS
    xpath = "//mods:name[mods:role/mods:roleTerm/text() = 'curator']"
    curator = mods.xpath(xpath, namespaces=NS)[0]
    curator.attrib["authority"] = "naf"

    return mods


def update_attribute_collection_relatedItem_type_to_original(mods):
    global NS
    xpath = "//mods:relatedItem[@displayLabel='Collection']"
    collection = mods.xpath(xpath, namespaces=NS)[0]
    collection.attrib["type"] = "original"

    return mods

def update_attribute_language_type_to_code(mods):
    global NS
    xpath = "//mods:language/mods:languageTerm"
    language_term = mods.xpath(xpath, namespaces=NS)[0]
    language_term.attrib["type"] = "code"

# Elements


def add_element_date_digital(mods, cdm):
    global NS
    mods_xpath = "//mods:originInfo"
    cdm_xpath = "string(//cdm:date-digital/text())"

    originInfo = mods.xpath(mods_xpath, namespaces=NS)[0]
    date_digital = cdm.xpath(cdm_xpath, namespaces=NS)
    originInfo.append(
        etree.fromstring(
            f"<dateCaptured encoding='iso8601'>{date_digital}</dateCaptured>\n"
        )
    )

    return mods


def add_element_folder(mods, cdm):
    global NS
    mods_xpath = "//mods:titleInfo[@displayLabel='Folder']"
    cdm_xpath = "string(//cdm:Folder/text())"

    fix_me = mods.xpath(mods_xpath, namespaces=NS)[0]
    folder_number = cdm.xpath(cdm_xpath, namespaces=NS)
    fix_me.append(etree.fromstring(f"<title>{folder_number}</title>\n"))

    return mods


def add_element_folder_title(mods, cdm):
    global NS
    mods_xpath = "//mods:titleInfo[@displayLabel='Folder']"
    cdm_xpath = "string(//cdm:folder-title/text())"

    fix_me = mods.xpath(mods_xpath, namespaces=NS)[0]
    folder_title = cdm.xpath(cdm_xpath, namespaces=NS)
    fix_me.append(etree.fromstring(f"<title>{folder_title}</title>\n"))

    return mods



def add_element_genre_aat(mods, cdm):
    global NS
    mods_xpath = "//mods:mods"
    cdm_xpath = "string(//cdm:aat-type/text())"

    fix_me = mods.xpath(mods_xpath, namespaces=NS)[0]
    genre = cdm.xpath(cdm_xpath, namespaces=NS)
    fix_me.append(etree.fromstring(f'<genre authority="aat">{genre}</genre>\n'))

    return mods


def add_element_note_hardware_software(mods, cdm):
    global NS
    mods_xpath = "//mods:mods"
    cdm_xpath = "string(//cdm:hardware-software/text())"
    fix_me = mods.xpath(mods_xpath, namespaces=NS)[0]
    hardware_software = cdm.xpath(cdm_xpath, namespaces=NS)
    fix_me.append(etree.fromstring(f'<note type="hardware/software">{hardware_software}</note>\n'))
    
    return mods


def add_element_record_created(mods, cdm):
    global NS
    mods_xpath = "//mods:recordInfo"
    cdm_xpath = "string(//cdm:date-created/text())"
    fix_me = mods.xpath(mods_xpath, namespaces=NS)[0]
    record_created = cdm.xpath(cdm_xpath, namespaces=NS)
    fix_me.append(
        etree.fromstring(
            f'<recordCreationDate encoding="iso8601">{record_created}</recordCreationDate>\n'
        )
    )

    return mods


def add_element_local_id_from_ark(mods):
    global NS
    xpath = "//mods:mods"
    ark_xpath = "string(/mods:mods/mods:identifier[@type='ark'])"
    local_id = mods.xpath(ark_xpath, namespaces=NS)
    fix_me = mods.xpath(xpath, namespaces=NS)[0]
    fix_me.append(etree.fromstring(f'<identifier type="local">{local_id}</identifier>\n'))

    return mods


def add_element_local_id_noncdm(mods, local_id):
    global NS
    xpath = "//mods:mods"
    fix_me = mods.xpath(xpath, namespaces=NS)[0]
    fix_me.append(etree.fromstring(f'<identifier type="local">{local_id}</identifier>\n'))

    return mods


def remove_element_identifier_if_empty(mods):
    global NS
    xpath = "//mods:identifier[not(@*) and not(text())]"
    empty_identifiers = mods.xpath(xpath, namespaces=NS)
    
    if len(empty_identifiers) > 0:
        for i in empty_identifiers:
            i.getparent().remove(i)

    return mods


def update_element_ark(mods, new_ark):
    global NS
    xpath = "/mods:mods/mods:identifier[@type='ark']"
    ark_elem = mods.xpath(xpath, namespaces=NS)[0]
    ark_elem.text = new_ark

    return mods


def update_element_digital_collection_ark(mods, new_ark):
    global NS
    xpath = "//mods:relatedItem[@displayLabel='Digital Collection']/mods:identifier[@type='ark']"
    ark_elem = mods.xpath(xpath, namespaces=NS)[0]
    ark_elem.text = new_ark

    return mods


def update_element_finding_aid_ark(mods, new_ark):
    global NS
    xpath = "//mods:relatedItem[@displayLabel='Collection']/mods:identifier[@type='ark']"
    ark_elem = mods.xpath(xpath, namespaces=NS)[0]
    ark_elem.text = new_ark

    return mods


def update_element_curator_to_curator(mods):
    global NS
    xpath = "//mods:roleTerm[text()='Contributing Institution']"
    curator = mods.xpath(xpath, namespaces=NS)[0]
    curator.text = "curator"

    return mods


def update_element_curator_name_to_naf(mods):
    global NS
    xpath = "//mods:name/mods:namePart[following-sibling::mods:role/mods:roleTerm/text()='curator' or following-sibling::mods:role/mods:roleTerm/text()='Contributing Institution']"
    curator = mods.xpath(xpath, namespaces=NS)[0]
    curator.text = "Iowa State University. Special Collections and University Archives"

    return mods


def update_element_genre_imt_to_image_tiff(mods):
    global NS
    xpath = "//mods:genre[@authority='imt']"
    imt_type = mods.xpath(xpath, namespaces=NS)[0]
    imt_type.text = "image/tiff"

    return mods


def update_element_local_id_from_filename(mods):
    global NS
    filename_xpath = "string(/mods:mods/mods:identifier[not(@*)])"
    local_id_xpath = "/mods:mods/mods:identifier[@type='local']"
    filename = mods.xpath(filename_xpath)
    local_id = mods.xpath(local_id_xpath)
    local_id.text = filename.split(".")[0]


def update_element_topic_split_on_semicolon(mods):
    global NS
    subjects_xpath = "//mods:subject[mods:topic]"
    subjects = mods.xpath(subjects_xpath, namespaces=NS)
    for s in subjects:
        topics = s.xpath("mods:topic", namespaces=NS)
        for t in topics:
            if t.text is not None:
                if ";" in t.text:
                    ts = [s.strip() for s in t.text.split(";")]
                    t.text = ts[0]
                    for tt in ts[1:]:
                        s.append(etree.fromstring(f"<topic>{tt}</topic>\n"))

    return mods


def update_element_namePart_split_on_semicolon(mods):
    global NS
    xpath = "//mods:subject[mods:name]"
    name_subjects = mods.xpath(xpath, namespaces=NS)
    for s in name_subjects:
        name_type = s.xpath("string(mods:name/@type)", namespaces=NS)
        name_parts = s.xpath("mods:name/mods:namePart", namespaces=NS)
        for np in name_parts:
            if np.text is not None:
                if ";" in np.text:
                    ns = [n.strip() for n in np.text.split(";")]
                    np.text = ns[0]
                    for nn in ns[1:]:
                        s.append(
                            etree.fromstring(
                                f'    <name type="{name_type}">\n      <namePart>{nn}</namePart></name>\n'
                            )
                        )

    return mods


def update_element_geographic_split_on_semicolon(mods):
    global NS
    xpath = "//mods:subject[mods:geographic]"
    subjects = mods.xpath(xpath, namespaces=NS)
    for s in subjects:
        geographic = s.xpath("mods:geographic", namespaces=NS)
        for g in geographic:
            if g.text is not None:
                if ";" in g.text:
                    gs = [s.strip() for s in g.text.split(";")]
                    g.text = gs[0]
                    for gg in gs[1:]:
                        s.append(etree.fromstring(f"<geographic>{gg}</geographic>\n"))

    return mods

def update_element_temporal_split_on_semicolon(mods):
    global NS
    xpath = "//mods:subject[mods:temporal]"
    subjects = mods.xpath(xpath, namespaces=NS)
    for s in subjects:
        temporal = s.xpath("mods:temporal", namespaces=NS)
        for t in temporal:
            if t.text is not None:
                if ";" in t.text:
                    ts = [s.strip() for s in t.text.split(";")]
                    t.text = ts[0]
                    for tt in ts[1:]:
                        s.append(etree.fromstring(f"<temporal>{tt}</temporal>\n"))


# Multi

def universal_changes(mods):
    add_update_attribute_roleTerm_type_text(mods)
    update_attribute_language_type_to_code(mods)
    update_attribute_collection_relatedItem_type_to_original(mods)
    remove_element_identifier_if_empty(mods)


# File handling

def load_cdm(pid):
    try:
        return etree.parse(f"contentdm_data_stream/cdm-{pid}.xml")
    except OSError:
        try:
            return etree.parse(f"cdm-{pid}.xml")
        except OSError:
            return etree.parse(f"{pid}.xml")


def load_mods(pid):
    return etree.parse(f"{pid}.xml")


def load_pids(pid_file):
    with open(pid_file, "r", encoding="utf8") as fh:
        pids = [p.strip() for p in fh if not p.startswith("#")]
    return pids


def save_mods(mods, pid):
    out_xml = etree.tostring(
        mods, xml_declaration=True, encoding="UTF-8", pretty_print=True
    ).decode("utf-8")
    
    with open(f"{pid}.xml", "w", encoding="utf8") as fh:
        fh.write(out_xml)


def save_dc(dc, pid):
    out_xml = etree.tostring(
        dc, xml_declaration=True, encoding="UTF-8", pretty_print=True
    ).decode("utf-8")
    
    with open(f"dc-{pid}.xml", "w", encoding="utf8") as fh:
        fh.write(out_xml)
