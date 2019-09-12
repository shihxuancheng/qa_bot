select '"' || system_code || '",'||'"'||system_code||'",' || '"' || lower(system_code) || '",' || '"' ||
       replace(replace(system_name_c,'(','['),')',']') || '",' || '"' || replace(replace(system_name_e,'(','['),')',']') || '"'
  from sec1103
 where system_loc <> 'CN'
 and instr(system_name_c,'(暫停使用)')<=0
