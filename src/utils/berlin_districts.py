"""
Berlin postal code and district mapping utility.
Maps Berlin districts (Bezirke) to their postal codes for easier filtering.
"""

from typing import List, Set

# Berlin postal codes by district (Bezirk)
BERLIN_DISTRICTS_TO_POSTAL_CODES = {
    # Mitte
    "mitte": [
        "10115", "10117", "10119", "10178", "10179", "10435", "10551", "10553", "10555", 
        "10557", "10559", "10623", "10785", "10787", "13347", "13349", "13351", "13353", 
        "13355", "13357", "13359", "13407", "13409"
    ],
    
    # Friedrichshain-Kreuzberg
    "friedrichshain-kreuzberg": [
        "10179", "10243", "10245", "10247", "10249", "10961", "10963", "10965", 
        "10967", "10969", "10997", "10999"
    ],
    "friedrichshain": [  # Alias for part of Friedrichshain-Kreuzberg
        "10243", "10245", "10247", "10249"
    ],
    "kreuzberg": [  # Alias for part of Friedrichshain-Kreuzberg
        "10961", "10963", "10965", "10967", "10969", "10997", "10999"
    ],
    
    # Pankow
    "pankow": [
        "10119", "10405", "10407", "10409", "10435", "10437", "10439", "13051", 
        "13053", "13086", "13088", "13089", "13125", "13127", "13129", "13156", 
        "13158", "13159", "13187", "13189"
    ],
    
    # Charlottenburg-Wilmersdorf
    "charlottenburg-wilmersdorf": [
        "10585", "10587", "10589", "10623", "10625", "10627", "10629", "10707", 
        "10709", "10711", "10713", "10715", "10717", "10719", "13627", "14050", 
        "14052", "14053", "14055", "14057", "14059", "14193", "14195", "14197", "14199"
    ],
    "charlottenburg": [  # Alias for part of Charlottenburg-Wilmersdorf
        "10585", "10587", "10589", "10623", "10625", "10627", "10629", "14050", 
        "14052", "14053", "14055", "14057", "14059"
    ],
    "wilmersdorf": [  # Alias for part of Charlottenburg-Wilmersdorf
        "10707", "10709", "10711", "10713", "10715", "10717", "10719", "14193", 
        "14195", "14197", "14199"
    ],
    
    # Spandau
    "spandau": [
        "13581", "13583", "13585", "13587", "13589", "13591", "13593", "13595", 
        "13597", "13599", "14052", "14089"
    ],
    
    # Steglitz-Zehlendorf
    "steglitz-zehlendorf": [
        "12157", "12159", "12161", "12163", "12165", "12167", "12169", "12203", 
        "12205", "12207", "12209", "12247", "12249", "12277", "12279", "14109", 
        "14129", "14163", "14165", "14167", "14169", "14195", "14199"
    ],
    "steglitz": [  # Alias for part of Steglitz-Zehlendorf  
        "12157", "12159", "12161", "12163", "12165", "12167", "12169", "12247", "12249"
    ],
    "zehlendorf": [  # Alias for part of Steglitz-Zehlendorf
        "14109", "14129", "14163", "14165", "14167", "14169", "14195", "14199"
    ],
    
    # Tempelhof-Schöneberg
    "tempelhof-schoeneberg": [
        "10777", "10779", "10781", "10783", "10785", "10787", "10789", "10823", 
        "10825", "10827", "10829", "12099", "12101", "12103", "12105", "12107", 
        "12109", "12157", "12247", "12277", "12279", "12305", "12307", "12309"
    ],
    "tempelhof": [  # Alias for part of Tempelhof-Schöneberg
        "12099", "12101", "12103", "12105", "12107", "12109", "12247"
    ],
    "schoeneberg": [  # Alias for part of Tempelhof-Schöneberg
        "10777", "10779", "10781", "10783", "10785", "10787", "10789", "10823", 
        "10825", "10827", "10829", "12157", "12277", "12279"
    ],
    
    # Neukölln
    "neukoelln": [
        "12043", "12045", "12047", "12049", "12051", "12053", "12055", "12057", 
        "12059", "12347", "12349", "12351", "12353", "12355", "12357", "12359"
    ],
    
    # Treptow-Köpenick
    "treptow-koepenick": [
        "12435", "12437", "12439", "12459", "12487", "12489", "12524", "12526", 
        "12527", "12555", "12557", "12559", "12587", "12589", "12623"
    ],
    "treptow": [  # Alias for part of Treptow-Köpenick
        "12435", "12437", "12439"
    ],
    "koepenick": [  # Alias for part of Treptow-Köpenick
        "12459", "12487", "12489", "12524", "12526", "12527", "12555", "12557", 
        "12559", "12587", "12589", "12623"
    ],
    
    # Marzahn-Hellersdorf
    "marzahn-hellersdorf": [
        "12619", "12621", "12623", "12627", "12629", "12679", "12681", "12683", 
        "12685", "12687", "12689"
    ],
    "marzahn": [  # Alias for part of Marzahn-Hellersdorf
        "12679", "12681", "12683", "12685", "12687", "12689"
    ],
    "hellersdorf": [  # Alias for part of Marzahn-Hellersdorf
        "12619", "12621", "12623", "12627", "12629"
    ],
    
    # Lichtenberg
    "lichtenberg": [
        "10315", "10317", "10318", "10319", "10365", "10367", "10369", "13051", 
        "13053", "13055", "13057", "13059"
    ],
    
    # Reinickendorf
    "reinickendorf": [
        "13403", "13405", "13407", "13409", "13435", "13437", "13439", "13465", 
        "13467", "13469", "13503", "13505", "13507", "13509", "13591", "13629"
    ]
}

