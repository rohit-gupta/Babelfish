cat hiwiki-20180501-langlinks.sql | grep -n ",'en'," | cut -c-10 | awk -F ":" '{print $1}' > hi-en_link_rows.txt
awk 'NR==FNR{a[$1]++;next} { if(FNR in a){ print } }' hi-en_link_rows.txt hiwiki-20180501-langlinks.sql > links_raw_queries.txt
