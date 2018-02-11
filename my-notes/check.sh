#!/bin/bash
# Check if an MD file can fit in ~1 page

send() {
    echo "📝  $1"
}

echo ""
send "CAN IT FIT IN 1 PAGE?"
fileLength="$(wc -l $1 | awk '{ print $1 }')"
send "File contains ${fileLength} lines"
if [ $fileLength -gt 46 ]; then
    echo ""
    send "️️That's more than 1 page! ⚠️"
    let "extraLines = $fileLength - 46"
    if [ 1 -eq 1 ]; then
        send "️Cut down by $extraLines line! 😈"
    else
        send "️Cut down by $extraLines lines! 😈"
    fi
else
    send "Nice one! 🤓"
fi
echo ""