# Aliases for common alternative names
DISTRICT_ALIASES = {
    # Alternative spellings
    "friedrichshain_kreuzberg": "friedrichshain-kreuzberg",
    "charlottenburg_wilmersdorf": "charlottenburg-wilmersdorf", 
    "steglitz_zehlendorf": "steglitz-zehlendorf",
    "tempelhof_schoeneberg": "tempelhof-schoeneberg",
    "treptow_koepenick": "treptow-koepenick",
    "marzahn_hellersdorf": "marzahn-hellersdorf",
    
    # Short forms
    "xberg": "kreuzberg",
    "fhain": "friedrichshain",
    "neuk": "neukoelln",
    "schberg": "schoeneberg",
    
    # With umlaut
    "neuköln": "neukoelln", 
    "köpenick": "koepenick",
    "schöneberg": "schoeneberg"
}


def get_postal_codes_for_districts(districts: List[str]) -> List[str]:
    """
    Get all postal codes for the given Berlin districts.
    
    Args:
        districts: List of district names (case insensitive)
        
    Returns:
        List of postal codes for all specified districts
        
    Examples:
        >>> get_postal_codes_for_districts(["mitte", "kreuzberg"])
        ['10115', '10117', ..., '10961', '10963', ...]
        
        >>> get_postal_codes_for_districts(["treptow-koepenick"])
        ['12435', '12437', '12439', '12459', ...]
    """
    postal_codes: Set[str] = set()
    
    for district in districts:
        # Normalize district name (lowercase, strip whitespace)
        district_normalized = district.lower().strip()
        
        # Check for alias
        if district_normalized in DISTRICT_ALIASES:
            district_normalized = DISTRICT_ALIASES[district_normalized]
        
        # Get postal codes for district
        if district_normalized in BERLIN_DISTRICTS_TO_POSTAL_CODES:
            postal_codes.update(BERLIN_DISTRICTS_TO_POSTAL_CODES[district_normalized])
        else:
            # List available districts for helpful error message
            available = list(BERLIN_DISTRICTS_TO_POSTAL_CODES.keys())
            aliases = list(DISTRICT_ALIASES.keys())
            raise ValueError(
                f"Unknown Berlin district: '{district}'. "
                f"Available districts: {available}. "
                f"Available aliases: {aliases}"
            )
    
    return sorted(list(postal_codes))


def get_all_berlin_postal_codes() -> List[str]:
    """
    Get all postal codes in Berlin.
    
    Returns:
        Sorted list of all Berlin postal codes
    """
    all_codes: Set[str] = set()
    for codes in BERLIN_DISTRICTS_TO_POSTAL_CODES.values():
        all_codes.update(codes)
    return sorted(list(all_codes))


def get_district_for_postal_code(postal_code: str) -> str:
    """
    Get the district name for a given postal code.
    
    Args:
        postal_code: The postal code to look up
        
    Returns:
        District name, or "unknown" if postal code is not found
        
    Examples:
        >>> get_district_for_postal_code("12459")
        'treptow-koepenick'
        
        >>> get_district_for_postal_code("10961")
        'friedrichshain-kreuzberg'
    """
    for district, codes in BERLIN_DISTRICTS_TO_POSTAL_CODES.items():
        if postal_code in codes:
            return district
    return "unknown"


if __name__ == "__main__":
    # Test the functions
    print("=== Berlin District Mapping Test ===")
    
    # Test single district
    mitte_codes = get_postal_codes_for_districts(["mitte"])
    print(f"Mitte postal codes ({len(mitte_codes)}): {mitte_codes[:5]}...")
    
    # Test multiple districts
    multi_codes = get_postal_codes_for_districts(["kreuzberg", "friedrichshain"])
    print(f"Kreuzberg + Friedrichshain ({len(multi_codes)}): {multi_codes[:5]}...")
    
    # Test combined district
    combined_codes = get_postal_codes_for_districts(["friedrichshain-kreuzberg"])
    print(f"Friedrichshain-Kreuzberg ({len(combined_codes)}): {combined_codes[:5]}...")
    
    # Test lookup
    print(f"District for 12459: {get_district_for_postal_code('12459')}")
    
    # Test total count
    all_codes = get_all_berlin_postal_codes()
    print(f"Total Berlin postal codes: {len(all_codes)}")