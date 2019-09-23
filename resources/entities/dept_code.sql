select '"' || dept_code || '",'||'"'||dept_code||'",' || '"' || lower(dept_code) || '",' || '"' ||
       dept_name_e || '",' || '"' || dept_name_c || '"'
  from v_sec_1004 where office_code = 'TWTPE01'