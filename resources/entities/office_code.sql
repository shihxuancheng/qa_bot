select '"'||place_code||place_kind||'",'||'"'||place_code||place_kind||'",'||'"'||place_name_c||'",'||'"'||place_name_e||'"' 
from pot1003 where place_kind='01' and (place_code||place_kind)=bkg_office