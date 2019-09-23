select '"' || div_code || '",'||'"'||div_code||'",' || '"' || lower(div_code) || '",' || '"' ||
       div_name_e || '",' || '"' || div_name_c || '"'
  from v_sec_1003 where office_code = 'TWTPE01'