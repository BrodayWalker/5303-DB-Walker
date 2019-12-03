# Open data file
data = open("MOCK_DATA.csv", "r")
# Open output file which will contain redis commands
out = open("data.txt", "w")

# The first line of the data file contains labels.
# Comment this section out if your data doesn't have labels. Or don't.
labels = data.readline()
labels = labels.splitlines()[0]
labels = labels.split(sep=",")

#############################################################################
#   The following loop outputs commands per the redis protocol which can be
# found at https://redis.io/topics/mass-insert
#
#   A command should look as follows (newlines shown for clarity):
#           *<args><cr><lf>            
#           $<len><cr><lf>
#           <arg0><cr><lf>   
#           <arg1><cr><lf>
#           ...
#           <argN><cr><lf>            
# 
#           Example:
#           $3<cr><lf>
#           SET<cr><lf>
#           $3<cr><lf>
#           key<cr><lf>
#           $5<cr><lf>
#           value<cr><lf>
#   
#############################################################################

user_id = 0

for line in data:
    # Split dat data.
    split_dat = line.split(sep=",") # separate data into an array
    split_dat[-1] = split_dat[-1].strip() # remove trailing newline
    
    # Command Template (no spaces):
    # HMSET user:1000 first_name <value> last_name <value> email <value> \
    # lati <value> longi <value>
    #
    # Note that there are 12 words we are sending through the redis pipe.
    # For this reason, we specify the redis array length as *12
    #
    # Because we must specify the number of bytes for each piece of data 
    # being sent, it is necessary to keep track of the number of digits
    # in the each field.
    user_id_char_count = len(f'user:{user_id}')
    first_name_len = len(split_dat[0])
    last_name_len = len(split_dat[1])
    email_len = len(split_dat[2])
    lati_len = len(split_dat[3])
    longi_len = len(split_dat[4])

    # Abandon hope all ye who generate redis pipe data here.
    out.write(f"*12\\r\\n$5\\r\\nHMSET\\r\\n${user_id_char_count}\\r\\nuser:{user_id}\\r\\n$10\\r\\nfirst_name\\r\\n${first_name_len}\\r\\n{split_dat[0]}\\r\\n$9\\r\\nlast_name\\r\\n${last_name_len}\\r\\n{split_dat[1]}\\r\\n$5\\r\\nemail\\r\\n${email_len}\\r\\n{split_dat[2]}\\r\\n$4\\r\\nlati\\r\\n${lati_len}\\r\\n{split_dat[3]}\\r\\n$5\\r\\nlongi\\r\\n${longi_len}\\r\\n{split_dat[4]}\\r\\n")

    user_id += 1

out.close()
data.close()