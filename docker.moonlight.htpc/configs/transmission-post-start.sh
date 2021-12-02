#!/bin/sh



USER_PASSWORD_ARG="" # curl invocations' --user argument
HOST_ARG="localhost:9091" # host passed to curl invocations


print_torrents_listing() {
    JSON=$1
    
    STATUS_PAUSED=0
    STATUS_QUEUED=3
    STATUS_DOWNLOADING=4
    STATUS_SEEDING=6
    
    ROW_BY_ROW=$(echo "$TORRENTS_INFO" | sed 's/}\,{/}\
{/g' | sed 's/^{//g' | sed 's/}$//g' | sed 's/}]},\"result\":.*$//g')
    
    # use grep to ignore paused torrents if they shouldn't be listed
    # if [ $TASK_LIST_PAUSED -eq 0 ]
    # then
    #     ROW_BY_ROW=$(echo "$ROW_BY_ROW" | grep -v "\"status\":0")
    # fi
    
    # header of table output
    TABLE_HEADER="Status\tName\tProgress" # Dirty. I'm sorry

    fmt="%-25s%-12s%-12s\n"
    TABLE_HEADER=$(printf "$fmt" STATUS PERCENT NAME)

    
    TABLE_DATA=$(echo "$ROW_BY_ROW" | while read LINE
    do
        STATUS=$(echo "$LINE" | grep -Eo "\".*status\":(.*?)\$" | sed 's/.*\"status\"://')

        TORRENT_ID=$(echo "$LINE" | sed 's/.*id\"://g;s/\,.*//g')
        TORRENT_NAME=$(echo "$LINE" | sed 's/.*name\":\"//g;s/\"\}.*//g')
        
        NAME=$(echo "$LINE" | grep -Eo "\"name\":\"(.*?)\"" | sed 's/\"name\":\"//' | sed 's/\"$//')
        PERCENT_DONE=$(echo "$LINE" | grep -Eo "\"percentDone\":(.*?)," | sed 's/\"percentDone\"://' | sed 's/,$//')
        PERCENT_DONE=$(perl -e "print int($PERCENT_DONE*100)")
        # RATE_DOWNLOAD=$(echo "$LINE" | grep -Eo "\"rateDownload\":(.*?)," | sed 's/\"rateDownload\"://' | sed 's/,$//')
        # RATE_UPLOAD=$(echo "$LINE" | grep -Eo "\"rateUpload\":(.*?)," | sed 's/\"rateUpload\"://' | sed 's/,$//')
        
        # RATE_DOWNLOAD_KB=$(perl -e "printf('%.1f', $RATE_DOWNLOAD/1024)")
        # RATE_UPLOAD_KB=$(perl -e "printf('%.1f', $RATE_UPLOAD/1024)")
        
        # turn status code into string
        if [ "$STATUS" -eq $STATUS_QUEUED ]
        then
            STATUS_STRING="Queued"
        elif [ "$STATUS" -eq $STATUS_DOWNLOADING ]
        then
            STATUS_STRING="Dl"
        elif [ "$STATUS" -eq $STATUS_SEEDING ]
        then
            STATUS_STRING="Seeding"
        elif [ "$STATUS" -eq $STATUS_PAUSED ]
        then
            STATUS_STRING="Paused"
            if [ "$PERCENT_DONE" -ne "100" ]
            then
                printf "$fmt" "$STATUS_STRING" "$PERCENT_DONE" "$TORRENT_ID\n"
                curl --silent --anyauth$USER_PASSWORD_ARG --header "$SESSION_HEADER" "http://$HOST_ARG/transmission/rpc" -d "{\"method\":\"torrent-start-now\",\"arguments\": {\"ids\":[${TORRENT_ID}]}}"
            fi
        else
            STATUS_STRING="N/A"
        fi
        
        # printf "${STATUS_STRING}\t%.40s\t${PERCENT_DONE}%s\t${RATE_DOWNLOAD_KB} KB/s\t${RATE_UPLOAD_KB} KB/s\n" "$NAME" "%%"

        

    done)
    
    # printf "${TABLE_HEADER}\n${TABLE_DATA}\n" | column -ts $'\t' | colorize_table

    printf "${TABLE_HEADER}\n${TABLE_DATA}\n"
}


sleep 15


# set USER_PASSWORD_ARG
if [ ! -z "$RPC_USER" ] && [ ! -z "$RPC_PASSWORD" ]
then
    USER_PASSWORD_ARG=" --user $RPC_USER:$RPC_PASSWORD"
elif [ ! -z "$RPC_USER" ]
then
    USER_PASSWORD_ARG=" --user $RPC_USER"
elif [ ! -z "$RPC_PASSWORD" ]
then
    echo "You specified a password but no username"
    exit 1
fi
# get header for this Transmission RPC session
SESSION_HEADER=$(curl --silent --anyauth$USER_PASSWORD_ARG -L $HOST_ARG/transmission/rpc/ | sed 's/.*<code>//g;s/<\/code>.*//g')


TORRENTS_INFO=$(curl --silent --anyauth$USER_PASSWORD_ARG --header "$SESSION_HEADER" "http://$HOST_ARG/transmission/rpc" -d "{\"method\":\"torrent-get\",\"arguments\": {\"fields\":[\"id\",\"percentDone\",\"status\",\"name\"]}}")
if [ "$?" -gt 0 ]
then
    printf "Error: Could not connect to Transmission RPC server."
    exit 1
fi

print_torrents_listing "$TORRENTS_INFO"
exit 0